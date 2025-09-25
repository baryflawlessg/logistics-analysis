#!/usr/bin/env python3
"""
Test Script for Question-Based Analysis
======================================

This script demonstrates how to ask questions programmatically.
"""

from question_analyzer import QuestionAnalyzer
import json

def test_questions():
    """Test various questions to demonstrate the system."""
    print("🚚 Testing Question-Based Analysis System")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = QuestionAnalyzer()
    
    # Test questions
    test_questions = [
        "Why were deliveries delayed in Chennai yesterday?",
        "What are the main reasons for delivery failures?",
        "Why did Saini LLC's orders fail in the past week?",
        "What risks should we expect with 20000 additional orders?",
        "Compare delivery performance between Chennai and Pune"
    ]
    
    results = []
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Test Question {i}: {question}")
        print("-" * 50)
        
        try:
            result = analyzer.ask_question(question)
            results.append(result)
            
            # Display results
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"📊 Analysis Type: {result.get('analysis_type', 'General Analysis')}")
                
                if 'total_orders' in result:
                    print(f"📈 Total Orders: {result['total_orders']}")
                if 'failed_orders' in result:
                    print(f"📈 Failed Orders: {result['failed_orders']}")
                if 'failure_rate' in result:
                    print(f"📈 Failure Rate: {result['failure_rate']:.1f}%")
                
                if 'insights' in result and result['insights']:
                    print(f"💡 Key Insights:")
                    for insight in result['insights'][:2]:
                        print(f"   • {insight}")
                
                if 'recommendations' in result and result['recommendations']:
                    print(f"🎯 Recommendations:")
                    for rec in result['recommendations'][:2]:
                        print(f"   • {rec}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Save all results
    with open('test_questions_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✅ Test complete! Results saved to test_questions_results.json")
    
    analyzer.close()

if __name__ == "__main__":
    test_questions()
