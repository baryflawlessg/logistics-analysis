#!/usr/bin/env python3
"""
Delivery Failure Root Cause Analysis System - Simplified Version
===============================================================

This is a simplified version that works with Python's built-in libraries only.
No external dependencies required.

Author: AI Assistant
Date: 2024
"""

import csv
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import os

class SimpleDeliveryAnalyzer:
    """Simplified delivery failure analyzer using only built-in Python libraries."""
    
    def __init__(self, data_folder="sample-files"):
        """Initialize the analyzer with data folder path."""
        self.data_folder = Path(data_folder)
        self.data = {}
        self.db_path = "delivery_analysis.db"
        self.conn = None
        
    def load_all_data(self):
        """Load all CSV files from the data folder."""
        print("Loading data from CSV files...")
        
        try:
            # Load all data files
            csv_files = [
                'orders.csv', 'fleet_logs.csv', 'warehouse_logs.csv',
                'external_factors.csv', 'feedback.csv', 'clients.csv',
                'drivers.csv', 'warehouses.csv'
            ]
            
            for filename in csv_files:
                filepath = self.data_folder / filename
                if filepath.exists():
                    table_name = filename.replace('.csv', '')
                    self.data[table_name] = self._load_csv(filepath)
                    print(f"✓ Loaded {filename}: {len(self.data[table_name])} records")
                else:
                    print(f"⚠ Warning: {filename} not found")
            
            print(f"✓ Loaded {len(self.data)} datasets successfully")
            
            # Create database for complex queries
            self._create_database()
            
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def _load_csv(self, filepath):
        """Load CSV file and return list of dictionaries."""
        data = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
        return data
    
    def _create_database(self):
        """Create SQLite database for complex queries."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Create tables and insert data
        for table_name, data in self.data.items():
            if not data:
                continue
                
            # Get column names from first row
            columns = list(data[0].keys())
            
            # Create table
            create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} TEXT' for col in columns])})"
            cursor.execute(create_sql)
            
            # Insert data
            for row in data:
                placeholders = ', '.join(['?' for _ in columns])
                values = [row.get(col, '') for col in columns]
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                cursor.execute(insert_sql, values)
        
        self.conn.commit()
        print("✓ Database created successfully")
    
    def analyze_city_delays(self, city, target_date=None):
        """Analyze delivery delays for a specific city."""
        print(f"\n🔍 Analyzing delivery delays for {city}...")
        
        # Filter orders for the city
        city_orders = [order for order in self.data.get('orders', []) 
                      if city.lower() in order.get('city', '').lower()]
        
        if target_date:
            city_orders = [order for order in city_orders 
                          if order.get('order_date', '').startswith(target_date)]
        
        if not city_orders:
            return {"error": f"No orders found for {city} on the specified date"}
        
        # Analyze failure reasons
        failed_orders = [order for order in city_orders if order.get('status') == 'Failed']
        failure_reasons = {}
        for order in failed_orders:
            reason = order.get('failure_reason', 'Unknown')
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
        
        # Correlate with external factors
        external_correlation = self._correlate_external_factors(city_orders)
        
        # Generate insights
        insights = []
        if failed_orders:
            top_reason = max(failure_reasons.items(), key=lambda x: x[1])[0] if failure_reasons else "Unknown"
            insights.append(f"Primary failure reason: {top_reason}")
            
            if top_reason == 'Stockout':
                insights.append("Warehouse inventory management needs improvement")
            elif top_reason == 'Traffic congestion':
                insights.append("Route optimization and traffic-aware scheduling required")
            elif top_reason == 'Warehouse delay':
                insights.append("Warehouse operations efficiency needs attention")
        
        if external_correlation['correlation_found']:
            insights.append("External factors significantly impact delivery performance")
        
        return {
            "city": city,
            "date": target_date,
            "total_orders": len(city_orders),
            "failed_orders": len(failed_orders),
            "failure_rate": (len(failed_orders) / len(city_orders) * 100) if city_orders else 0,
            "failure_reasons": failure_reasons,
            "external_correlation": external_correlation,
            "insights": insights,
            "recommendations": self._generate_recommendations(insights)
        }
    
    def analyze_client_failures(self, client_name, days=7):
        """Analyze failures for a specific client over a time period."""
        print(f"\n🔍 Analyzing failures for client: {client_name}...")
        
        # Find client ID
        client_info = None
        for client in self.data.get('clients', []):
            if client_name.lower() in client.get('client_name', '').lower():
                client_info = client
                break
        
        if not client_info:
            return {"error": f"Client '{client_name}' not found"}
        
        client_id = client_info['client_id']
        
        # Get recent orders for this client
        cutoff_date = datetime.now() - timedelta(days=days)
        client_orders = []
        
        for order in self.data.get('orders', []):
            if order.get('client_id') == client_id:
                try:
                    order_date = datetime.strptime(order.get('order_date', ''), '%Y-%m-%d %H:%M:%S')
                    if order_date >= cutoff_date:
                        client_orders.append(order)
                except:
                    continue
        
        if not client_orders:
            return {"error": f"No orders found for {client_name} in the last {days} days"}
        
        # Analyze patterns
        failed_orders = [order for order in client_orders if order.get('status') == 'Failed']
        failure_patterns = {}
        for order in failed_orders:
            reason = order.get('failure_reason', 'Unknown')
            failure_patterns[reason] = failure_patterns.get(reason, 0) + 1
        
        insights = []
        if failed_orders:
            insights.append(f"Client has {len(failed_orders)} failed orders out of {len(client_orders)} total orders")
            if failure_patterns:
                top_pattern = max(failure_patterns.items(), key=lambda x: x[1])[0]
                insights.append(f"Most common failure reason: {top_pattern}")
        
        return {
            "client_name": client_name,
            "client_id": client_id,
            "analysis_period_days": days,
            "total_orders": len(client_orders),
            "failed_orders": len(failed_orders),
            "failure_rate": (len(failed_orders) / len(client_orders) * 100) if client_orders else 0,
            "failure_patterns": failure_patterns,
            "insights": insights,
            "recommendations": self._generate_recommendations(insights)
        }
    
    def analyze_warehouse_performance(self, warehouse_name, month=None):
        """Analyze delivery failures linked to a specific warehouse."""
        print(f"\n🔍 Analyzing warehouse performance: {warehouse_name}...")
        
        # Find warehouse ID
        warehouse_info = None
        for warehouse in self.data.get('warehouses', []):
            if warehouse_name.lower() in warehouse.get('warehouse_name', '').lower():
                warehouse_info = warehouse
                break
        
        if not warehouse_info:
            return {"error": f"Warehouse '{warehouse_name}' not found"}
        
        warehouse_id = warehouse_info['warehouse_id']
        
        # Get warehouse logs
        warehouse_logs = [log for log in self.data.get('warehouse_logs', [])
                         if log.get('warehouse_id') == warehouse_id]
        
        if not warehouse_logs:
            return {"error": f"No warehouse logs found for {warehouse_name}"}
        
        # Get related orders
        order_ids = [log['order_id'] for log in warehouse_logs]
        related_orders = [order for order in self.data.get('orders', [])
                         if order.get('order_id') in order_ids]
        
        # Analyze performance
        failed_orders = [order for order in related_orders if order.get('status') == 'Failed']
        
        insights = []
        if failed_orders:
            insights.append(f"Warehouse processed {len(warehouse_logs)} orders with {len(failed_orders)} failures")
            failure_rate = len(failed_orders) / len(related_orders) * 100 if related_orders else 0
            insights.append(f"Failure rate: {failure_rate:.1f}%")
        
        return {
            "warehouse_name": warehouse_name,
            "warehouse_id": warehouse_id,
            "analysis_month": month,
            "total_orders_processed": len(warehouse_logs),
            "failed_orders": len(failed_orders),
            "failure_rate": (len(failed_orders) / len(related_orders) * 100) if related_orders else 0,
            "insights": insights,
            "recommendations": self._generate_recommendations(insights)
        }
    
    def compare_city_performance(self, city_a, city_b, days=30):
        """Compare delivery failure causes between two cities."""
        print(f"\n🔍 Comparing performance between {city_a} and {city_b}...")
        
        # Analyze each city
        city_a_analysis = self.analyze_city_delays(city_a)
        city_b_analysis = self.analyze_city_delays(city_b)
        
        if 'error' in city_a_analysis or 'error' in city_b_analysis:
            return {"error": "Insufficient data for comparison"}
        
        # Compare results
        comparison = {
            "city_a_failure_rate": city_a_analysis.get('failure_rate', 0),
            "city_b_failure_rate": city_b_analysis.get('failure_rate', 0),
            "city_a_total_orders": city_a_analysis.get('total_orders', 0),
            "city_b_total_orders": city_b_analysis.get('total_orders', 0)
        }
        
        insights = []
        if comparison["city_a_failure_rate"] > comparison["city_b_failure_rate"]:
            insights.append(f"{city_a} has higher failure rate than {city_b}")
        elif comparison["city_b_failure_rate"] > comparison["city_a_failure_rate"]:
            insights.append(f"{city_b} has higher failure rate than {city_a}")
        else:
            insights.append("Both cities have similar failure rates")
        
        return {
            "city_a": city_a,
            "city_b": city_b,
            "analysis_period_days": days,
            "city_a_analysis": city_a_analysis,
            "city_b_analysis": city_b_analysis,
            "comparison": comparison,
            "insights": insights,
            "recommendations": self._generate_recommendations(insights)
        }
    
    def predict_festival_risks(self, festival_period_days=7):
        """Predict delivery failure risks during festival periods."""
        print(f"\n🔍 Predicting festival period risks...")
        
        # Analyze historical holiday periods
        holiday_orders = []
        holiday_dates = [factor['recorded_at'] for factor in self.data.get('external_factors', [])
                        if factor.get('event_type') == 'Holiday']
        
        for order in self.data.get('orders', []):
            order_date = order.get('order_date', '')[:10]  # Get date part
            for holiday_date in holiday_dates:
                if holiday_date.startswith(order_date):
                    holiday_orders.append(order)
                    break
        
        if not holiday_orders:
            return {"error": "No holiday data available for analysis"}
        
        failed_holiday_orders = [order for order in holiday_orders if order.get('status') == 'Failed']
        
        insights = []
        if failed_holiday_orders:
            holiday_failure_rate = len(failed_holiday_orders) / len(holiday_orders) * 100
            insights.append(f"Historical holiday failure rate: {holiday_failure_rate:.1f}%")
            insights.append("Festival periods show increased delivery challenges")
        
        return {
            "festival_period_days": festival_period_days,
            "historical_holiday_orders": len(holiday_orders),
            "holiday_failure_rate": (len(failed_holiday_orders) / len(holiday_orders) * 100) if holiday_orders else 0,
            "insights": insights,
            "recommendations": self._generate_recommendations(insights)
        }
    
    def assess_scaling_risks(self, additional_orders=20000, months=1):
        """Assess risks when scaling up with additional orders."""
        print(f"\n🔍 Assessing scaling risks for {additional_orders} additional orders...")
        
        # Analyze current capacity
        total_orders = len(self.data.get('orders', []))
        failed_orders = len([order for order in self.data.get('orders', []) if order.get('status') == 'Failed'])
        current_failure_rate = (failed_orders / total_orders * 100) if total_orders else 0
        
        # Calculate scaling impact
        scaling_factor = additional_orders / total_orders if total_orders else 1
        projected_failures = failed_orders * scaling_factor
        
        insights = []
        insights.append(f"Current failure rate: {current_failure_rate:.1f}%")
        insights.append(f"With {additional_orders} additional orders, expect ~{projected_failures:.0f} failures")
        
        if current_failure_rate > 10:
            insights.append("High current failure rate indicates capacity constraints")
        
        return {
            "additional_monthly_orders": additional_orders,
            "analysis_period_months": months,
            "current_total_orders": total_orders,
            "current_failure_rate": current_failure_rate,
            "projected_failures": projected_failures,
            "insights": insights,
            "recommendations": self._generate_scaling_recommendations(insights)
        }
    
    def _correlate_external_factors(self, orders):
        """Correlate orders with external factors."""
        order_ids = [order.get('order_id') for order in orders]
        external_factors = [factor for factor in self.data.get('external_factors', [])
                          if factor.get('order_id') in order_ids]
        
        if not external_factors:
            return {"correlation_found": False, "factors": {}}
        
        weather_conditions = {}
        traffic_conditions = {}
        event_types = {}
        
        for factor in external_factors:
            weather = factor.get('weather_condition', 'Unknown')
            traffic = factor.get('traffic_condition', 'Unknown')
            event = factor.get('event_type', 'Unknown')
            
            weather_conditions[weather] = weather_conditions.get(weather, 0) + 1
            traffic_conditions[traffic] = traffic_conditions.get(traffic, 0) + 1
            event_types[event] = event_types.get(event, 0) + 1
        
        return {
            "correlation_found": True,
            "factors": {
                "weather_conditions": weather_conditions,
                "traffic_conditions": traffic_conditions,
                "event_types": event_types
            },
            "total_correlated_orders": len(external_factors)
        }
    
    def _generate_recommendations(self, insights):
        """Generate actionable recommendations based on insights."""
        recommendations = []
        
        for insight in insights:
            if 'Stockout' in insight:
                recommendations.append("Implement real-time inventory tracking and automated reorder systems")
            elif 'Traffic' in insight:
                recommendations.append("Deploy dynamic routing software with real-time traffic data")
            elif 'Warehouse' in insight:
                recommendations.append("Optimize warehouse layout and implement lean processes")
            elif 'Weather' in insight:
                recommendations.append("Develop weather contingency plans and flexible scheduling")
            elif 'Address' in insight:
                recommendations.append("Implement address verification system and driver training")
        
        return recommendations
    
    def _generate_scaling_recommendations(self, insights):
        """Generate scaling-specific recommendations."""
        recommendations = []
        
        for insight in insights:
            if 'capacity constraints' in insight:
                recommendations.append("Expand warehouse capacity and hire additional drivers")
                recommendations.append("Implement predictive analytics for demand forecasting")
            elif 'failure rate' in insight:
                recommendations.append("Invest in process automation and quality control systems")
                recommendations.append("Develop contingency plans for peak periods")
        
        return recommendations
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")

def main():
    """Main function to demonstrate the analysis system."""
    print("🚚 Delivery Failure Root Cause Analysis System (Simplified)")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = SimpleDeliveryAnalyzer()
    
    # Load data
    if not analyzer.load_all_data():
        print("❌ Failed to load data. Exiting.")
        return
    
    print("\n📊 Sample Analysis Results:")
    print("-" * 30)
    
    # Example 1: Analyze city delays
    try:
        result1 = analyzer.analyze_city_delays("Chennai")
        print(f"\n1. City Analysis - Chennai:")
        print(f"   Total Orders: {result1.get('total_orders', 'N/A')}")
        print(f"   Failed Orders: {result1.get('failed_orders', 'N/A')}")
        print(f"   Failure Rate: {result1.get('failure_rate', 0):.1f}%")
        if 'insights' in result1 and result1['insights']:
            print(f"   Key Insights: {result1['insights'][0]}")
    except Exception as e:
        print(f"   Error in city analysis: {e}")
    
    # Example 2: Analyze client failures
    try:
        result2 = analyzer.analyze_client_failures("Saini LLC", 30)
        print(f"\n2. Client Analysis - Saini LLC:")
        print(f"   Total Orders: {result2.get('total_orders', 'N/A')}")
        print(f"   Failed Orders: {result2.get('failed_orders', 'N/A')}")
        print(f"   Failure Rate: {result2.get('failure_rate', 0):.1f}%")
    except Exception as e:
        print(f"   Error in client analysis: {e}")
    
    # Example 3: Analyze warehouse performance
    try:
        result3 = analyzer.analyze_warehouse_performance("Warehouse 1")
        print(f"\n3. Warehouse Analysis - Warehouse 1:")
        print(f"   Orders Processed: {result3.get('total_orders_processed', 'N/A')}")
        print(f"   Failed Orders: {result3.get('failed_orders', 'N/A')}")
        print(f"   Failure Rate: {result3.get('failure_rate', 0):.1f}%")
    except Exception as e:
        print(f"   Error in warehouse analysis: {e}")
    
    # Close connections
    analyzer.close()
    
    print(f"\n✅ Analysis complete! Database saved as: {analyzer.db_path}")
    print("\n💡 Next steps:")
    print("   1. Review the generated insights")
    print("   2. Run individual analysis functions for detailed results")
    print("   3. Modify parameters to explore different scenarios")

if __name__ == "__main__":
    main()
