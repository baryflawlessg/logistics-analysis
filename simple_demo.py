#!/usr/bin/env python3
"""
Demo Script for Simple Delivery Failure Analysis System
======================================================

This script demonstrates all 6 sample use cases with the simplified analyzer.
No external dependencies required - uses only Python built-in libraries.

Usage:
    python simple_demo.py

Author: AI Assistant
Date: 2024
"""

from simple_delivery_analyzer import SimpleDeliveryAnalyzer
import json
from datetime import datetime, timedelta

def save_results_to_file(results, filename):
    """Save analysis results to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"📄 Results saved to: {filename}")

def print_analysis_summary(title, results):
    """Print a formatted summary of analysis results."""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")
    
    if 'error' in results:
        print(f"❌ Error: {results['error']}")
        return
    
    # Print key metrics
    key_metrics = ['total_orders', 'failed_orders', 'failure_rate']
    for metric in key_metrics:
        if metric in results:
            if metric == 'failure_rate':
                print(f"📈 {metric.replace('_', ' ').title()}: {results[metric]:.1f}%")
            else:
                print(f"📈 {metric.replace('_', ' ').title()}: {results[metric]}")
    
    # Print insights
    if 'insights' in results and results['insights']:
        print(f"\n💡 Key Insights:")
        for i, insight in enumerate(results['insights'][:3], 1):
            print(f"   {i}. {insight}")
    
    # Print recommendations
    if 'recommendations' in results and results['recommendations']:
        print(f"\n🎯 Recommendations:")
        for i, rec in enumerate(results['recommendations'][:3], 1):
            print(f"   {i}. {rec}")

def run_demo():
    """Run the complete demo with all 6 use cases."""
    print("🚚 Simple Delivery Failure Analysis System - DEMO")
    print("=" * 60)
    print("This demo will run all 6 sample use cases with your data.")
    print("Results will be saved to individual files for review.\n")
    
    # Initialize analyzer
    analyzer = SimpleDeliveryAnalyzer()
    
    # Load data
    print("📂 Loading sample data...")
    if not analyzer.load_all_data():
        print("❌ Failed to load data. Please check your sample-files folder.")
        return
    
    print("✅ Data loaded successfully!\n")
    
    # Use Case 1: City-specific delivery delays
    print("🔍 Use Case 1: Why were deliveries delayed in Chennai yesterday?")
    try:
        result1 = analyzer.analyze_city_delays("Chennai", "2025-08-15")
        print_analysis_summary("Chennai Delivery Delays Analysis", result1)
        save_results_to_file(result1, "use_case_1_chennai_delays.json")
    except Exception as e:
        print(f"❌ Error in Use Case 1: {e}")
    
    # Use Case 2: Client-specific failures
    print("\n🔍 Use Case 2: Why did Saini LLC's orders fail in the past week?")
    try:
        result2 = analyzer.analyze_client_failures("Saini LLC", 7)
        print_analysis_summary("Saini LLC Order Failures Analysis", result2)
        save_results_to_file(result2, "use_case_2_client_failures.json")
    except Exception as e:
        print(f"❌ Error in Use Case 2: {e}")
    
    # Use Case 3: Warehouse performance
    print("\n🔍 Use Case 3: Explain the top reasons for delivery failures linked to Warehouse 1?")
    try:
        result3 = analyzer.analyze_warehouse_performance("Warehouse 1", "2025-08")
        print_analysis_summary("Warehouse 1 Performance Analysis", result3)
        save_results_to_file(result3, "use_case_3_warehouse_performance.json")
    except Exception as e:
        print(f"❌ Error in Use Case 3: {e}")
    
    # Use Case 4: City comparison
    print("\n🔍 Use Case 4: Compare delivery failure causes between Chennai and Pune?")
    try:
        result4 = analyzer.compare_city_performance("Chennai", "Pune", 30)
        print_analysis_summary("Chennai vs Pune Performance Comparison", result4)
        save_results_to_file(result4, "use_case_4_city_comparison.json")
    except Exception as e:
        print(f"❌ Error in Use Case 4: {e}")
    
    # Use Case 5: Festival period risks
    print("\n🔍 Use Case 5: What are the likely causes of delivery failures during festival periods?")
    try:
        result5 = analyzer.predict_festival_risks(7)
        print_analysis_summary("Festival Period Risk Analysis", result5)
        save_results_to_file(result5, "use_case_5_festival_risks.json")
    except Exception as e:
        print(f"❌ Error in Use Case 5: {e}")
    
    # Use Case 6: Scaling risks
    print("\n🔍 Use Case 6: What risks should we expect with 20,000 additional monthly orders?")
    try:
        result6 = analyzer.assess_scaling_risks(20000, 1)
        print_analysis_summary("Scaling Risk Assessment", result6)
        save_results_to_file(result6, "use_case_6_scaling_risks.json")
    except Exception as e:
        print(f"❌ Error in Use Case 6: {e}")
    
    # Close analyzer
    analyzer.close()
    
    print(f"\n{'='*60}")
    print("🎉 DEMO COMPLETE!")
    print(f"{'='*60}")
    print("📁 All results have been saved to JSON files:")
    print("   - use_case_1_chennai_delays.json")
    print("   - use_case_2_client_failures.json")
    print("   - use_case_3_warehouse_performance.json")
    print("   - use_case_4_city_comparison.json")
    print("   - use_case_5_festival_risks.json")
    print("   - use_case_6_scaling_risks.json")
    print("\n💡 Next steps:")
    print("   1. Review the JSON files for detailed results")
    print("   2. Modify the demo script to test different parameters")
    print("   3. Run individual analysis functions for deeper insights")
    print("   4. Replace sample-files with your full dataset when ready")

def run_interactive_demo():
    """Run an interactive demo where user can choose analysis."""
    print("🚚 Interactive Delivery Failure Analysis Demo")
    print("=" * 50)
    
    analyzer = SimpleDeliveryAnalyzer()
    if not analyzer.load_all_data():
        print("❌ Failed to load data.")
        return
    
    while True:
        print("\n📋 Available Analysis Options:")
        print("1. Analyze city delivery delays")
        print("2. Analyze client order failures")
        print("3. Analyze warehouse performance")
        print("4. Compare city performance")
        print("5. Predict festival period risks")
        print("6. Assess scaling risks")
        print("0. Exit")
        
        choice = input("\n🎯 Enter your choice (0-6): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            city = input("Enter city name: ").strip()
            date = input("Enter date (YYYY-MM-DD) or press Enter for all dates: ").strip()
            date = date if date else None
            result = analyzer.analyze_city_delays(city, date)
            print_analysis_summary(f"{city} Delivery Analysis", result)
        elif choice == '2':
            client = input("Enter client name: ").strip()
            days = input("Enter days to look back (default 7): ").strip()
            days = int(days) if days.isdigit() else 7
            result = analyzer.analyze_client_failures(client, days)
            print_analysis_summary(f"{client} Failure Analysis", result)
        elif choice == '3':
            warehouse = input("Enter warehouse name: ").strip()
            month = input("Enter month (YYYY-MM) or press Enter for all: ").strip()
            month = month if month else None
            result = analyzer.analyze_warehouse_performance(warehouse, month)
            print_analysis_summary(f"{warehouse} Performance Analysis", result)
        elif choice == '4':
            city_a = input("Enter first city: ").strip()
            city_b = input("Enter second city: ").strip()
            days = input("Enter days to compare (default 30): ").strip()
            days = int(days) if days.isdigit() else 30
            result = analyzer.compare_city_performance(city_a, city_b, days)
            print_analysis_summary(f"{city_a} vs {city_b} Comparison", result)
        elif choice == '5':
            days = input("Enter festival period days (default 7): ").strip()
            days = int(days) if days.isdigit() else 7
            result = analyzer.predict_festival_risks(days)
            print_analysis_summary("Festival Risk Analysis", result)
        elif choice == '6':
            orders = input("Enter additional monthly orders (default 20000): ").strip()
            orders = int(orders) if orders.isdigit() else 20000
            months = input("Enter analysis period months (default 1): ").strip()
            months = int(months) if months.isdigit() else 1
            result = analyzer.assess_scaling_risks(orders, months)
            print_analysis_summary("Scaling Risk Analysis", result)
        else:
            print("❌ Invalid choice. Please try again.")
    
    analyzer.close()
    print("\n👋 Thank you for using the Delivery Failure Analysis System!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_demo()
    else:
        run_demo()
