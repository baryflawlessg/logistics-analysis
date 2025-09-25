#!/usr/bin/env python3
"""
LLM Readiness Test
==================

This script tests if Ollama LLM is ready and responding properly.
"""

import requests
import json
import time

def test_ollama_connection():
    """Test basic Ollama connection."""
    print("🔍 Testing Ollama connection...")
    
    try:
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
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return False

def test_simple_generation():
    """Test simple text generation."""
    print("\n🔍 Testing simple text generation...")
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": "Say hello",
                "stream": False
            },
            timeout=15
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get('response', '').strip()
            print(f"✅ LLM responded in {end_time - start_time:.1f}s")
            print(f"📝 Response: {llm_response[:100]}...")
            return True
        else:
            print(f"❌ LLM API error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ LLM timeout after 15 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_json_generation():
    """Test JSON generation capability."""
    print("\n🔍 Testing JSON generation...")
    
    prompt = """Return a simple JSON object with city and sales data:

{"city": "Chennai", "sales": 1000}

JSON:"""
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get('response', '').strip()
            print(f"✅ LLM responded in {end_time - start_time:.1f}s")
            print(f"📝 Response: {llm_response}")
            
            # Try to parse JSON
            try:
                import re
                json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    parsed = json.loads(json_str)
                    print(f"✅ JSON parsed successfully: {parsed}")
                    return True
                else:
                    print("❌ No JSON found in response")
                    return False
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error: {e}")
                return False
        else:
            print(f"❌ LLM API error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ LLM timeout after 20 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_query_generation():
    """Test the actual query generation we need."""
    print("\n🔍 Testing query generation...")
    
    prompt = """You are a data analyst. Generate a data query for this question:

Question: "Which city has the highest sales?"

Return JSON:
{"intent": "Find city with highest sales", "table": "orders", "group_by": "city", "aggregations": {"amount": "sum"}, "sort_by": "sum_amount", "sort_order": "desc", "limit": 1}

JSON:"""
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get('response', '').strip()
            print(f"✅ LLM responded in {end_time - start_time:.1f}s")
            print(f"📝 Response: {llm_response}")
            
            # Try to parse JSON
            try:
                import re
                json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    parsed = json.loads(json_str)
                    print(f"✅ Query generated successfully: {parsed}")
                    return True
                else:
                    print("❌ No JSON found in response")
                    return False
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error: {e}")
                return False
        else:
            print(f"❌ LLM API error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ LLM timeout after 25 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all LLM readiness tests."""
    print("🧪 LLM Readiness Test Suite")
    print("=" * 40)
    
    # Test 1: Connection
    connection_ok = test_ollama_connection()
    
    if not connection_ok:
        print("\n❌ Cannot proceed without Ollama connection")
        print("Please ensure Ollama is running:")
        print("  1. ollama serve")
        print("  2. ollama run llama2")
        return
    
    # Test 2: Simple generation
    simple_ok = test_simple_generation()
    
    # Test 3: JSON generation
    json_ok = test_json_generation()
    
    # Test 4: Query generation
    query_ok = test_query_generation()
    
    # Summary
    print("\n📊 Test Results:")
    print(f"   Connection: {'✅' if connection_ok else '❌'}")
    print(f"   Simple Generation: {'✅' if simple_ok else '❌'}")
    print(f"   JSON Generation: {'✅' if json_ok else '❌'}")
    print(f"   Query Generation: {'✅' if query_ok else '❌'}")
    
    if connection_ok and simple_ok and json_ok and query_ok:
        print("\n🎉 LLM is ready! All tests passed.")
        print("   You can now run: python llm_analyzer.py")
    else:
        print("\n⚠️ Some tests failed. LLM may not be ready.")
        print("   Try restarting Ollama or using a different model.")

if __name__ == "__main__":
    main()
