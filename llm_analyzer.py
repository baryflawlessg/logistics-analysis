#!/usr/bin/env python3
"""
LLM-Enhanced Delivery Failure Analysis System
============================================

This system uses Ollama (local LLM) for natural language processing
to understand questions and extract parameters for analysis.

Requirements:
- Ollama installed locally
- A model like llama2 or mistral running in Ollama

Usage:
    python llm_analyzer.py

Author: AI Assistant
Date: 2024
"""

from simple_delivery_analyzer import SimpleDeliveryAnalyzer
import json
import requests
import re
from datetime import datetime, timedelta
import os

class LLMEnhancedAnalyzer:
    """Delivery failure analyzer enhanced with OpenAI API for NLP."""
    
    def __init__(self, openai_api_key="", model="gpt-3.5-turbo"):
        """Initialize the OpenAI-enhanced analyzer."""
        self.analyzer = SimpleDeliveryAnalyzer()
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.analyzer.load_all_data()
        
        # Define table relationships
        self.relationships = {
            "orders": {
                "primary_key": "order_id",
                "foreign_keys": {
                    "client_id": "clients"
                },
                "referenced_by": {
                    "order_id": ["external_factors", "feedback", "fleet_logs", "warehouse_logs"]
                }
            },
            "warehouse_logs": {
                "primary_key": "log_id",
                "foreign_keys": {
                    "order_id": "orders",
                    "warehouse_id": "warehouses"
                }
            },
            "fleet_logs": {
                "primary_key": "fleet_log_id",
                "foreign_keys": {
                    "order_id": "orders",
                    "driver_id": "drivers"
                }
            },
            "external_factors": {
                "primary_key": "factor_id",
                "foreign_keys": {
                    "order_id": "orders"
                }
            },
            "feedback": {
                "primary_key": "feedback_id",
                "foreign_keys": {
                    "order_id": "orders"
                }
            },
            "clients": {
                "primary_key": "client_id"
            },
            "drivers": {
                "primary_key": "driver_id"
            },
            "warehouses": {
                "primary_key": "warehouse_id"
            }
        }
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to constructor.")
    
    def _classify_question(self, question):
        """Classify question type using LLM."""
        prompt = f"""
        Classify this question: "{question}"
        
        Question Types:
        - "data_query": Can be answered with current data only (e.g., "What are current failure rates?", "Which city has most orders?")
        - "analytical": Requires analysis, prediction, or recommendations only (e.g., "What will happen if we add 20,000 orders?", "How should we prepare?")
        - "hybrid": Has both data and analytical elements (e.g., "What are likely causes and how should we prepare?")
        
        Return JSON: {{"type": "data_query|analytical|hybrid", "reasoning": "explanation"}}
        """
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a question classifier. Return only valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 200
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                llm_response = result['choices'][0]['message']['content'].strip()
                
                # Extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    classification = json.loads(json_str)
                    return classification["type"]
                else:
                    return "data_query"  # Default fallback
            else:
                return "data_query"  # Default fallback
                
        except Exception as e:
            print(f"⚠️ Classification error: {e}")
            return "data_query"  # Default fallback
    
    def _process_data_query(self, question):
        """Process data query questions."""
        print("🔄 Processing data query...")
        
        # Step 1: LLM generates query
        query_params = self.process_with_llm(question)
        print(f"🔍 LLM generated query: {query_params}")
        
        # Step 2: Execute query on data
        results = self.execute_query(query_params)
        
        # Step 3: Generate insights from results
        insights = self._generate_insights(question, query_params, results)
        
        return {
            "question": question,
            "type": "data_query",
            "query_params": query_params,
            "results": results,
            "insights": insights
        }
    
    def _process_analytical_question(self, question):
        """Process analytical questions."""
        print("🔄 Processing analytical question...")
        
        # Generate analytical insights using LLM
        insights = self._generate_analytical_insights(question)
        
        return {
            "question": question,
            "type": "analytical",
            "insights": insights
        }
    
    def _process_hybrid_question(self, question):
        """Process hybrid questions with both data and analytical elements."""
        print("🔄 Processing hybrid question...")
        
        # Stage 1: Get data
        print("📊 Stage 1: Data Analysis")
        data_results = self._process_data_query(question)
        
        # Stage 2: Generate analytical insights
        print("🧠 Stage 2: Analytical Insights")
        analytical_insights = self._generate_analytical_insights(question, data_results)
        
        # Stage 3: Combine results
        combined_insights = data_results["insights"] + analytical_insights
        
        return {
            "question": question,
            "type": "hybrid",
            "data_results": data_results,
            "analytical_insights": analytical_insights,
            "combined_insights": combined_insights
        }
    
    def _generate_analytical_insights(self, question, data_results=None):
        """Generate analytical insights using LLM."""
        prompt = f"""
        Question: "{question}"
        
        Based on your expertise in logistics and delivery operations, provide analytical insights and recommendations.
        
        {f"Data Context: {data_results['results'] if data_results else 'No specific data provided'}"}
        
        Provide:
        1. Key insights and patterns
        2. Risk assessment
        3. Specific recommendations
        4. Implementation strategies
        
        Be specific, actionable, and data-driven.
        """
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a senior logistics analyst with 10+ years of experience. Provide specific, actionable insights."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                insights = result['choices'][0]['message']['content'].strip()
                return [insights]
            else:
                return ["Unable to generate analytical insights at this time."]
                
        except Exception as e:
            print(f"⚠️ Analytical insights error: {e}")
            return ["Unable to generate analytical insights at this time."]
    
    def _execute_warehouse_sales_join(self, query_params):
        """Execute warehouse sales analysis by joining warehouse_logs and orders."""
        print("🔍 Executing warehouse sales join...")
        
        # Get data from both tables
        warehouse_logs = self.analyzer.data.get('warehouse_logs', [])
        orders = self.analyzer.data.get('orders', [])
        
        if not warehouse_logs or not orders:
            return {"error": "Missing warehouse_logs or orders data"}
        
        # Create lookup dictionaries for efficient joining
        orders_lookup = {order['order_id']: order for order in orders}
        
        # Join the data
        joined_data = []
        for log in warehouse_logs:
            order_id = log.get('order_id')
            if order_id in orders_lookup:
                order = orders_lookup[order_id]
                # Create joined record
                joined_record = {
                    'warehouse_id': log.get('warehouse_id'),
                    'order_id': order_id,
                    'amount': float(order.get('amount', 0)),
                    'status': order.get('status'),
                    'city': order.get('city')
                }
                joined_data.append(joined_record)
        
        print(f"🔍 Joined {len(joined_data)} records")
        
        # Apply filters
        filters = query_params.get('filters', {})
        if filters:
            for col, val in filters.items():
                if col == 'status':
                    joined_data = [row for row in joined_data if row.get(col, '').lower() == str(val).lower()]
        
        # Group by warehouse_id and sum amounts
        warehouse_sales = {}
        for record in joined_data:
            warehouse_id = record['warehouse_id']
            amount = record['amount']
            
            if warehouse_id not in warehouse_sales:
                warehouse_sales[warehouse_id] = 0
            warehouse_sales[warehouse_id] += amount
        
        # Convert to results format
        results = []
        for warehouse_id, total_sales in warehouse_sales.items():
            results.append({
                'warehouse_id': warehouse_id,
                'sum_amount': total_sales
            })
        
        # Sort by sales amount
        results.sort(key=lambda x: x['sum_amount'], reverse=True)
        
        # Apply limit
        limit = query_params.get('limit', 1)
        if limit:
            results = results[:limit]
        
        return results
    
    def _get_relationship_info(self):
        """Get table relationship information for LLM understanding."""
        relationship_info = "Table Relationships:\n"
        for table, info in self.relationships.items():
            relationship_info += f"\n{table}:\n"
            if "foreign_keys" in info:
                relationship_info += "  Foreign Keys:\n"
                for fk_col, ref_table in info["foreign_keys"].items():
                    relationship_info += f"    {fk_col} -> {ref_table}\n"
            if "referenced_by" in info:
                relationship_info += "  Referenced By:\n"
                for ref_col, ref_tables in info["referenced_by"].items():
                    relationship_info += f"    {ref_col} <- {', '.join(ref_tables)}\n"
        
        return relationship_info
    
    def _get_data_schema(self):
        """Get data schema with sample data for LLM understanding."""
        import csv
        from pathlib import Path
        
        schema = {}
        sample_data_folder = Path("sample-data")
        
        # Define the files and their descriptions
        files_info = {
            "sample_orders.csv": {
                "table_name": "orders",
                "description": "Delivery orders with amounts, cities, clients, status, failure reasons"
            },
            "sample_clients.csv": {
                "table_name": "clients", 
                "description": "Client information and contact details"
            },
            "sample_warehouses.csv": {
                "table_name": "warehouses",
                "description": "Warehouse locations, capacity, and management"
            },
            "sample_drivers.csv": {
                "table_name": "drivers",
                "description": "Driver information and performance data"
            },
            "sample_fleet_logs.csv": {
                "table_name": "fleet_logs",
                "description": "Fleet vehicle logs and maintenance records"
            },
            "sample_warehouse_logs.csv": {
                "table_name": "warehouse_logs", 
                "description": "Warehouse operations and inventory logs"
            },
            "sample_external_factors.csv": {
                "table_name": "external_factors",
                "description": "External factors like weather, traffic, events"
            },
            "sample_feedback.csv": {
                "table_name": "feedback",
                "description": "Customer feedback and ratings"
            }
        }
        
        # Read sample data from each file
        for filename, info in files_info.items():
            filepath = sample_data_folder / filename
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        rows = list(reader)
                        
                        if rows:
                            # Get columns from first row
                            columns = list(rows[0].keys())
                            
                            # Get sample rows (first 3 rows)
                            sample_rows = rows[:3]
                            
                            schema[info["table_name"]] = {
                                "description": info["description"],
                                "columns": columns,
                                "sample_data": sample_rows
                            }
                except Exception as e:
                    print(f"Warning: Could not read {filename}: {e}")
        
        return json.dumps(schema, indent=2)
        
    def ask_question(self, question):
        """Ask a question using LLM-generated queries."""
        print(f"\n🤔 Question: {question}")
        print("=" * 60)
        
        try:
            # Step 1: Classify question type
            question_type = self._classify_question(question)
            print(f"🔍 Question type: {question_type}")
            
            if question_type == "hybrid":
                return self._process_hybrid_question(question)
            elif question_type == "analytical":
                return self._process_analytical_question(question)
            else:
                return self._process_data_query(question)
            
        except Exception as e:
            print(f"❌ Error processing question: {e}")
            return {"error": f"Error processing question: {e}"}
    
    def process_with_llm(self, question):
        """Use LLM to generate data query from question intent."""
        
        # Get data schema
        schema = self._get_data_schema()
        relationships = self._get_relationship_info()
        
        prompt = f"""You are a data analyst. Generate a data query for this question: "{question}"

Available Data Schema with Sample Data:
{schema}

{relationships}

Instructions:
- Use the sample data to understand the actual data values and formats
- Generate appropriate filters based on the sample data patterns
- Consider the relationships between tables (e.g., client_id links orders to clients)
- For date filters, use actual dates from the sample data (e.g., "2025-09-15", "2025-08-20")
- For time periods, use specific date ranges that exist in the data
- For festival/seasonal queries, use actual dates from the sample data that represent those periods
- IMPORTANT: System can perform basic joins for specific queries (warehouse sales analysis)
- For warehouse sales analysis: Use orders table - system will automatically join with warehouse_logs
- For driver performance analysis: Use fleet_logs table (has driver_id but no performance metrics)
- For client analysis: Use clients table for client info, orders table for client orders
- When relationships are needed but joins are not possible, provide alternative analysis using available data

Return JSON:
{{
    "intent": "what user wants",
    "table": "orders|clients|warehouses|drivers|fleet_logs|warehouse_logs|external_factors|feedback",
    "group_by": "column",
    "aggregations": {{"column": "sum|count|avg"}},
    "filters": {{"column": "value"}},
    "sort_by": "column",
    "sort_order": "desc|asc",
    "limit": number
}}

Examples:
"Which city has highest sales?" -> {{"intent": "Find city with highest sales", "table": "orders", "group_by": "city", "aggregations": {{"amount": "sum"}}, "sort_by": "sum_amount", "sort_order": "desc", "limit": 1}}
"How many clients?" -> {{"intent": "Count clients", "table": "clients", "aggregations": {{"client_id": "count"}}}}
"Why were deliveries delayed in Chennai?" -> {{"intent": "Analyze delivery delays in Chennai", "table": "orders", "filters": {{"city": "Chennai", "status": "Failed"}}, "group_by": "failure_reason", "aggregations": {{"order_id": "count"}}}}
"Compare delivery failure causes between Chennai and Mumbai" -> {{"intent": "Compare failure causes between cities", "table": "orders", "filters": {{"city": ["Chennai", "Mumbai"], "status": "Failed"}}, "group_by": "city,failure_reason", "aggregations": {{"order_id": "count"}}, "sort_by": "city"}}
"What are the likely causes of delivery failures during the festival period?" -> {{"intent": "Analyze festival period failures", "table": "orders", "filters": {{"status": "Failed", "order_date": "2025-09-15"}}, "group_by": "failure_reason", "aggregations": {{"order_id": "count"}}, "sort_by": "count_order_id", "sort_order": "desc"}}
"Identify top reasons for delivery failures linked to Warehouse 20" -> {{"intent": "Analyze warehouse failures", "table": "orders", "filters": {{"status": "Failed"}}, "group_by": "failure_reason", "aggregations": {{"order_id": "count"}}, "sort_by": "count_order_id", "sort_order": "desc", "limit": 5}}
"Which warehouse had the most sale amount?" -> {{"intent": "Identify warehouse with highest sales", "table": "orders", "filters": {{"status": "Delivered"}}, "group_by": "warehouse_id", "aggregations": {{"amount": "sum"}}, "sort_by": "sum_amount", "sort_order": "desc", "limit": 1}}

JSON:"""
        
        # OpenAI API call
        try:
            print("🔄 Asking OpenAI for query generation...")
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a data analyst. Generate JSON queries for data analysis. Always return valid JSON only."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.1,
                    "max_tokens": 500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                llm_response = result['choices'][0]['message']['content'].strip()
                
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    query_params = json.loads(json_str)
                    print("✅ OpenAI generated query successfully")
                    return query_params
                else:
                    print(f"❌ Could not extract JSON from OpenAI response: {llm_response[:200]}...")
                    raise Exception("OpenAI did not return valid JSON")
            else:
                error_detail = response.json().get('error', {}).get('message', 'Unknown error')
                print(f"❌ OpenAI API error: {response.status_code} - {error_detail}")
                raise Exception(f"OpenAI API error: {error_detail}")
                
        except requests.exceptions.Timeout:
            print("⏰ OpenAI timeout")
            raise Exception("OpenAI timeout")
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
            raise Exception(f"OpenAI failed: {e}")
    
    def _fallback_query(self, question):
        """Fallback query generation when LLM fails."""
        print("🔄 Using fallback query generation...")
        question_lower = question.lower()
        
        # Enhanced keyword-based fallback
        cities = ['chennai', 'mumbai', 'delhi', 'bangalore', 'pune', 'ahmedabad', 'surat', 'coimbatore']
        found_cities = [city for city in cities if city in question_lower]
        
        # City ranking by sales
        if 'which city' in question_lower and any(word in question_lower for word in ['highest', 'best', 'most', 'top']):
            return {
                "intent": "Find city with highest sales",
                "table": "orders",
                "group_by": "city",
                "aggregations": {"amount": "sum"},
                "sort_by": "sum_amount",
                "sort_order": "desc",
                "limit": 1
            }
        
        # City delay analysis
        if 'delayed' in question_lower and 'chennai' in question_lower:
            return {
                "intent": "Analyze delivery delays in Chennai",
                "table": "orders",
                "filters": {"city": "Chennai", "status": "Failed"},
                "group_by": "failure_reason",
                "aggregations": {"order_id": "count"},
                "sort_by": "count_order_id",
                "sort_order": "desc"
            }
        
        # City comparison
        if 'compare' in question_lower and len(found_cities) >= 2:
            return {
                "intent": f"Compare {found_cities[0]} and {found_cities[1]}",
                "table": "orders",
                "group_by": "city",
                "filters": {"city": f"{found_cities[0]}|{found_cities[1]}"},
                "aggregations": {"amount": "sum", "order_id": "count"},
                "sort_by": "sum_amount",
                "sort_order": "desc"
            }
        
        # Client ranking
        if any(word in question_lower for word in ['top', 'best', 'worst']) and 'client' in question_lower:
            numbers = re.findall(r'\d+', question)
            limit = int(numbers[0]) if numbers else 5
            return {
                "intent": f"Rank top {limit} clients",
                "table": "orders",
                "group_by": "client_id",
                "aggregations": {"order_id": "count"},
                "sort_by": "count_order_id",
                "sort_order": "desc",
                "limit": limit
            }
        
        # Client count
        if any(phrase in question_lower for phrase in ['how many client', 'total client', 'client count']):
            return {
                "intent": "Count total clients",
                "table": "clients",
                "aggregations": {"client_id": "count"}
            }
        
        # Default to general analysis
        return {
            "intent": "General analysis",
            "table": "orders",
            "aggregations": {"order_id": "count", "amount": "sum"}
        }
    
    def execute_query(self, query_params):
        """Execute the LLM-generated query on actual data."""
        table = query_params.get('table', 'orders')
        group_by = query_params.get('group_by')
        aggregations = query_params.get('aggregations', {})
        filters = query_params.get('filters', {})
        sort_by = query_params.get('sort_by')
        sort_order = query_params.get('sort_order', 'desc')
        limit = query_params.get('limit')
        
        print(f"🔍 Executing query: {query_params}")
        
        # Check if this is a warehouse sales query that needs joining
        if (table == 'orders' and 'warehouse' in query_params.get('intent', '').lower() and 
            'sales' in query_params.get('intent', '').lower()):
            print("🔍 Detected warehouse sales query - attempting join")
            return self._execute_warehouse_sales_join(query_params)
        
        # Get data
        print(f"🔍 Available tables: {list(self.analyzer.data.keys())}")
        print(f"🔍 Looking for table: {table}")
        data = self.analyzer.data.get(table, [])
        if not data:
            return {"error": f"No data found for table: {table}. Available tables: {list(self.analyzer.data.keys())}"}
        
        # Apply filters
        if filters:
            print(f"🔍 Applying filters: {filters}")
            for col, val in filters.items():
                print(f"🔍 Filtering column '{col}' for value '{val}'")
                
                # Handle multiple values (list or pipe-separated string)
                if isinstance(val, list):
                    print(f"🔍 Multiple values (list): {val}")
                    data = [row for row in data if str(row.get(col, '')).lower() in [v.lower() for v in val]]
                elif '|' in str(val):  # Pipe-separated string
                    values = str(val).split('|')
                    print(f"🔍 Multiple values (pipe): {values}")
                    data = [row for row in data if str(row.get(col, '')).lower() in [v.lower() for v in values]]
                else:
                    print(f"🔍 Single value filter")
                    # Handle date filtering - check if column contains dates
                    if any(date_col in col.lower() for date_col in ['date', 'time', 'created', 'updated']):
                        print(f"🔍 Date column detected: {col}")
                        # For date columns, check if the filter value matches the date part
                        filter_val = str(val).lower()
                        data = [row for row in data if filter_val in str(row.get(col, '')).lower()]
                    else:
                        data = [row for row in data if str(row.get(col, '')).lower() == str(val).lower()]
                print(f"🔍 Data after filter: {len(data)} rows")
        
        # Group and aggregate
        if group_by:
            groups = {}
            for row in data:
                # Handle multiple group_by columns (comma-separated)
                if ',' in group_by:
                    group_columns = [col.strip() for col in group_by.split(',')]
                    key = tuple(row.get(col, 'Unknown') for col in group_columns)
                    # Create a readable key for display
                    key_display = ' | '.join(f"{col}: {row.get(col, 'Unknown')}" for col in group_columns)
                else:
                    key = row.get(group_by, 'Unknown')
                    key_display = key
                
                if key not in groups:
                    groups[key] = []
                groups[key].append(row)
            
            # Calculate aggregations
            results = []
            for group_key, group_data in groups.items():
                if ',' in group_by:
                    group_columns = [col.strip() for col in group_by.split(',')]
                    result = {}
                    for i, col in enumerate(group_columns):
                        result[col] = group_key[i] if isinstance(group_key, tuple) else group_key
                else:
                    result = {group_by: group_key}
                for col, operation in aggregations.items():
                    if operation == 'sum':
                        values = [float(row.get(col, 0)) for row in group_data if row.get(col)]
                        result[f'sum_{col}'] = sum(values)
                    elif operation == 'count':
                        result[f'count_{col}'] = len(group_data)
                    elif operation == 'avg':
                        values = [float(row.get(col, 0)) for row in group_data if row.get(col)]
                        result[f'avg_{col}'] = sum(values) / len(values) if values else 0
                results.append(result)
            
            # Sort
            if sort_by:
                results.sort(key=lambda x: x.get(sort_by, 0), reverse=(sort_order == 'desc'))
            
            # Limit
            if limit:
                results = results[:limit]
            
            return results
        else:
            # No grouping - check if we have aggregations
            if aggregations:
                # Just aggregations
                result = {}
                for col, operation in aggregations.items():
                    if operation == 'sum':
                        values = [float(row.get(col, 0)) for row in data if row.get(col)]
                        result[f'sum_{col}'] = sum(values)
                    elif operation == 'count':
                        result[f'count_{col}'] = len(data)
                    elif operation == 'avg':
                        values = [float(row.get(col, 0)) for row in data if row.get(col)]
                        result[f'avg_{col}'] = sum(values) / len(values) if values else 0
                return [result] if result else []
            else:
                # No grouping, no aggregations - return raw data
                return data
    
    def _generate_insights(self, question, query_params, results):
        """Generate human-readable insights from query results."""
        if not results or isinstance(results, dict) and 'error' in results:
            return ["No data found for this query"]
        
        insights = []
        intent = query_params.get('intent', 'Analysis')
        
        # Handle raw data results (no aggregations, no grouping)
        if isinstance(results, list) and len(results) > 0 and isinstance(results[0], dict) and 'order_id' in results[0]:
            # This is raw order data
            insights.append(f"Found {len(results)} orders matching the criteria")
            if len(results) <= 5:
                insights.append("All orders:")
                for i, order in enumerate(results, 1):
                    order_id = order.get('order_id', 'N/A')
                    city = order.get('city', 'N/A')
                    status = order.get('status', 'N/A')
                    failure_reason = order.get('failure_reason', 'N/A')
                    insights.append(f"  {i}. Order {order_id}: {city} - {status} ({failure_reason})")
            else:
                insights.append("First 5 orders:")
                for i, order in enumerate(results[:5], 1):
                    order_id = order.get('order_id', 'N/A')
                    city = order.get('city', 'N/A')
                    status = order.get('status', 'N/A')
                    failure_reason = order.get('failure_reason', 'N/A')
                    insights.append(f"  {i}. Order {order_id}: {city} - {status} ({failure_reason})")
                insights.append(f"  ... and {len(results) - 5} more orders")
            return insights
        
        # Handle grouped results (like city rankings, client rankings)
        if isinstance(results, list) and len(results) > 0 and isinstance(results[0], dict):
            # Check if this is a comparison query (has both city and failure_reason)
            if 'city' in results[0] and 'failure_reason' in results[0]:
                # Comparison insights
                insights.append("Comparison Results:")
                
                # Group by city for comparison
                city_data = {}
                for result in results:
                    city = result['city']
                    if city not in city_data:
                        city_data[city] = []
                    city_data[city].append(result)
                
                # Show comparison for each city
                for city, city_results in city_data.items():
                    insights.append(f"\n{city}:")
                    for result in city_results[:3]:  # Top 3 failure reasons per city
                        failure_reason = result['failure_reason']
                        count = result['count_order_id']
                        insights.append(f"  • {failure_reason}: {count} failures")
            
            elif 'city' in results[0]:
                # City-based insights
                if 'sum_amount' in results[0]:
                    insights.append(f"City with highest sales: {results[0]['city']} (₹{results[0]['sum_amount']:,.2f})")
                if 'count_order_id' in results[0]:
                    insights.append(f"City with most orders: {results[0]['city']} ({results[0]['count_order_id']} orders)")
            
            elif 'client_id' in results[0]:
                # Client-based insights
                if 'count_order_id' in results[0]:
                    insights.append(f"Top client by orders: Client {results[0]['client_id']} ({results[0]['count_order_id']} orders)")
            
            # General ranking insights (only if not a comparison)
            if len(results) > 1 and not ('city' in results[0] and 'failure_reason' in results[0]):
                insights.append(f"Top {len(results)} results:")
                for i, result in enumerate(results[:3], 1):
                    if 'city' in result:
                        if 'sum_amount' in result:
                            insights.append(f"  {i}. {result['city']}: ₹{result['sum_amount']:,.2f}")
                        elif 'count_order_id' in result:
                            insights.append(f"  {i}. {result['city']}: {result['count_order_id']} orders")
                    elif 'client_id' in result:
                        insights.append(f"  {i}. Client {result['client_id']}: {result['count_order_id']} orders")
        
        # Handle single result (like total counts)
        elif isinstance(results, list) and len(results) == 1:
            result = results[0]
            if 'count_client_id' in result:
                insights.append(f"Total clients: {result['count_client_id']}")
            if 'count_order_id' in result:
                insights.append(f"Total orders: {result['count_order_id']}")
            if 'sum_amount' in result:
                insights.append(f"Total sales: ₹{result['sum_amount']:,.2f}")
        
        # If no specific insights generated, create generic ones
        if not insights:
            insights.append(f"Query executed successfully: {intent}")
            insights.append(f"Found {len(results)} result(s)")
        
        return insights
    
    def _handle_city_comparison(self, params):
        """Handle city comparison analysis."""
        city1 = params.get('city1', 'Chennai')
        city2 = params.get('city2', 'Mumbai')
        time_days = self._get_time_days(params)
        
        print(f"🔍 Comparing {city1} vs {city2} over {time_days} days...")
        result = self.analyzer.compare_city_performance(city1, city2, time_days)
        result["question"] = f"Compare {city1} and {city2}"
        result["llm_params"] = params
        return result
    
    def _handle_client_ranking(self, params):
        """Handle client ranking analysis."""
        count = params.get('count', 3)
        criteria = params.get('criteria', 'success_rate')
        
        print(f"🔍 Analyzing top {count} clients by {criteria}...")
        
        if criteria == 'order_volume':
            result = self._analyze_most_orders_clients(count)
        else:
            result = self._analyze_top_clients(count)
        
        result["question"] = f"Top {count} clients"
        result["llm_params"] = params
        return result
    
    def _handle_client_count(self, params):
        """Handle client count analysis."""
        print("🔍 Analyzing total client count...")
        result = self._analyze_client_count()
        result["question"] = "How many clients in total?"
        result["llm_params"] = params
        return result
    
    def _handle_city_analysis(self, params):
        """Handle city-specific analysis."""
        city = params.get('city1', 'Chennai')
        time_days = self._get_time_days(params)
        
        print(f"🔍 Analyzing {city} delivery performance...")
        result = self.analyzer.analyze_city_delays(city)
        result["question"] = f"Analysis for {city}"
        result["llm_params"] = params
        return result
    
    def _handle_client_analysis(self, params):
        """Handle client-specific analysis."""
        client_name = params.get('client_name', 'Saini LLC')
        time_days = self._get_time_days(params)
        
        print(f"🔍 Analyzing {client_name} performance...")
        result = self.analyzer.analyze_client_failures(client_name, time_days)
        result["question"] = f"Analysis for {client_name}"
        result["llm_params"] = params
        return result
    
    def _handle_warehouse_analysis(self, params):
        """Handle warehouse analysis."""
        warehouse_name = params.get('warehouse_name', 'Warehouse 1')
        
        print(f"🔍 Analyzing {warehouse_name} performance...")
        result = self.analyzer.analyze_warehouse_performance(warehouse_name)
        result["question"] = f"Analysis for {warehouse_name}"
        result["llm_params"] = params
        return result
    
    def _handle_scaling_analysis(self, params):
        """Handle scaling analysis."""
        additional_orders = params.get('additional_orders', 20000)
        
        print(f"🔍 Analyzing scaling risks for {additional_orders} additional orders...")
        result = self.analyzer.assess_scaling_risks(additional_orders, 1)
        result["question"] = f"Scaling analysis for {additional_orders} orders"
        result["llm_params"] = params
        return result
    
    def _handle_festival_analysis(self, params):
        """Handle festival/risk analysis."""
        print("🔍 Analyzing festival period risks...")
        result = self.analyzer.predict_festival_risks(7)
        result["question"] = "Festival period risk analysis"
        result["llm_params"] = params
        return result
    
    def _handle_general_analysis(self, params):
        """Handle general analysis."""
        print("🔍 Performing general failure analysis...")
        result = self._analyze_general_failures()
        result["question"] = "General delivery failure analysis"
        result["llm_params"] = params
        return result
    
    def _get_time_days(self, params):
        """Convert time period to days."""
        time_period = params.get('time_period', 'all_time')
        time_days = params.get('time_days')
        
        if time_days:
            return int(time_days)
        
        time_mapping = {
            'yesterday': 1,
            'last_week': 7,
            'last_month': 30,
            'last_year': 365,
            'all_time': 365
        }
        
        return time_mapping.get(time_period, 30)
    
    # Analysis helper methods (copied from simple_delivery_analyzer or question_analyzer)
    def _analyze_top_clients(self, count=3):
        """Analyze top performing clients."""
        client_stats = {}
        
        for order in self.analyzer.data.get('orders', []):
            client_id = order.get('client_id')
            if not client_id:
                continue
                
            if client_id not in client_stats:
                client_stats[client_id] = {
                    'total_orders': 0,
                    'failed_orders': 0,
                    'successful_orders': 0,
                    'client_name': 'Unknown'
                }
            
            client_stats[client_id]['total_orders'] += 1
            if order.get('status') == 'Failed':
                client_stats[client_id]['failed_orders'] += 1
            else:
                client_stats[client_id]['successful_orders'] += 1
        
        # Get client names
        for client in self.analyzer.data.get('clients', []):
            client_id = client.get('client_id')
            if client_id in client_stats:
                client_stats[client_id]['client_name'] = client.get('client_name', 'Unknown')
        
        # Calculate success rates
        for client_id, stats in client_stats.items():
            if stats['total_orders'] > 0:
                stats['success_rate'] = (stats['successful_orders'] / stats['total_orders']) * 100
                stats['failure_rate'] = (stats['failed_orders'] / stats['total_orders']) * 100
            else:
                stats['success_rate'] = 0
                stats['failure_rate'] = 0
        
        # Sort by success rate
        sorted_clients = sorted(client_stats.items(), 
                              key=lambda x: x[1]['success_rate'], 
                              reverse=True)
        
        top_clients = sorted_clients[:count]
        
        insights = []
        if top_clients:
            insights.append(f"Top {count} clients by success rate:")
            for i, (client_id, stats) in enumerate(top_clients, 1):
                insights.append(f"{i}. {stats['client_name']}: {stats['success_rate']:.1f}% success rate ({stats['total_orders']} orders)")
        
        return {
            "analysis_type": f"Top {count} Clients Analysis",
            "top_clients": [
                {
                    "rank": i,
                    "client_id": client_id,
                    "client_name": stats['client_name'],
                    "total_orders": stats['total_orders'],
                    "successful_orders": stats['successful_orders'],
                    "failed_orders": stats['failed_orders'],
                    "success_rate": stats['success_rate'],
                    "failure_rate": stats['failure_rate']
                }
                for i, (client_id, stats) in enumerate(top_clients, 1)
            ],
            "insights": insights,
            "recommendations": []
        }
    
    def _analyze_most_orders_clients(self, count=5):
        """Analyze clients with most orders."""
        client_stats = {}
        
        for order in self.analyzer.data.get('orders', []):
            client_id = order.get('client_id')
            if not client_id:
                continue
                
            if client_id not in client_stats:
                client_stats[client_id] = {
                    'total_orders': 0,
                    'failed_orders': 0,
                    'successful_orders': 0,
                    'client_name': 'Unknown'
                }
            
            client_stats[client_id]['total_orders'] += 1
            if order.get('status') == 'Failed':
                client_stats[client_id]['failed_orders'] += 1
            else:
                client_stats[client_id]['successful_orders'] += 1
        
        # Get client names
        for client in self.analyzer.data.get('clients', []):
            client_id = client.get('client_id')
            if client_id in client_stats:
                client_stats[client_id]['client_name'] = client.get('client_name', 'Unknown')
        
        # Calculate success rates
        for client_id, stats in client_stats.items():
            if stats['total_orders'] > 0:
                stats['success_rate'] = (stats['successful_orders'] / stats['total_orders']) * 100
                stats['failure_rate'] = (stats['failed_orders'] / stats['total_orders']) * 100
            else:
                stats['success_rate'] = 0
                stats['failure_rate'] = 0
        
        # Sort by total orders
        sorted_clients = sorted(client_stats.items(), 
                              key=lambda x: x[1]['total_orders'], 
                              reverse=True)
        
        top_clients = sorted_clients[:count]
        
        insights = []
        insights.append(f"Clients with most orders:")
        for i, (client_id, stats) in enumerate(top_clients, 1):
            insights.append(f"{i}. {stats['client_name']}: {stats['total_orders']} orders ({stats['success_rate']:.1f}% success rate)")
        
        return {
            "analysis_type": f"Most Orders Clients Analysis",
            "top_clients_by_orders": [
                {
                    "rank": i,
                    "client_id": client_id,
                    "client_name": stats['client_name'],
                    "total_orders": stats['total_orders'],
                    "successful_orders": stats['successful_orders'],
                    "failed_orders": stats['failed_orders'],
                    "success_rate": stats['success_rate'],
                    "failure_rate": stats['failure_rate']
                }
                for i, (client_id, stats) in enumerate(top_clients, 1)
            ],
            "insights": insights,
            "recommendations": []
        }
    
    def _analyze_client_count(self):
        """Analyze total number of clients."""
        total_clients = len(self.analyzer.data.get('clients', []))
        
        # Get client order statistics
        client_order_stats = {}
        for order in self.analyzer.data.get('orders', []):
            client_id = order.get('client_id')
            if client_id:
                client_order_stats[client_id] = client_order_stats.get(client_id, 0) + 1
        
        clients_with_orders = len(client_order_stats)
        clients_without_orders = total_clients - clients_with_orders
        
        insights = []
        insights.append(f"Total clients in system: {total_clients}")
        insights.append(f"Clients with orders: {clients_with_orders}")
        insights.append(f"Clients without orders: {clients_without_orders}")
        
        recommendations = []
        if clients_without_orders > 0:
            recommendations.append("Follow up with clients who haven't placed orders")
            recommendations.append("Review client onboarding process")
        
        return {
            "analysis_type": "Client Count Analysis",
            "total_clients": total_clients,
            "clients_with_orders": clients_with_orders,
            "clients_without_orders": clients_without_orders,
            "insights": insights,
            "recommendations": recommendations
        }
    
    def _analyze_general_failures(self):
        """Analyze general failure patterns."""
        all_orders = self.analyzer.data.get('orders', [])
        failed_orders = [order for order in all_orders if order.get('status') == 'Failed']
        
        # Analyze failure reasons
        failure_reasons = {}
        for order in failed_orders:
            reason = order.get('failure_reason', 'Unknown')
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
        
        # Analyze by city
        city_failures = {}
        for order in failed_orders:
            city = order.get('city', 'Unknown')
            city_failures[city] = city_failures.get(city, 0) + 1
        
        insights = []
        if failure_reasons:
            top_reason = max(failure_reasons.items(), key=lambda x: x[1])[0]
            insights.append(f"Most common failure reason: {top_reason}")
        
        if city_failures:
            top_city = max(city_failures.items(), key=lambda x: x[1])[0]
            insights.append(f"City with most failures: {top_city}")
        
        return {
            "analysis_type": "General Failure Analysis",
            "total_orders": len(all_orders),
            "failed_orders": len(failed_orders),
            "failure_rate": (len(failed_orders)/len(all_orders)*100) if all_orders else 0,
            "failure_reasons": failure_reasons,
            "city_failures": city_failures,
            "insights": insights,
            "recommendations": []
        }
    
    def close(self):
        """Close the analyzer."""
        self.analyzer.close()

def main():
    """Main function for OpenAI-enhanced analysis."""
    print("🚚 OpenAI-Enhanced Delivery Analysis System")
    print("=" * 60)
    print("Using OpenAI API for dynamic data queries")
    print("Type 'quit' to exit, 'help' for examples")
    print()
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API key not found!")
        print("   Please set your API key:")
        print("   Option 1: Set environment variable: set OPENAI_API_KEY=your_key_here")
        print("   Option 2: Edit the code and add your key directly")
        print("   Option 3: Pass key to constructor: LLMEnhancedAnalyzer(openai_api_key='your_key')")
        return
    
    try:
        analyzer = LLMEnhancedAnalyzer()
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    while True:
        question = input("\n❓ Ask a question: ").strip()
        
        if question.lower() == 'quit':
            break
        elif question.lower() == 'help':
            print("\n📋 Question Examples:")
            print("\n📊 Data Queries:")
            print("- Which city has the highest sales?")
            print("- Compare Chennai and Mumbai")
            print("- What are the top 5 clients?")
            print("- How many clients do we have?")
            print("- Which clients have the most orders?")
            print("- What are the worst performing cities?")
            print("\n🧠 Analytical Questions:")
            print("- What will happen if we add 20,000 orders?")
            print("- How should we prepare for peak season?")
            print("- What are the future risks?")
            print("\n🔄 Hybrid Questions:")
            print("- What are likely causes of failures and how should we prepare?")
            print("- What are current failure rates and what can we do about them?")
            continue
        elif not question:
            continue
        
        # Analyze the question
        result = analyzer.ask_question(question)
        
        # Display results
        print(f"\n📊 Analysis Results:")
        print("-" * 40)
        
        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            # Print query details
            if 'query_params' in result:
                print(f"🔍 Query Intent: {result['query_params'].get('intent', 'Unknown')}")
            
            # Handle different question types
            if result.get('type') == 'hybrid':
                print(f"\n💡 Data Analysis:")
                if 'data_results' in result and 'insights' in result['data_results']:
                    for insight in result['data_results']['insights']:
                        print(f"   • {insight}")
                
                print(f"\n🧠 Analytical Insights:")
                if 'analytical_insights' in result:
                    for insight in result['analytical_insights']:
                        print(f"   • {insight}")
                        
            elif result.get('type') == 'analytical':
                print(f"\n🧠 Analytical Insights:")
                if 'insights' in result:
                    for insight in result['insights']:
                        print(f"   • {insight}")
                        
            else:  # data_query
                # Print insights
                if 'insights' in result and result['insights']:
                    print(f"\n💡 Key Insights:")
                    for insight in result['insights']:
                        print(f"   • {insight}")
                
                # Print raw results (for debugging)
                if 'results' in result and result['results']:
                    print(f"\n📈 Raw Data:")
                    for i, row in enumerate(result['results'][:3], 1):
                        print(f"   {i}. {row}")
    
    analyzer.close()
    print("\n👋 Thank you for using the OpenAI-Enhanced Analysis System!")

if __name__ == "__main__":
    main()
