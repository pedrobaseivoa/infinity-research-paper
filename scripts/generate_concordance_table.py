#!/usr/bin/env python3
"""
🔍 CONCORDANCE TABLE GENERATOR - Infinity Research Paper
========================================================

Generates the Concordance Performance table comparing Claude 3.5 Sonnet vs DeepSeek V3
analysis results against manual gold-standard across 152 field comparisons.

Input: analysis_claude.json + analysis_deepseek.json
Output: concordance_table.txt + summary statistics
"""

import json
import os
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

def extract_classifications_from_analysis(file_path: str) -> List[str]:
    """
    Extract all classification codes from analysis file
    Returns list of classification codes (A, B, C, D, E, F)
    """
    classifications = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for article in data:
        for field_name, field_data in article['fields'].items():
            analysis = field_data.get('analysis', {})
            
            # Handle multi-part fields (like Author, Year, Study Type)
            if 'author_classification' in analysis:
                # Multi-part field
                for key in analysis:
                    if key.endswith('_classification'):
                        classifications.append(analysis[key])
            elif 'classification' in analysis:
                # Single classification field
                classifications.append(analysis['classification'])
    
    return classifications

def count_concordance_categories(classifications: List[str]) -> Dict[str, int]:
    """
    Count occurrences of each concordance category
    """
    counter = Counter(classifications)
    
    # Ensure all categories are present with 0 if missing
    categories = ['A', 'B', 'C', 'D', 'E', 'F']
    result = {}
    for cat in categories:
        result[cat] = counter.get(cat, 0)
    
    return result

def calculate_percentages(counts: Dict[str, int], total: int) -> Dict[str, float]:
    """
    Calculate percentages for each category
    """
    percentages = {}
    for category, count in counts.items():
        percentages[category] = (count / total * 100) if total > 0 else 0
    return percentages

def generate_concordance_table(claude_counts: Dict[str, int], deepseek_counts: Dict[str, int]) -> str:
    """
    Generate the concordance performance table
    """
    claude_total = sum(claude_counts.values())
    deepseek_total = sum(deepseek_counts.values())
    
    claude_pct = calculate_percentages(claude_counts, claude_total)
    deepseek_pct = calculate_percentages(deepseek_counts, deepseek_total)
    
    # Calculate concordance groups
    claude_strong = claude_counts['A'] + claude_counts['B']
    claude_general = claude_counts['A'] + claude_counts['B'] + claude_counts['C']
    
    deepseek_strong = deepseek_counts['A'] + deepseek_counts['B']
    deepseek_general = deepseek_counts['A'] + deepseek_counts['B'] + deepseek_counts['C']
    
    claude_strong_pct = (claude_strong / claude_total * 100) if claude_total > 0 else 0
    claude_general_pct = (claude_general / claude_total * 100) if claude_total > 0 else 0
    
    deepseek_strong_pct = (deepseek_strong / deepseek_total * 100) if deepseek_total > 0 else 0
    deepseek_general_pct = (deepseek_general / deepseek_total * 100) if deepseek_total > 0 else 0
    
    # Generate table
    table = f"""4.5 Concordance Performance

| Concordance Category                        | Claude 3.5 Sonnet     | DeepSeek V3           |
|---------------------------------------------|------------------------|-----------------------|
| Category A (Equivalent)                     | {claude_counts['A']:2d} ({claude_pct['A']:4.1f}%)        | {deepseek_counts['A']:2d} ({deepseek_pct['A']:4.1f}%)       |
| Category B (Concordant with Detail)        | {claude_counts['B']:2d} ({claude_pct['B']:4.1f}%)        | {deepseek_counts['B']:2d} ({deepseek_pct['B']:4.1f}%)       |
| Category C (Concordant with gaps in non-critical) | {claude_counts['C']:2d} ({claude_pct['C']:4.1f}%)        | {deepseek_counts['C']:2d} ({deepseek_pct['C']:4.1f}%)        |
| Category D (Factually Divergent)           | {claude_counts['D']:2d} ({claude_pct['D']:4.1f}%)         | {deepseek_counts['D']:2d} ({deepseek_pct['D']:4.1f}%)        |
| Category E (Conceptually Different)        | {claude_counts['E']:2d} ({claude_pct['E']:4.1f}%)         | {deepseek_counts['E']:2d} ({deepseek_pct['E']:4.1f}%)        |
| Category F (Incomparable)                  | {claude_counts['F']:2d} ({claude_pct['F']:4.1f}%)         | {deepseek_counts['F']:2d} ({deepseek_pct['F']:4.1f}%)        |
| **Strong Concordance (A+B)**               | **{claude_strong:3d} ({claude_strong_pct:4.1f}%)**    | **{deepseek_strong:3d} ({deepseek_strong_pct:4.1f}%)**   |
| **General Concordance (A+B+C)**            | **{claude_general:3d} ({claude_general_pct:4.1f}%)**    | **{deepseek_general:3d} ({deepseek_general_pct:4.1f}%)**   |

Automated extraction accuracy was evaluated through a structured comparison between
machine-generated outputs and manually curated gold-standard data across cross
comparisons ({claude_total} articles × 8 scientific fields). Each extraction was assessed using a six-level
concordance classification, revealing nuanced patterns of agreement and conflict. Strong
Concordance (Categories A + B) was observed in {claude_strong} cases ({claude_strong_pct:.1f}%) for Claude and {deepseek_strong}
cases ({deepseek_strong_pct:.1f}%) for DeepSeek, where automated outputs either matched or preserved or
preserved all core content while adding beneficial details. General Concordance (A + B + C),
which also includes core manual information present with gaps in non-critical details"""
    
    return table

def main():
    """
    Main function to generate concordance table
    """
    print("🔍 INFINITY RESEARCH - Concordance Table Generator")
    print("=" * 60)
    
    # File paths
    claude_file = "analysis/analysis_claude.json"
    deepseek_file = "analysis/analysis_deepseek.json"
    
    if not os.path.exists(claude_file):
        print(f"❌ Error: {claude_file} not found!")
        return
        
    if not os.path.exists(deepseek_file):
        print(f"❌ Error: {deepseek_file} not found!")
        return
    
    print("📊 Extracting classification data...")
    
    # Extract classifications
    claude_classifications = extract_classifications_from_analysis(claude_file)
    deepseek_classifications = extract_classifications_from_analysis(deepseek_file)
    
    print(f"   Claude classifications: {len(claude_classifications)} fields")
    print(f"   DeepSeek classifications: {len(deepseek_classifications)} fields")
    
    # Count categories
    claude_counts = count_concordance_categories(claude_classifications)
    deepseek_counts = count_concordance_categories(deepseek_classifications)
    
    print(f"\n📈 CONCORDANCE ANALYSIS RESULTS:")
    print("=" * 50)
    
    # Display detailed counts
    print("🎯 Claude 3.5 Sonnet:")
    for category, count in claude_counts.items():
        total = sum(claude_counts.values())
        pct = (count / total * 100) if total > 0 else 0
        print(f"   Category {category}: {count:2d} ({pct:4.1f}%)")
    
    print("\n🎯 DeepSeek V3:")
    for category, count in deepseek_counts.items():
        total = sum(deepseek_counts.values())
        pct = (count / total * 100) if total > 0 else 0
        print(f"   Category {category}: {count:2d} ({pct:4.1f}%)")
    
    # Generate table
    print(f"\n📝 Generating concordance table...")
    table_content = generate_concordance_table(claude_counts, deepseek_counts)
    
    # Save table
    output_file = "plots/concordance_table.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(table_content)
    
    print(f"   ✅ Table saved: {output_file}")
    
    # Display summary
    claude_total = sum(claude_counts.values())
    deepseek_total = sum(deepseek_counts.values())
    
    claude_strong = claude_counts['A'] + claude_counts['B']
    deepseek_strong = deepseek_counts['A'] + deepseek_counts['B']
    
    claude_general = claude_counts['A'] + claude_counts['B'] + claude_counts['C']
    deepseek_general = deepseek_counts['A'] + deepseek_counts['B'] + deepseek_counts['C']
    
    print(f"\n🎯 KEY METRICS:")
    print(f"   Total field comparisons: {claude_total} (Claude), {deepseek_total} (DeepSeek)")
    print(f"   Strong Concordance (A+B): {claude_strong}/{claude_total} ({claude_strong/claude_total*100:.1f}%) vs {deepseek_strong}/{deepseek_total} ({deepseek_strong/deepseek_total*100:.1f}%)")
    print(f"   General Concordance (A+B+C): {claude_general}/{claude_total} ({claude_general/claude_total*100:.1f}%) vs {deepseek_general}/{deepseek_total} ({deepseek_general/deepseek_total*100:.1f}%)")
    
    print(f"\n🎯 Concordance table generation complete!")
    print(f"   📊 Table: {output_file}")

if __name__ == "__main__":
    main()