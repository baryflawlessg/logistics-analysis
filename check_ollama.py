#!/usr/bin/env python3
"""
Simple Ollama Check for Windows
==============================

This script checks if Ollama is running on Windows.
"""

import requests
import sys

def check_ollama():
    """Check if Ollama is running."""
    print("🔍 Checking if Ollama is running...")
    
    try:
        # Try to connect to Ollama API
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("✅ Ollama is running!")
            print(f"📋 Found {len(models)} models:")
            for model in models:
                print(f"   • {model.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ Ollama responded with error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama")
        print("   Ollama is not running or not accessible")
        return False
    except requests.exceptions.Timeout:
        print("❌ Connection timeout")
        print("   Ollama might be starting up")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function."""
    print("🧪 Ollama Status Check")
    print("=" * 30)
    
    if check_ollama():
        print("\n🎉 Ollama is ready to use!")
        print("   You can run: python llm_analyzer.py")
    else:
        print("\n⚠️ Ollama is not running")
        print("   To start Ollama:")
        print("   1. Open Command Prompt")
        print("   2. Run: ollama serve")
        print("   3. In another window: ollama run llama2")

if __name__ == "__main__":
    main()
