#!/usr/bin/env python3
"""
Test City Comparison Question
=============================

Test the specific city comparison question that was failing.
"""

from question_analyzer import QuestionAnalyzer
import json

def test_city_comparison():
    """Test the city comparison question."""
    print("🚚 Testing City Comparison Question")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = QuestionAnalyzer()
    
    # Your specific test question
    test_question = "Compare delivery failure causes between Chennai and Mumbai last month?"
    
    print(f"🔍 Test Question: {test_question}")
    print("-" * 50)
    
    try:
        result = analyzer.ask_question(test_question)
        
        # Display results
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"📊 Analysis Type: {result.get('analysis_type', 'General Analysis')}")
            print(f"📅 Time Period: {result.get('time_period', 'Not specified')}")
            
            # Display city comparison results
            if 'city_a_analysis' in result and 'city_b_analysis' in result:
                city_a = result['city_a_analysis']
                city_b = result['city_b_analysis']
                
                print(f"\n🏙️ {result.get('city_a', 'City A')} Analysis:")
                print(f"   Total Orders: {city_a.get('total_orders', 'N/A')}")
                print(f"   Failed Orders: {city_a.get('failed_orders', 'N/A')}")
                print(f"   Failure Rate: {city_a.get('failure_rate', 0):.1f}%")
                
                print(f"\n🏙️ {result.get('city_b', 'City B')} Analysis:")
                print(f"   Total Orders: {city_b.get('total_orders', 'N/A')}")
                print(f"   Failed Orders: {city_b.get('failed_orders', 'N/A')}")
                print(f"   Failure Rate: {city_b.get('failure_rate', 0):.1f}%")
                
                # Display comparison
                if 'comparison' in result:
                    comp = result['comparison']
                    print(f"\n📊 Comparison:")
                    print(f"   {result.get('city_a', 'City A')} Failure Rate: {comp.get('city_a_failure_rate', 0):.1f}%")
                    print(f"   {result.get('city_b', 'City B')} Failure Rate: {comp.get('city_b_failure_rate', 0):.1f}%")
            
            # Display insights
            if 'insights' in result and result['insights']:
                print(f"\n💡 Key Insights:")
                for insight in result['insights']:
                    print(f"   • {insight}")
            
            # Display recommendations
            if 'recommendations' in result and result['recommendations']:
                print(f"\n🎯 Recommendations:")
                for rec in result['recommendations']:
                    print(f"   • {rec}")
        
        # Save result
        with open('city_comparison_test.json', 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"\n📄 Result saved to city_comparison_test.json")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    analyzer.close()

if __name__ == "__main__":
    test_city_comparison()
