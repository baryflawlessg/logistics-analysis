#!/usr/bin/env python3
"""
Delivery Failure Root Cause Analysis System
==========================================

This program analyzes delivery failures by aggregating data from multiple sources:
- Orders data (delivery status, timestamps, failure reasons)
- Fleet logs (driver routes, GPS data, operational notes)
- Warehouse logs (picking, packing, dispatch times)
- External factors (weather, traffic, events)
- Customer feedback (sentiment, complaints, ratings)

Author: AI Assistant
Date: 2024
"""

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class DeliveryFailureAnalyzer:
    """Main class for analyzing delivery failures and generating insights."""
    
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
            self.data['orders'] = pd.read_csv(self.data_folder / 'orders.csv')
            self.data['fleet_logs'] = pd.read_csv(self.data_folder / 'fleet_logs.csv')
            self.data['warehouse_logs'] = pd.read_csv(self.data_folder / 'warehouse_logs.csv')
            self.data['external_factors'] = pd.read_csv(self.data_folder / 'external_factors.csv')
            self.data['feedback'] = pd.read_csv(self.data_folder / 'feedback.csv')
            self.data['clients'] = pd.read_csv(self.data_folder / 'clients.csv')
            self.data['drivers'] = pd.read_csv(self.data_folder / 'drivers.csv')
            self.data['warehouses'] = pd.read_csv(self.data_folder / 'warehouses.csv')
            
            print(f"✓ Loaded {len(self.data)} datasets successfully")
            
            # Convert date columns
            self._convert_date_columns()
            
            # Create database for complex queries
            self._create_database()
            
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def _convert_date_columns(self):
        """Convert string dates to datetime objects."""
        date_columns = {
            'orders': ['order_date', 'promised_delivery_date', 'actual_delivery_date', 'created_at'],
            'fleet_logs': ['departure_time', 'arrival_time', 'created_at'],
            'warehouse_logs': ['picking_start', 'picking_end', 'dispatch_time'],
            'external_factors': ['recorded_at'],
            'feedback': ['created_at'],
            'clients': ['created_at'],
            'drivers': ['created_at'],
            'warehouses': ['created_at']
        }
        
        for table, columns in date_columns.items():
            if table in self.data:
                for col in columns:
                    if col in self.data[table].columns:
                        self.data[table][col] = pd.to_datetime(
                            self.data[table][col], errors='coerce'
                        )
    
    def _create_database(self):
        """Create SQLite database for complex queries."""
        self.conn = sqlite3.connect(self.db_path)
        
        # Store dataframes as tables
        for name, df in self.data.items():
            df.to_sql(name, self.conn, if_exists='replace', index=False)
        
        print("✓ Database created successfully")
    
    def analyze_city_delays(self, city, target_date=None):
        """
        Analyze delivery delays for a specific city.
        
        Args:
            city (str): City name to analyze
            target_date (str): Date to analyze (YYYY-MM-DD format)
        
        Returns:
            dict: Analysis results with insights and recommendations
        """
        print(f"\n🔍 Analyzing delivery delays for {city}...")
        
        # Filter orders for the city
        city_orders = self.data['orders'][
            self.data['orders']['city'].str.contains(city, case=False, na=False)
        ].copy()
        
        if target_date:
            target_dt = pd.to_datetime(target_date)
            city_orders = city_orders[
                city_orders['order_date'].dt.date == target_dt.date()
            ]
        
        if city_orders.empty:
            return {"error": f"No orders found for {city} on the specified date"}
        
        # Analyze failure reasons
        failure_analysis = self._analyze_failure_reasons(city_orders)
        
        # Correlate with external factors
        external_correlation = self._correlate_external_factors(city_orders)
        
        # Analyze warehouse performance
        warehouse_analysis = self._analyze_warehouse_performance(city_orders)
        
        # Analyze fleet performance
        fleet_analysis = self._analyze_fleet_performance(city_orders)
        
        # Generate insights
        insights = self._generate_city_insights(
            city_orders, failure_analysis, external_correlation, 
            warehouse_analysis, fleet_analysis
        )
        
        return {
            "city": city,
            "date": target_date,
            "total_orders": len(city_orders),
            "failed_orders": len(city_orders[city_orders['status'] == 'Failed']),
            "failure_rate": len(city_orders[city_orders['status'] == 'Failed']) / len(city_orders) * 100,
            "failure_analysis": failure_analysis,
            "external_correlation": external_correlation,
            "warehouse_analysis": warehouse_analysis,
            "fleet_analysis": fleet_analysis,
            "insights": insights,
            "recommendations": self._generate_recommendations(insights)
        }
    
    def analyze_client_failures(self, client_name, days=7):
        """
        Analyze failures for a specific client over a time period.
        
        Args:
            client_name (str): Client name to analyze
            days (int): Number of days to look back
        
        Returns:
            dict: Analysis results
        """
        print(f"\n🔍 Analyzing failures for client: {client_name}...")
        
        # Find client ID
        client_info = self.data['clients'][
            self.data['clients']['client_name'].str.contains(client_name, case=False, na=False)
        ]
        
        if client_info.empty:
            return {"error": f"Client '{client_name}' not found"}
        
        client_id = client_info.iloc[0]['client_id']
        
        # Get recent orders for this client
        cutoff_date = datetime.now() - timedelta(days=days)
        client_orders = self.data['orders'][
            (self.data['orders']['client_id'] == client_id) &
            (self.data['orders']['order_date'] >= cutoff_date)
        ].copy()
        
        if client_orders.empty:
            return {"error": f"No orders found for {client_name} in the last {days} days"}
        
        # Analyze patterns
        failure_patterns = self._analyze_client_failure_patterns(client_orders)
        feedback_analysis = self._analyze_client_feedback(client_orders)
        operational_issues = self._analyze_operational_issues(client_orders)
        
        insights = self._generate_client_insights(
            client_name, client_orders, failure_patterns, 
            feedback_analysis, operational_issues
        )
        
        return {
            "client_name": client_name,
            "client_id": client_id,
            "analysis_period_days": days,
            "total_orders": len(client_orders),
            "failed_orders": len(client_orders[client_orders['status'] == 'Failed']),
            "failure_rate": len(client_orders[client_orders['status'] == 'Failed']) / len(client_orders) * 100,
            "failure_patterns": failure_patterns,
            "feedback_analysis": feedback_analysis,
            "operational_issues": operational_issues,
            "insights": insights,
            "recommendations": self._generate_client_recommendations(insights)
        }
    
    def analyze_warehouse_performance(self, warehouse_name, month=None):
        """
        Analyze delivery failures linked to a specific warehouse.
        
        Args:
            warehouse_name (str): Warehouse name to analyze
            month (str): Month to analyze (YYYY-MM format)
        
        Returns:
            dict: Analysis results
        """
        print(f"\n🔍 Analyzing warehouse performance: {warehouse_name}...")
        
        # Find warehouse ID
        warehouse_info = self.data['warehouses'][
            self.data['warehouses']['warehouse_name'].str.contains(warehouse_name, case=False, na=False)
        ]
        
        if warehouse_info.empty:
            return {"error": f"Warehouse '{warehouse_name}' not found"}
        
        warehouse_id = warehouse_info.iloc[0]['warehouse_id']
        
        # Get warehouse logs
        warehouse_logs = self.data['warehouse_logs'][
            self.data['warehouse_logs']['warehouse_id'] == warehouse_id
        ].copy()
        
        if month:
            warehouse_logs = warehouse_logs[
                warehouse_logs['dispatch_time'].dt.to_period('M') == month
            ]
        
        if warehouse_logs.empty:
            return {"error": f"No warehouse logs found for {warehouse_name}"}
        
        # Get related orders
        order_ids = warehouse_logs['order_id'].tolist()
        related_orders = self.data['orders'][
            self.data['orders']['order_id'].isin(order_ids)
        ]
        
        # Analyze warehouse performance
        performance_metrics = self._calculate_warehouse_metrics(warehouse_logs, related_orders)
        delay_analysis = self._analyze_warehouse_delays(warehouse_logs)
        failure_correlation = self._correlate_warehouse_failures(warehouse_logs, related_orders)
        
        insights = self._generate_warehouse_insights(
            warehouse_name, performance_metrics, delay_analysis, failure_correlation
        )
        
        return {
            "warehouse_name": warehouse_name,
            "warehouse_id": warehouse_id,
            "analysis_month": month,
            "total_orders_processed": len(warehouse_logs),
            "performance_metrics": performance_metrics,
            "delay_analysis": delay_analysis,
            "failure_correlation": failure_correlation,
            "insights": insights,
            "recommendations": self._generate_warehouse_recommendations(insights)
        }
    
    def compare_city_performance(self, city_a, city_b, days=30):
        """
        Compare delivery failure causes between two cities.
        
        Args:
            city_a (str): First city name
            city_b (str): Second city name
            days (int): Number of days to analyze
        
        Returns:
            dict: Comparative analysis results
        """
        print(f"\n🔍 Comparing performance between {city_a} and {city_b}...")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Get orders for both cities
        city_a_orders = self.data['orders'][
            (self.data['orders']['city'].str.contains(city_a, case=False, na=False)) &
            (self.data['orders']['order_date'] >= cutoff_date)
        ]
        
        city_b_orders = self.data['orders'][
            (self.data['orders']['city'].str.contains(city_b, case=False, na=False)) &
            (self.data['orders']['order_date'] >= cutoff_date)
        ]
        
        if city_a_orders.empty or city_b_orders.empty:
            return {"error": f"Insufficient data for comparison between {city_a} and {city_b}"}
        
        # Analyze each city
        city_a_analysis = self._analyze_city_performance(city_a_orders, city_a)
        city_b_analysis = self._analyze_city_performance(city_b_orders, city_b)
        
        # Compare results
        comparison = self._compare_city_metrics(city_a_analysis, city_b_analysis)
        
        insights = self._generate_comparison_insights(city_a, city_b, comparison)
        
        return {
            "city_a": city_a,
            "city_b": city_b,
            "analysis_period_days": days,
            "city_a_analysis": city_a_analysis,
            "city_b_analysis": city_b_analysis,
            "comparison": comparison,
            "insights": insights,
            "recommendations": self._generate_comparison_recommendations(insights)
        }
    
    def predict_festival_risks(self, festival_period_days=7):
        """
        Predict delivery failure risks during festival periods.
        
        Args:
            festival_period_days (int): Number of days to analyze for festival impact
        
        Returns:
            dict: Risk prediction results
        """
        print(f"\n🔍 Predicting festival period risks...")
        
        # Analyze historical festival periods (holidays)
        holiday_orders = self.data['orders'][
            self.data['orders']['order_date'].isin(
                self.data['external_factors'][
                    self.data['external_factors']['event_type'] == 'Holiday'
                ]['recorded_at'].dt.date
            )
        ]
        
        if holiday_orders.empty:
            return {"error": "No holiday data available for analysis"}
        
        # Analyze patterns
        holiday_patterns = self._analyze_holiday_patterns(holiday_orders)
        external_factors = self._analyze_festival_external_factors()
        capacity_analysis = self._analyze_festival_capacity()
        
        insights = self._generate_festival_insights(
            holiday_patterns, external_factors, capacity_analysis
        )
        
        return {
            "festival_period_days": festival_period_days,
            "historical_holiday_orders": len(holiday_orders),
            "holiday_patterns": holiday_patterns,
            "external_factors": external_factors,
            "capacity_analysis": capacity_analysis,
            "insights": insights,
            "recommendations": self._generate_festival_recommendations(insights)
        }
    
    def assess_scaling_risks(self, additional_orders=20000, months=1):
        """
        Assess risks when scaling up with additional orders.
        
        Args:
            additional_orders (int): Number of additional monthly orders
            months (int): Time period for analysis
        
        Returns:
            dict: Scaling risk assessment
        """
        print(f"\n🔍 Assessing scaling risks for {additional_orders} additional orders...")
        
        # Analyze current capacity
        current_capacity = self._analyze_current_capacity()
        
        # Identify bottlenecks
        bottlenecks = self._identify_bottlenecks()
        
        # Calculate scaling impact
        scaling_impact = self._calculate_scaling_impact(additional_orders, current_capacity)
        
        # Risk assessment
        risk_factors = self._assess_scaling_risks(additional_orders, bottlenecks)
        
        insights = self._generate_scaling_insights(
            additional_orders, current_capacity, bottlenecks, scaling_impact, risk_factors
        )
        
        return {
            "additional_monthly_orders": additional_orders,
            "analysis_period_months": months,
            "current_capacity": current_capacity,
            "bottlenecks": bottlenecks,
            "scaling_impact": scaling_impact,
            "risk_factors": risk_factors,
            "insights": insights,
            "recommendations": self._generate_scaling_recommendations(insights)
        }
    
    # Helper methods for analysis
    def _analyze_failure_reasons(self, orders):
        """Analyze failure reasons in orders."""
        failed_orders = orders[orders['status'] == 'Failed']
        if failed_orders.empty:
            return {"total_failures": 0, "reasons": {}}
        
        reasons = failed_orders['failure_reason'].value_counts().to_dict()
        return {
            "total_failures": len(failed_orders),
            "reasons": reasons,
            "top_reason": reasons.get(reasons.keys()[0], "Unknown") if reasons else "Unknown"
        }
    
    def _correlate_external_factors(self, orders):
        """Correlate orders with external factors."""
        order_ids = orders['order_id'].tolist()
        external_factors = self.data['external_factors'][
            self.data['external_factors']['order_id'].isin(order_ids)
        ]
        
        if external_factors.empty:
            return {"correlation_found": False, "factors": {}}
        
        factors = {
            "weather_conditions": external_factors['weather_condition'].value_counts().to_dict(),
            "traffic_conditions": external_factors['traffic_condition'].value_counts().to_dict(),
            "event_types": external_factors['event_type'].value_counts().to_dict()
        }
        
        return {
            "correlation_found": True,
            "factors": factors,
            "total_correlated_orders": len(external_factors)
        }
    
    def _analyze_warehouse_performance(self, orders):
        """Analyze warehouse performance for orders."""
        order_ids = orders['order_id'].tolist()
        warehouse_logs = self.data['warehouse_logs'][
            self.data['warehouse_logs']['order_id'].isin(order_ids)
        ]
        
        if warehouse_logs.empty:
            return {"data_available": False}
        
        # Calculate average processing times
        warehouse_logs['processing_time'] = (
            warehouse_logs['dispatch_time'] - warehouse_logs['picking_start']
        ).dt.total_seconds() / 3600  # Convert to hours
        
        avg_processing_time = warehouse_logs['processing_time'].mean()
        
        return {
            "data_available": True,
            "total_orders_processed": len(warehouse_logs),
            "average_processing_time_hours": round(avg_processing_time, 2),
            "delays_due_to_stock": len(warehouse_logs[warehouse_logs['notes'].str.contains('Stock', na=False)]),
            "delays_due_to_packing": len(warehouse_logs[warehouse_logs['notes'].str.contains('packing', na=False)])
        }
    
    def _analyze_fleet_performance(self, orders):
        """Analyze fleet performance for orders."""
        order_ids = orders['order_id'].tolist()
        fleet_logs = self.data['fleet_logs'][
            self.data['fleet_logs']['order_id'].isin(order_ids)
        ]
        
        if fleet_logs.empty:
            return {"data_available": False}
        
        # Calculate delivery times
        fleet_logs['delivery_time'] = (
            fleet_logs['arrival_time'] - fleet_logs['departure_time']
        ).dt.total_seconds() / 3600  # Convert to hours
        
        avg_delivery_time = fleet_logs['delivery_time'].mean()
        
        # Analyze delay notes
        delay_notes = fleet_logs['gps_delay_notes'].value_counts().to_dict()
        
        return {
            "data_available": True,
            "total_deliveries": len(fleet_logs),
            "average_delivery_time_hours": round(avg_delivery_time, 2),
            "delay_notes": delay_notes,
            "address_issues": len(fleet_logs[fleet_logs['gps_delay_notes'].str.contains('Address', na=False)]),
            "traffic_issues": len(fleet_logs[fleet_logs['gps_delay_notes'].str.contains('congestion', na=False)]),
            "breakdowns": len(fleet_logs[fleet_logs['gps_delay_notes'].str.contains('Breakdown', na=False)])
        }
    
    def _generate_city_insights(self, orders, failure_analysis, external_correlation, warehouse_analysis, fleet_analysis):
        """Generate insights for city analysis."""
        insights = []
        
        if failure_analysis['total_failures'] > 0:
            top_reason = failure_analysis['top_reason']
            insights.append(f"Primary failure reason: {top_reason}")
            
            if top_reason == 'Stockout':
                insights.append("Warehouse inventory management needs improvement")
            elif top_reason == 'Traffic congestion':
                insights.append("Route optimization and traffic-aware scheduling required")
            elif top_reason == 'Warehouse delay':
                insights.append("Warehouse operations efficiency needs attention")
        
        if external_correlation['correlation_found']:
            insights.append("External factors significantly impact delivery performance")
            if 'Rain' in str(external_correlation['factors']['weather_conditions']):
                insights.append("Weather conditions (rain) are affecting deliveries")
            if 'Heavy' in str(external_correlation['factors']['traffic_conditions']):
                insights.append("Heavy traffic is causing delivery delays")
        
        if warehouse_analysis.get('data_available'):
            if warehouse_analysis['average_processing_time_hours'] > 2:
                insights.append("Warehouse processing times are above optimal levels")
        
        if fleet_analysis.get('data_available'):
            if fleet_analysis['average_delivery_time_hours'] > 4:
                insights.append("Delivery times are longer than expected")
        
        return insights
    
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
    
    # Additional helper methods would be implemented here...
    # (Truncated for brevity - full implementation would include all helper methods)
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")

def main():
    """Main function to demonstrate the analysis system."""
    print("🚚 Delivery Failure Root Cause Analysis System")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = DeliveryFailureAnalyzer()
    
    # Load data
    if not analyzer.load_all_data():
        print("❌ Failed to load data. Exiting.")
        return
    
    print("\n📊 Sample Analysis Results:")
    print("-" * 30)
    
    # Example 1: Analyze city delays
    try:
        result1 = analyzer.analyze_city_delays("Chennai", "2025-08-15")
        print(f"\n1. City Analysis - Chennai:")
        print(f"   Total Orders: {result1.get('total_orders', 'N/A')}")
        print(f"   Failed Orders: {result1.get('failed_orders', 'N/A')}")
        print(f"   Failure Rate: {result1.get('failure_rate', 0):.1f}%")
        if 'insights' in result1:
            print(f"   Key Insights: {result1['insights'][:2] if result1['insights'] else 'None'}")
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
        if 'performance_metrics' in result3:
            metrics = result3['performance_metrics']
            print(f"   Avg Processing Time: {metrics.get('average_processing_time_hours', 'N/A')} hours")
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
