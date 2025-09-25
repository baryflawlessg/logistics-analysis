#!/usr/bin/env python3
"""
Batch Question Processor for Delivery Failure Analysis
====================================================

This script reads questions from a file and processes them automatically.
Perfect for running multiple questions at once.

Usage:
    python batch_questions.py questions.txt

Author: AI Assistant
Date: 2024
"""

from question_analyzer import QuestionAnalyzer
import json
import sys
from datetime import datetime

def process_questions_from_file(filename):
    """Process questions from a text file."""
    print(f"🚚 Batch Question Processor")
    print("=" * 50)
    print(f"📂 Processing questions from: {filename}")
    print()
    
    # Initialize analyzer
    analyzer = QuestionAnalyzer()
    
    # Read questions from file
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
        return
    
    # Parse questions (lines starting with - or numbered)
    questions = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if line and (line.startswith('- ') or line.startswith(tuple('123456789'))):
            # Remove bullet points and numbering
            question = line.lstrip('- ').lstrip('0123456789. ')
            if question:
                questions.append(question)
    
    if not questions:
        print("❌ No questions found in the file")
        return
    
    print(f"📋 Found {len(questions)} questions to process")
    print()
    
    # Process each question
    results = []
    for i, question in enumerate(questions, 1):
        print(f"🔍 Processing Question {i}/{len(questions)}: {question}")
        print("-" * 60)
        
        try:
            result = analyzer.ask_question(question)
            result["question_number"] = i
            result["question"] = question
            results.append(result)
            
            # Display summary
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
            else:
                if 'failure_rate' in result:
                    print(f"📊 Failure Rate: {result['failure_rate']:.1f}%")
                if 'insights' in result and result['insights']:
                    print(f"💡 Key Insight: {result['insights'][0]}")
                if 'recommendations' in result and result['recommendations']:
                    print(f"🎯 Top Recommendation: {result['recommendations'][0]}")
            
        except Exception as e:
            error_result = {
                "question_number": i,
                "question": question,
                "error": f"Processing error: {e}"
            }
            results.append(error_result)
            print(f"❌ Error processing question: {e}")
        
        print()
    
    # Save all results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"batch_results_{timestamp}.json"
    
    with open(output_filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"✅ Batch processing complete!")
    print(f"📄 All results saved to: {output_filename}")
    
    # Summary statistics
    successful = len([r for r in results if 'error' not in r])
    failed = len([r for r in results if 'error' in r])
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success Rate: {successful/len(results)*100:.1f}%")
    
    analyzer.close()

def create_sample_questions_file():
    """Create a sample questions file if it doesn't exist."""
    filename = "my_questions.txt"
    
    sample_content = """# My Delivery Failure Analysis Questions

## City Analysis
- Why were deliveries delayed in Chennai yesterday?
- What's happening with deliveries in Mumbai?
- Compare delivery performance between Delhi and Bangalore

## Client Analysis  
- Why did Saini LLC's orders fail in the past week?
- What's wrong with Mann Group's deliveries?
- Which client has the most delivery issues?

## Warehouse Analysis
- What's the problem with Warehouse 1?
- Why does Warehouse 2 have so many delays?
- Which warehouse performs best?

## General Analysis
- What are the main reasons for delivery failures?
- Why do deliveries fail more often on weekends?
- What risks should we expect with 20000 additional orders?

## Custom Questions
- How does weather affect delivery performance?
- What's the impact of traffic on deliveries?
- Which drivers perform best?
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print(f"📄 Created sample questions file: {filename}")
    print("   Edit this file to add your own questions")
    print("   Then run: python batch_questions.py my_questions.txt")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("🚚 Batch Question Processor")
        print("=" * 50)
        print("Usage: python batch_questions.py <questions_file>")
        print()
        print("Examples:")
        print("  python batch_questions.py sample_questions.txt")
        print("  python batch_questions.py my_questions.txt")
        print()
        print("To create a sample questions file:")
        print("  python batch_questions.py --create-sample")
        return
    
    if sys.argv[1] == "--create-sample":
        create_sample_questions_file()
        return
    
    filename = sys.argv[1]
    process_questions_from_file(filename)

if __name__ == "__main__":
    main()
