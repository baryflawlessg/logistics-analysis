#!/usr/bin/env python3
"""
Test script for LLM Analyzer
============================

This script tests the connection to Ollama and basic functionality.

Usage:
    python test_llm_analyzer.py
"""

import requests
import json

def test_ollama_connection():
    """Test if Ollama is running and accessible."""
    print("🔍 Testing Ollama connection...")
    
    try:
        # Test basic connection
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running! Found {len(models)} models:")
            for model in models:
                print(f"   • {model.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ Ollama responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running?")
        print("   Try: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return False

def test_llm_generation():
    """Test basic LLM text generation."""
    print("\n🔍 Testing LLM text generation...")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": "Extract the city names from this question: Compare Chennai and Mumbai",
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get('response', '').strip()
            print(f"✅ LLM responded: {llm_response[:100]}...")
            return True
        else:
            print(f"❌ LLM API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing LLM: {e}")
        return False

def test_json_extraction():
    """Test JSON extraction from LLM response."""
    print("\n🔍 Testing JSON extraction...")
    
    prompt = """
Extract parameters from this question: "Compare Chennai and Mumbai"

Return ONLY a JSON object:
{"analysis_type": "city_comparison", "city1": "Chennai", "city2": "Mumbai", "confidence": 0.9}
"""
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get('response', '').strip()
            print(f"✅ LLM response: {llm_response}")
            
            # Try to extract JSON
            import re
            json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                try:
                    params = json.loads(json_str)
                    print(f"✅ Extracted JSON: {params}")
                    return True
                except json.JSONDecodeError as e:
                    print(f"❌ JSON decode error: {e}")
                    return False
            else:
                print("❌ No JSON found in response")
                return False
        else:
            print(f"❌ LLM API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing JSON extraction: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 LLM Analyzer Test Suite")
    print("=" * 40)
    
    # Test 1: Connection
    connection_ok = test_ollama_connection()
    
    if not connection_ok:
        print("\n❌ Cannot proceed without Ollama connection")
        print("Please ensure Ollama is running:")
        print("  1. Install Ollama: https://ollama.ai/")
        print("  2. Start Ollama: ollama serve")
        print("  3. Load a model: ollama run llama2")
        return
    
    # Test 2: Basic generation
    generation_ok = test_llm_generation()
    
    # Test 3: JSON extraction
    json_ok = test_json_extraction()
    
    # Summary
    print("\n📊 Test Results:")
    print(f"   Connection: {'✅' if connection_ok else '❌'}")
    print(f"   Generation: {'✅' if generation_ok else '❌'}")
    print(f"   JSON Extract: {'✅' if json_ok else '❌'}")
    
    if connection_ok and generation_ok and json_ok:
        print("\n🎉 All tests passed! LLM Analyzer is ready to use.")
        print("   Run: python llm_analyzer.py")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
