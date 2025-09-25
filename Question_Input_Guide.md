# Complete Guide: How to Input Questions to the Delivery Analysis System

## 🎯 **Multiple Ways to Ask Questions**

You now have **4 different ways** to input questions to the system:

### 1. **Interactive Mode** (Type Questions Live)
```bash
python question_analyzer.py
```
- Type questions directly in the terminal
- Get immediate answers
- Perfect for exploring and testing

### 2. **Questions File** (Store Questions in Text File)
```bash
python batch_questions.py sample_questions.txt
```
- Write questions in a text file
- Process multiple questions at once
- Great for batch analysis

### 3. **Programmatic Questions** (Call Functions Directly)
```python
from question_analyzer import QuestionAnalyzer

analyzer = QuestionAnalyzer()
result = analyzer.ask_question("Why were deliveries delayed in Chennai?")
```

### 4. **Direct Function Calls** (Specific Analysis Functions)
```python
from simple_delivery_analyzer import SimpleDeliveryAnalyzer

analyzer = SimpleDeliveryAnalyzer()
analyzer.load_all_data()
result = analyzer.analyze_city_delays("Chennai")
```

## 📝 **How to Store Questions Before Running**

### Option 1: Create a Questions File
Create a text file (e.g., `my_questions.txt`) with your questions:

```
# My Delivery Analysis Questions

## City Analysis
- Why were deliveries delayed in Chennai yesterday?
- What's happening with deliveries in Mumbai?
- Compare delivery performance between Delhi and Bangalore

## Client Analysis  
- Why did Saini LLC's orders fail in the past week?
- What's wrong with Mann Group's deliveries?

## Warehouse Analysis
- What's the problem with Warehouse 1?
- Why does Warehouse 2 have so many delays?

## General Analysis
- What are the main reasons for delivery failures?
- Why do deliveries fail more often on weekends?
- What risks should we expect with 20000 additional orders?
```

Then run:
```bash
python batch_questions.py my_questions.txt
```

### Option 2: Use the Sample Questions File
I've already created `sample_questions.txt` with 50+ example questions. You can:
1. **Use it as-is**: `python batch_questions.py sample_questions.txt`
2. **Edit it**: Add your own questions to the file
3. **Copy sections**: Take relevant questions for your analysis

### Option 3: Interactive Question Input
Run the interactive mode and type questions as you think of them:
```bash
python question_analyzer.py
```

## 🔍 **Question Types the System Understands**

### City-Based Questions
- "Why were deliveries delayed in Chennai yesterday?"
- "What's happening with deliveries in Mumbai?"
- "Compare delivery performance between Delhi and Bangalore"

### Client-Based Questions
- "Why did Saini LLC's orders fail in the past week?"
- "What's wrong with Mann Group's deliveries?"
- "Which client has the most delivery issues?"

### Warehouse-Based Questions
- "What's the problem with Warehouse 1?"
- "Why does Warehouse 2 have so many delays?"
- "Which warehouse performs best?"

### Time-Based Questions
- "Why do deliveries fail more often on weekends?"
- "What happens during festival periods?"
- "Why are Monday deliveries problematic?"

### Operational Questions
- "What are the main reasons for delivery failures?"
- "Why do drivers have trouble finding addresses?"
- "How does traffic congestion affect deliveries?"

### Scaling Questions
- "What risks should we expect with 20,000 additional orders?"
- "How will 50,000 extra orders affect our operations?"
- "What happens if we double our order volume?"

### External Factor Questions
- "How does weather affect delivery performance?"
- "What's the impact of traffic on deliveries?"
- "How do strikes affect our operations?"

## 🚀 **Quick Start Examples**

### Example 1: Ask One Question
```bash
python question_analyzer.py
# Then type: Why were deliveries delayed in Chennai yesterday?
```

### Example 2: Process Multiple Questions
```bash
python batch_questions.py sample_questions.txt
```

### Example 3: Create Your Own Questions File
```bash
# Create my_questions.txt with your questions
python batch_questions.py my_questions.txt
```

### Example 4: Test the System
```bash
python test_questions.py
```

## 📊 **Understanding the Output**

### Question Results Format
```json
{
  "question": "Why were deliveries delayed in Chennai yesterday?",
  "analysis_type": "City Analysis",
  "total_orders": 45,
  "failed_orders": 8,
  "failure_rate": 17.8,
  "insights": [
    "Primary failure reason: Stockout",
    "Warehouse inventory management needs improvement"
  ],
  "recommendations": [
    "Implement real-time inventory tracking",
    "Deploy dynamic routing software"
  ]
}
```

### Key Output Fields
- **question**: The question you asked
- **analysis_type**: Type of analysis performed
- **total_orders**: Number of orders analyzed
- **failed_orders**: Number of failed deliveries
- **failure_rate**: Percentage of failed deliveries
- **insights**: Human-readable explanations
- **recommendations**: Actionable improvement suggestions

## 🎯 **Best Practices for Questions**

### Good Question Examples
- ✅ "Why were deliveries delayed in Chennai yesterday?"
- ✅ "What are the main reasons for delivery failures?"
- ✅ "Compare delivery performance between Mumbai and Delhi"
- ✅ "What risks should we expect with 20000 additional orders?"

### Question Tips
- **Be specific**: Include city names, client names, time periods
- **Use natural language**: The system understands conversational questions
- **Include context**: Mention relevant details (yesterday, last week, etc.)
- **Ask follow-up questions**: Build on previous answers

## 🔧 **Customizing Questions**

### Adding New Question Types
You can extend the system to handle new question types by:

1. **Adding new patterns** to `question_patterns` in `question_analyzer.py`
2. **Creating new analysis functions** for specific question types
3. **Modifying the question understanding logic**

### Example: Adding a New Question Type
```python
# Add to question_patterns in question_analyzer.py
r'what.*cost.*fail': self._analyze_failure_costs,

def _analyze_failure_costs(self, question):
    """Analyze the cost impact of delivery failures."""
    # Your analysis logic here
    return {
        "question": question,
        "analysis_type": "Cost Analysis",
        "insights": ["Cost insights here"],
        "recommendations": ["Cost recommendations here"]
    }
```

## 📁 **File Organization**

### Questions Files
- `sample_questions.txt` - 50+ example questions
- `my_questions.txt` - Your custom questions (create this)
- `batch_results_YYYYMMDD_HHMMSS.json` - Batch processing results

### Question System Files
- `question_analyzer.py` - Main question processing system
- `batch_questions.py` - Batch question processor
- `test_questions.py` - Test script for questions
- `simple_delivery_analyzer.py` - Core analysis engine

## 🎉 **Ready to Use!**

You now have a **complete question-based system** that can:

- ✅ **Understand natural language questions**
- ✅ **Process questions from files**
- ✅ **Handle interactive question input**
- ✅ **Generate human-readable insights**
- ✅ **Provide actionable recommendations**
- ✅ **Save results for further analysis**

**Start asking questions about your delivery failures!** 🚀
