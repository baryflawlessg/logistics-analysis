#!/usr/bin/env python3
"""
Test Script for Improved Question Analysis
=========================================

This script tests the specific questions you mentioned.
"""

from question_analyzer import QuestionAnalyzer
import json

def test_specific_questions():
    """Test the specific questions you mentioned."""
    print("🚚 Testing Improved Question Analysis System")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = QuestionAnalyzer()
    
    # Your specific test questions
    test_questions = [
        "currently, what are the top 3 clients?",
        "how many clients in total?",
        "what are the worst 2 clients?",
        "which clients have the most orders?",
        "show me the best performing client"
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
                
                # Display specific results based on analysis type
                if 'top_clients' in result:
                    print(f"🏆 Top Clients:")
                    for client in result['top_clients']:
                        print(f"   {client['rank']}. {client['client_name']}: {client['success_rate']:.1f}% success rate ({client['total_orders']} orders)")
                
                elif 'worst_clients' in result:
                    print(f"⚠️ Worst Clients:")
                    for client in result['worst_clients']:
                        print(f"   {client['rank']}. {client['client_name']}: {client['failure_rate']:.1f}% failure rate ({client['total_orders']} orders)")
                
                elif 'total_clients' in result:
                    print(f"📈 Total Clients: {result['total_clients']}")
                    print(f"📈 Clients with Orders: {result['clients_with_orders']}")
                    print(f"📈 Clients without Orders: {result['clients_without_orders']}")
                
                if 'insights' in result and result['insights']:
                    print(f"💡 Key Insights:")
                    for insight in result['insights'][:3]:
                        print(f"   • {insight}")
                
                if 'recommendations' in result and result['recommendations']:
                    print(f"🎯 Recommendations:")
                    for rec in result['recommendations'][:2]:
                        print(f"   • {rec}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Save all results
    with open('improved_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✅ Test complete! Results saved to improved_test_results.json")
    
    analyzer.close()

if __name__ == "__main__":
    test_specific_questions()
