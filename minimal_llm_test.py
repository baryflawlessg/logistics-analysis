#!/usr/bin/env python3
"""
Minimal LLM Test
================

Test if ANY model can respond quickly.
"""

import requests
import time

def test_minimal():
    """Test with absolute minimal prompt."""
    print("🔍 Testing minimal LLM response...")
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral:7b",
                "prompt": "Hello",
                "stream": False
            },
            timeout=15
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get('response', '').strip()
            print(f"✅ LLM responded in {end_time - start_time:.1f}s")
            print(f"📝 Response: {llm_response}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout after 15 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_json_minimal():
    """Test minimal JSON generation."""
    print("\n🔍 Testing minimal JSON...")
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral:7b",
                "prompt": 'Return JSON: {"test": "ok"}',
                "stream": False
            },
            timeout=15
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get('response', '').strip()
            print(f"✅ JSON test completed in {end_time - start_time:.1f}s")
            print(f"📝 Response: {llm_response}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ JSON test timeout after 15 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run minimal tests."""
    print("🧪 Minimal LLM Test")
    print("=" * 30)
    
    # Test 1: Basic response
    basic_ok = test_minimal()
    
    # Test 2: JSON response
    json_ok = test_json_minimal()
    
    print("\n📊 Results:")
    print(f"   Basic Response: {'✅' if basic_ok else '❌'}")
    print(f"   JSON Response: {'✅' if json_ok else '❌'}")
    
    if basic_ok and json_ok:
        print("\n🎉 LLM is working! Try smaller model for faster responses.")
    else:
        print("\n❌ LLM is too slow. Try:")
        print("   ollama run llama2:7b")
        print("   ollama run mistral:7b")

if __name__ == "__main__":
    main()
