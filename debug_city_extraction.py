#!/usr/bin/env python3
"""
Debug City Extraction
====================

Debug why city names aren't being extracted properly.
"""

import re

def debug_city_extraction():
    """Debug city name extraction."""
    question = "Compare delivery failure causes between Chennai and Mumbai last month?"
    question_lower = question.lower()
    
    print(f"Original question: {question}")
    print(f"Lowercase question: {question_lower}")
    print()
    
    cities = ['chennai', 'mumbai', 'delhi', 'bangalore', 'pune', 'ahmedabad', 'surat', 'coimbatore']
    
    # Method 1: Simple search
    print("Method 1: Simple search")
    found_cities = [city for city in cities if city in question_lower]
    print(f"Found cities: {found_cities}")
    print()
    
    # Method 2: Regex patterns
    print("Method 2: Regex patterns")
    city_patterns = [
        r'between\s+(\w+)\s+and\s+(\w+)',
        r'(\w+)\s+and\s+(\w+)',
        r'(\w+)\s+vs\s+(\w+)',
        r'(\w+)\s+versus\s+(\w+)'
    ]
    
    for i, pattern in enumerate(city_patterns):
        match = re.search(pattern, question_lower)
        if match:
            print(f"Pattern {i+1}: {pattern}")
            print(f"  Match: {match.groups()}")
            city1_candidate = match.group(1)
            city2_candidate = match.group(2)
            print(f"  City1 candidate: {city1_candidate}")
            print(f"  City2 candidate: {city2_candidate}")
            print(f"  City1 in cities: {city1_candidate in cities}")
            print(f"  City2 in cities: {city2_candidate in cities}")
            print()
    
    # Method 3: Direct extraction
    print("Method 3: Direct extraction")
    if 'chennai' in question_lower and 'mumbai' in question_lower:
        print("Found both Chennai and Mumbai in question")
        print("Should return: Chennai vs Mumbai")
    else:
        print("Did not find both cities")

if __name__ == "__main__":
    debug_city_extraction()
