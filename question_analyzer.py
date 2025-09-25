#!/usr/bin/env python3
"""
Question-Based Delivery Failure Analysis System
==============================================

This system allows you to ask natural language questions about delivery failures
and automatically routes them to the appropriate analysis functions.

Usage:
    python question_analyzer.py

Author: AI Assistant
Date: 2024
"""

from simple_delivery_analyzer import SimpleDeliveryAnalyzer
import json
import re
from datetime import datetime, timedelta

class QuestionAnalyzer:
    """Analyzes natural language questions and routes them to appropriate analysis functions."""
    
    def __init__(self):
        """Initialize the question analyzer."""
        self.analyzer = SimpleDeliveryAnalyzer()
        self.analyzer.load_all_data()
        
        # Question patterns and their corresponding functions
        self.question_patterns = {
            # Client ranking questions
            r'top.*(\d+).*client': self._analyze_top_clients,
            r'best.*(\d+).*client': self._analyze_top_clients,
            r'worst.*(\d+).*client': self._analyze_worst_clients,
            r'how.*many.*client': self._analyze_client_count,
            r'total.*client': self._analyze_client_count,
            r'client.*count': self._analyze_client_count,
            r'which.*client.*most.*order': self._analyze_most_orders_clients,
            r'client.*most.*order': self._analyze_most_orders_clients,
            
            # City-based questions
            r'why.*deliver.*delay.*city.*(\w+)': self._analyze_city_delays,
            r'why.*deliver.*fail.*city.*(\w+)': self._analyze_city_delays,
            r'what.*happen.*deliver.*(\w+)': self._analyze_city_delays,
            
            # Client-based questions
            r'why.*client.*(\w+).*fail': self._analyze_client_failures,
            r'why.*(\w+).*order.*fail': self._analyze_client_failures,
            r'what.*wrong.*client.*(\w+)': self._analyze_client_failures,
            
            # Warehouse-based questions
            r'why.*warehouse.*(\w+).*fail': self._analyze_warehouse_performance,
            r'what.*problem.*warehouse.*(\w+)': self._analyze_warehouse_performance,
            r'explain.*warehouse.*(\w+)': self._analyze_warehouse_performance,
            
            # Time-based questions
            r'why.*deliver.*fail.*yesterday': self._analyze_recent_failures,
            r'what.*happen.*last.*week': self._analyze_recent_failures,
            r'why.*deliver.*fail.*festival': self._analyze_festival_risks,
            r'what.*risk.*holiday': self._analyze_festival_risks,
            
            # Scaling questions
            r'what.*happen.*(\d+).*order': self._analyze_scaling_risks,
            r'risk.*(\d+).*additional': self._analyze_scaling_risks,
            r'what.*expect.*(\d+).*order': self._analyze_scaling_risks,
            
            # General questions
            r'what.*main.*reason.*fail': self._analyze_general_failures,
            r'why.*deliver.*fail': self._analyze_general_failures,
            r'what.*problem.*deliver': self._analyze_general_failures,
        }
    
    def ask_question(self, question):
        """Ask a natural language question and get analysis results."""
        print(f"\n🤔 Question: {question}")
        print("=" * 60)
        
        # Clean and normalize the question
        normalized_question = question.lower().strip()
        
        # Try to match patterns
        for pattern, function in self.question_patterns.items():
            match = re.search(pattern, normalized_question)
            if match:
                try:
                    # Extract parameters from the question
                    params = match.groups()
                    result = function(question, *params)
                    return result
                except Exception as e:
                    return {"error": f"Error processing question: {e}"}
        
        # If no pattern matches, try to understand the question
        return self._understand_question(question)
    
    def _analyze_top_clients(self, question, count):
        """Analyze top performing clients."""
        print(f"🔍 Analyzing top {count} clients...")
        
        # Get all clients and their order statistics
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
        
        # Calculate success rates and sort
        for client_id, stats in client_stats.items():
            if stats['total_orders'] > 0:
                stats['success_rate'] = (stats['successful_orders'] / stats['total_orders']) * 100
                stats['failure_rate'] = (stats['failed_orders'] / stats['total_orders']) * 100
            else:
                stats['success_rate'] = 0
                stats['failure_rate'] = 0
        
        # Sort by success rate (descending)
        sorted_clients = sorted(client_stats.items(), 
                              key=lambda x: x[1]['success_rate'], 
                              reverse=True)
        
        # Get top N clients
        top_count = int(count) if count.isdigit() else 3
        top_clients = sorted_clients[:top_count]
        
        insights = []
        recommendations = []
        
        if top_clients:
            insights.append(f"Top {top_count} clients by success rate:")
            for i, (client_id, stats) in enumerate(top_clients, 1):
                insights.append(f"{i}. {stats['client_name']}: {stats['success_rate']:.1f}% success rate ({stats['total_orders']} orders)")
        
        return {
            "question": question,
            "analysis_type": f"Top {top_count} Clients Analysis",
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
            "recommendations": recommendations
        }
    
    def _analyze_worst_clients(self, question, count):
        """Analyze worst performing clients."""
        print(f"🔍 Analyzing worst {count} clients...")
        
        # Get all clients and their order statistics
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
        
        # Calculate failure rates and sort
        for client_id, stats in client_stats.items():
            if stats['total_orders'] > 0:
                stats['success_rate'] = (stats['successful_orders'] / stats['total_orders']) * 100
                stats['failure_rate'] = (stats['failed_orders'] / stats['total_orders']) * 100
            else:
                stats['success_rate'] = 0
                stats['failure_rate'] = 0
        
        # Sort by failure rate (descending)
        sorted_clients = sorted(client_stats.items(), 
                              key=lambda x: x[1]['failure_rate'], 
                              reverse=True)
        
        # Get worst N clients
        worst_count = int(count) if count.isdigit() else 3
        worst_clients = sorted_clients[:worst_count]
        
        insights = []
        recommendations = []
        
        if worst_clients:
            insights.append(f"Worst {worst_count} clients by failure rate:")
            for i, (client_id, stats) in enumerate(worst_clients, 1):
                insights.append(f"{i}. {stats['client_name']}: {stats['failure_rate']:.1f}% failure rate ({stats['total_orders']} orders)")
        
        return {
            "question": question,
            "analysis_type": f"Worst {worst_count} Clients Analysis",
            "worst_clients": [
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
                for i, (client_id, stats) in enumerate(worst_clients, 1)
            ],
            "insights": insights,
            "recommendations": recommendations
        }
    
    def _analyze_client_count(self, question):
        """Analyze total number of clients."""
        print("🔍 Analyzing total client count...")
        
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
            "question": question,
            "analysis_type": "Client Count Analysis",
            "total_clients": total_clients,
            "clients_with_orders": clients_with_orders,
            "clients_without_orders": clients_without_orders,
            "insights": insights,
            "recommendations": recommendations
        }
    
    def _analyze_most_orders_clients(self, question):
        """Analyze clients with the most orders."""
        print("🔍 Analyzing clients with most orders...")
        
        # Get all clients and their order statistics
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
        
        # Sort by total orders (descending)
        sorted_clients = sorted(client_stats.items(), 
                              key=lambda x: x[1]['total_orders'], 
                              reverse=True)
        
        # Get top 5 clients by order volume
        top_clients = sorted_clients[:5]
        
        insights = []
        insights.append("Clients with most orders:")
        for i, (client_id, stats) in enumerate(top_clients, 1):
            insights.append(f"{i}. {stats['client_name']}: {stats['total_orders']} orders ({stats['success_rate']:.1f}% success rate)")
        
        recommendations = []
        if top_clients:
            top_client = top_clients[0][1]
            recommendations.append(f"Focus on {top_client['client_name']} - they have the highest order volume")
            recommendations.append("Consider dedicated account management for high-volume clients")
        
        return {
            "question": question,
            "analysis_type": "Most Orders Clients Analysis",
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
            "recommendations": recommendations
        }
    
    def _analyze_city_delays(self, question, city):
        """Analyze city-specific delivery delays."""
        print(f"🔍 Analyzing delivery delays for {city}...")
        result = self.analyzer.analyze_city_delays(city)
        result["question"] = question
        return result
    
    def _analyze_client_failures(self, question, client):
        """Analyze client-specific failures."""
        print(f"🔍 Analyzing failures for client: {client}...")
        result = self.analyzer.analyze_client_failures(client, 30)
        result["question"] = question
        return result
    
    def _analyze_warehouse_performance(self, question, warehouse):
        """Analyze warehouse performance."""
        print(f"🔍 Analyzing warehouse performance: {warehouse}...")
        result = self.analyzer.analyze_warehouse_performance(warehouse)
        result["question"] = question
        return result
    
    def _compare_cities(self, question, city1, city2):
        """Compare two cities."""
        print(f"🔍 Comparing performance between {city1} and {city2}...")
        
        # Check if question mentions time period
        question_lower = question.lower()
        days = 30  # default
        
        if 'last month' in question_lower:
            days = 30
        elif 'last week' in question_lower:
            days = 7
        elif 'last year' in question_lower:
            days = 365
        elif 'yesterday' in question_lower:
            days = 1
        
        result = self.analyzer.compare_city_performance(city1, city2, days)
        result["question"] = question
        result["time_period"] = f"Last {days} days"
        return result
    
    def _analyze_recent_failures(self, question):
        """Analyze recent failures."""
        print("🔍 Analyzing recent delivery failures...")
        
        # Get recent orders (last 7 days)
        recent_orders = []
        cutoff_date = datetime.now() - timedelta(days=7)
        
        for order in self.analyzer.data.get('orders', []):
            try:
                order_date = datetime.strptime(order.get('order_date', ''), '%Y-%m-%d %H:%M:%S')
                if order_date >= cutoff_date:
                    recent_orders.append(order)
            except:
                continue
        
        failed_orders = [order for order in recent_orders if order.get('status') == 'Failed']
        
        # Analyze failure reasons
        failure_reasons = {}
        for order in failed_orders:
            reason = order.get('failure_reason', 'Unknown')
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
        
        insights = []
        if failed_orders:
            insights.append(f"Recent failure rate: {len(failed_orders)/len(recent_orders)*100:.1f}%")
            if failure_reasons:
                top_reason = max(failure_reasons.items(), key=lambda x: x[1])[0]
                insights.append(f"Most common reason: {top_reason}")
        
        return {
            "question": question,
            "analysis_type": "Recent Failures Analysis",
            "total_recent_orders": len(recent_orders),
            "failed_orders": len(failed_orders),
            "failure_rate": (len(failed_orders)/len(recent_orders)*100) if recent_orders else 0,
            "failure_reasons": failure_reasons,
            "insights": insights,
            "recommendations": self._generate_recommendations(insights)
        }
    
    def _analyze_festival_risks(self, question):
        """Analyze festival/holiday risks."""
        print("🔍 Analyzing festival period risks...")
        result = self.analyzer.predict_festival_risks(7)
        result["question"] = question
        return result
    
    def _analyze_scaling_risks(self, question, order_count):
        """Analyze scaling risks."""
        print(f"🔍 Analyzing scaling risks for {order_count} additional orders...")
        result = self.analyzer.assess_scaling_risks(int(order_count), 1)
        result["question"] = question
        return result
    
    def _analyze_general_failures(self, question):
        """Analyze general failure patterns."""
        print("🔍 Analyzing general delivery failure patterns...")
        
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
            "question": question,
            "analysis_type": "General Failure Analysis",
            "total_orders": len(all_orders),
            "failed_orders": len(failed_orders),
            "failure_rate": (len(failed_orders)/len(all_orders)*100) if all_orders else 0,
            "failure_reasons": failure_reasons,
            "city_failures": city_failures,
            "insights": insights,
            "recommendations": self._generate_recommendations(insights)
        }
    
    def _understand_question(self, question):
        """Try to understand questions that don't match patterns."""
        print("🤔 Trying to understand your question...")
        
        # Extract key terms
        question_lower = question.lower()
        
        # Look for client ranking questions
        if any(word in question_lower for word in ['top', 'best', 'worst']) and 'client' in question_lower:
            numbers = re.findall(r'\d+', question)
            count = numbers[0] if numbers else '3'
            if 'worst' in question_lower:
                return self._analyze_worst_clients(question, count)
            else:
                return self._analyze_top_clients(question, count)
        
        # Look for client count questions
        if any(phrase in question_lower for phrase in ['how many client', 'total client', 'client count', 'number of client']):
            return self._analyze_client_count(question)
        
        # Look for city names
        cities = ['chennai', 'mumbai', 'delhi', 'bangalore', 'pune', 'ahmedabad', 'surat', 'coimbatore']
        found_cities = [city for city in cities if city in question_lower]
        
        # Handle city comparison questions
        if 'compare' in question_lower and len(found_cities) >= 2:
            return self._compare_cities(question, found_cities[0], found_cities[1])
        
        # Handle city comparison with better extraction
        if 'compare' in question_lower:
            # Try to extract city names more carefully
            city_patterns = [
                r'between\s+(\w+)\s+and\s+(\w+)',
                r'(\w+)\s+and\s+(\w+)',
                r'(\w+)\s+vs\s+(\w+)',
                r'(\w+)\s+versus\s+(\w+)'
            ]
            
            for pattern in city_patterns:
                match = re.search(pattern, question_lower)
                if match:
                    city1_candidate = match.group(1)
                    city2_candidate = match.group(2)
                    
                    # Check if candidates are in our city list
                    if city1_candidate in cities and city2_candidate in cities:
                        return self._compare_cities(question, city1_candidate, city2_candidate)
        
        # Look for client names
        clients = ['saini', 'mann', 'zacharia']
        found_clients = [client for client in clients if client in question_lower]
        
        # Look for warehouse names
        warehouses = ['warehouse']
        found_warehouses = [warehouse for warehouse in warehouses if warehouse in question_lower]
        
        # Look for time references
        time_refs = ['yesterday', 'last week', 'month', 'festival', 'holiday']
        found_time = [time for time in time_refs if time in question_lower]
        
        # Look for numbers (scaling)
        numbers = re.findall(r'\d+', question)
        
        # Route based on what we found
        if found_cities:
            return self._analyze_city_delays(question, found_cities[0])
        elif found_clients:
            return self._analyze_client_failures(question, found_clients[0])
        elif found_warehouses:
            return self._analyze_warehouse_performance(question, "Warehouse 1")
        elif found_time:
            return self._analyze_recent_failures(question)
        elif numbers:
            return self._analyze_scaling_risks(question, numbers[0])
        else:
            return self._analyze_general_failures(question)
    
    def _generate_recommendations(self, insights):
        """Generate recommendations based on insights."""
        recommendations = []
        
        for insight in insights:
            if 'stockout' in insight.lower():
                recommendations.append("Implement real-time inventory tracking")
            elif 'traffic' in insight.lower():
                recommendations.append("Deploy dynamic routing software")
            elif 'warehouse' in insight.lower():
                recommendations.append("Optimize warehouse operations")
            elif 'weather' in insight.lower():
                recommendations.append("Develop weather contingency plans")
            elif 'address' in insight.lower():
                recommendations.append("Implement address verification system")
        
        return recommendations
    
    def save_question_results(self, results, filename):
        """Save question results to a file."""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"📄 Results saved to: {filename}")
    
    def close(self):
        """Close the analyzer."""
        self.analyzer.close()

def main():
    """Main function for question-based analysis."""
    print("🚚 Question-Based Delivery Failure Analysis System")
    print("=" * 60)
    print("Ask natural language questions about delivery failures!")
    print("Type 'quit' to exit, 'help' for examples, 'list' for sample questions")
    print()
    
    analyzer = QuestionAnalyzer()
    
    # Sample questions file
    sample_questions = [
        "Why were deliveries delayed in Chennai yesterday?",
        "Why did Saini LLC's orders fail in the past week?",
        "What are the main reasons for delivery failures?",
        "Compare delivery performance between Chennai and Pune",
        "What risks should we expect with 20000 additional orders?",
        "Why do deliveries fail more often on weekends?",
        "What's the problem with Warehouse 1?",
        "How does weather affect deliveries?",
        "Which city has the highest failure rate?",
        "What happens during festival periods?"
    ]
    
    while True:
        question = input("\n❓ Ask a question: ").strip()
        
        if question.lower() == 'quit':
            break
        elif question.lower() == 'help':
            print("\n📋 Question Examples:")
            print("- Why were deliveries delayed in [city] yesterday?")
            print("- Why did [client]'s orders fail in the past week?")
            print("- What are the main reasons for delivery failures?")
            print("- Compare delivery performance between [city1] and [city2]")
            print("- What risks should we expect with [number] additional orders?")
            print("- What's the problem with [warehouse]?")
            continue
        elif question.lower() == 'list':
            print("\n📋 Sample Questions:")
            for i, q in enumerate(sample_questions, 1):
                print(f"   {i}. {q}")
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
            # Print key metrics
            if 'total_orders' in result:
                print(f"📈 Total Orders: {result['total_orders']}")
            if 'failed_orders' in result:
                print(f"📈 Failed Orders: {result['failed_orders']}")
            if 'failure_rate' in result:
                print(f"📈 Failure Rate: {result['failure_rate']:.1f}%")
            
            # Print insights
            if 'insights' in result and result['insights']:
                print(f"\n💡 Key Insights:")
                for i, insight in enumerate(result['insights'][:3], 1):
                    print(f"   {i}. {insight}")
            
            # Print recommendations
            if 'recommendations' in result and result['recommendations']:
                print(f"\n🎯 Recommendations:")
                for i, rec in enumerate(result['recommendations'][:3], 1):
                    print(f"   {i}. {rec}")
            
            # Save results
            filename = f"question_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            analyzer.save_question_results(result, filename)
    
    analyzer.close()
    print("\n👋 Thank you for using the Question-Based Analysis System!")

if __name__ == "__main__":
    main()
