#!/usr/bin/env python3
"""
Quick LLM Timeout Test
=====================

This script tests if the LLM timeout issue is resolved.
"""

import requests
import json
import time

def test_quick_llm():
    """Test LLM with a very simple prompt."""
    print("🔍 Testing LLM with simple prompt...")
    
    prompt = "Extract city names from: Compare Chennai and Mumbai. Return JSON:"
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get('response', '').strip()
            print(f"✅ Success! Response time: {end_time - start_time:.1f}s")
            print(f"📝 Response: {llm_response[:200]}...")
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout after 30 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_fallback():
    """Test the fallback system."""
    print("\n🔍 Testing fallback system...")
    
    # Import the analyzer
    try:
        from llm_analyzer import LLMEnhancedAnalyzer
        analyzer = LLMEnhancedAnalyzer()
        
        # Test fallback analysis
        result = analyzer._fallback_analysis("Compare Chennai and Mumbai")
        print(f"✅ Fallback result: {result}")
        
        analyzer.close()
        return True
    except Exception as e:
        print(f"❌ Fallback test error: {e}")
        return False

def main():
    """Run timeout tests."""
    print("🧪 LLM Timeout Test")
    print("=" * 30)
    
    # Test 1: Quick LLM test
    llm_ok = test_quick_llm()
    
    # Test 2: Fallback system
    fallback_ok = test_fallback()
    
    print("\n📊 Results:")
    print(f"   LLM Response: {'✅' if llm_ok else '❌'}")
    print(f"   Fallback System: {'✅' if fallback_ok else '❌'}")
    
    if llm_ok:
        print("\n🎉 LLM is working! The timeout issue is resolved.")
    elif fallback_ok:
        print("\n⚠️ LLM has issues, but fallback system works.")
        print("   The system will still function using keyword matching.")
    else:
        print("\n❌ Both LLM and fallback have issues.")

if __name__ == "__main__":
    main()
