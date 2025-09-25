# LLM-Enhanced Delivery Analysis Setup Guide

## 🚀 Quick Start

### 1. Install Python Dependencies
```bash
pip install requests
```

### 2. Verify Ollama is Running
```bash
# Test connection
python test_llm_analyzer.py
```

### 3. Run the LLM Analyzer
```bash
python llm_analyzer.py
```

## 🔧 Detailed Setup

### Prerequisites
- ✅ Python 3.7+
- ✅ Ollama installed and running
- ✅ A model loaded (e.g., llama2, mistral)

### Ollama Setup (if not already done)

1. **Install Ollama**
   - Download from: https://ollama.ai/
   - Follow installation instructions for Windows

2. **Start Ollama Service**
   ```bash
   ollama serve
   ```

3. **Load a Model**
   ```bash
   # Load llama2 (recommended)
   ollama run llama2
   
   # Or load mistral (alternative)
   ollama run mistral
   ```

### Testing the Setup

1. **Test Ollama Connection**
   ```bash
   python test_llm_analyzer.py
   ```
   
   Expected output:
   ```
   ✅ Ollama is running! Found X models:
      • llama2
   ✅ LLM responded: ...
   ✅ Extracted JSON: {...}
   🎉 All tests passed! LLM Analyzer is ready to use.
   ```

2. **Run the Main System**
   ```bash
   python llm_analyzer.py
   ```

## 📝 Usage Examples

### Sample Questions You Can Ask:

1. **Client Analysis**
   - "What are the top 5 clients?"
   - "How many clients do we have?"
   - "Which clients have the most orders?"

2. **City Comparison**
   - "Compare delivery performance between Chennai and Mumbai"
   - "Why did deliveries fail in Delhi last month?"

3. **General Analysis**
   - "What are the main reasons for delivery failures?"
   - "What risks should we expect with 20000 additional orders?"

### Interactive Commands:
- Type your question and press Enter
- Type `help` for more examples
- Type `quit` to exit

## 🔍 How It Works

1. **Question Processing**: Your natural language question is sent to Ollama
2. **Parameter Extraction**: LLM extracts structured parameters (cities, counts, etc.)
3. **Analysis Routing**: System routes to appropriate analysis function
4. **Results Display**: Human-readable insights and recommendations

## 🛠️ Troubleshooting

### Common Issues:

1. **"Cannot connect to Ollama"**
   - Ensure Ollama is running: `ollama serve`
   - Check if port 11434 is accessible

2. **"Model not found"**
   - Load a model: `ollama run llama2`
   - List available models: `ollama list`

3. **"JSON extraction failed"**
   - Try a different model: `ollama run mistral`
   - Check if the model is responding properly

4. **"Analysis failed"**
   - Ensure sample data files are in `sample-files/` directory
   - Check if `simple_delivery_analyzer.py` works independently

### Performance Tips:

1. **Use smaller models** for faster responses:
   ```bash
   ollama run llama2:7b  # Smaller version
   ```

2. **Adjust timeout** in `llm_analyzer.py` if needed:
   ```python
   timeout=30  # Increase if model is slow
   ```

## 📊 Expected Output

When you ask "What are the top 3 clients?", you should see:

```
🤔 Question: What are the top 3 clients?
============================================================
🔍 LLM extracted parameters: {'analysis_type': 'client_ranking', 'count': 3, 'criteria': 'success_rate', 'confidence': 0.8}
🔍 Analyzing top 3 clients by success_rate...

📊 Analysis Results:
----------------------------------------
📈 Total Orders: 10000
📈 Failed Orders: 2004
📈 Failure Rate: 20.0%

💡 Key Insights:
   • Top 3 clients by success rate:
   • 1. Saini LLC: 85.2% success rate (1250 orders)
   • 2. Mann Industries: 82.1% success rate (980 orders)
   • 3. Zacharia Corp: 78.9% success rate (1100 orders)
```

## 🎯 Next Steps

1. **Test with your questions** - Try the sample questions above
2. **Customize analysis** - Modify analysis functions in `llm_analyzer.py`
3. **Add new question types** - Extend the LLM prompt for new analysis types
4. **Scale to full data** - Replace sample files with your full dataset

## 📞 Support

If you encounter issues:
1. Run `python test_llm_analyzer.py` to diagnose problems
2. Check Ollama logs for model-specific issues
3. Verify all sample data files are present
4. Ensure Python dependencies are installed
