#!/usr/bin/env python3
"""
📊 FIELD-BY-FIELD ANALYSIS TABLE GENERATOR - Infinity Research Paper
====================================================================

Generates the Field-by-Field Analysis of General Concordance table (Section 4.6)
comparing Claude 3.5 Sonnet vs DeepSeek V3 performance across 8 scientific fields.

Input: analysis_claude.json + analysis_deepseek.json
Output: field_analysis_table.txt with detailed field-specific concordance
"""

import json
import os
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

def extract_field_classifications(file_path: str) -> Dict[str, List[str]]:
    """
    Extract classifications organized by scientific field
    Returns dict: {field_name: [list_of_classifications]}
    """
    field_classifications = defaultdict(list)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for article in data:
        for field_name, field_data in article['fields'].items():
            analysis = field_data.get('analysis', {})
            
            # Handle the combined "Author, Year, Study Type" field
            if field_name == "Author, Year, Study Type":
                if 'author_classification' in analysis:
                    field_classifications['Author'].append(analysis['author_classification'])
                if 'year_classification' in analysis:
                    field_classifications['Year'].append(analysis['year_classification'])
                if 'study_type_classification' in analysis:
                    field_classifications['Study Type'].append(analysis['study_type_classification'])
            elif 'classification' in analysis:
                # Use exact field names from the data
                field_classifications[field_name].append(analysis['classification'])
    
    return dict(field_classifications)

def calculate_general_concordance_rate(classifications: List[str]) -> Tuple[float, int, int]:
    """
    Calculate General Concordance (A+B+C) rate for a field
    Returns: (percentage, concordant_count, total_count)
    """
    if not classifications:
        return 0.0, 0, 0
    
    concordant = sum(1 for c in classifications if c in ['A', 'B', 'C'])
    total = len(classifications)
    percentage = (concordant / total * 100) if total > 0 else 0
    
    return percentage, concordant, total

def count_distributions(classifications: List[str]) -> Dict[str, int]:
    """
    Count distribution of each category (A, B, C, D, E, F)
    """
    counter = Counter(classifications)
    categories = ['A', 'B', 'C', 'D', 'E', 'F']
    
    result = {}
    for cat in categories:
        result[cat] = counter.get(cat, 0)
    
    return result

def format_distribution(distribution: Dict[str, int]) -> str:
    """
    Format distribution as "A:19 B:0 C:0 D:0 E:0 F:0"
    """
    parts = []
    for cat in ['A', 'B', 'C', 'D', 'E', 'F']:
        count = distribution.get(cat, 0)
        if count > 0:
            parts.append(f"{cat}:{count}")
        else:
            parts.append(f"{cat}:0")
    
    return " ".join(parts)

def generate_field_analysis_table(claude_fields: Dict[str, List[str]], 
                                deepseek_fields: Dict[str, List[str]]) -> str:
    """
    Generate the field-by-field analysis table
    """
    
    # Define field order as shown in the image
    field_order = [
        'Author',
        'Year', 
        'Study Type',
        'Methodology',
        'Sample Size (n), Population Characteristics',
        'Outcome Measure',
        'Key Findings',
        'Limitations'
    ]
    
    table = ["4.6 Field-by-Field Analysis of General Concordance", ""]
    table.append("| Scientific Field                          | Claude 3.5 Sonnet | DeepSeek V3       | Distribution (Claude)      | Distribution (DeepSeek)    |")
    table.append("|-------------------------------------------|--------------------|--------------------|----------------------------|----------------------------|")
    
    for field in field_order:
        claude_classifications = claude_fields.get(field, [])
        deepseek_classifications = deepseek_fields.get(field, [])
        
        # Calculate concordance rates
        claude_rate, claude_concordant, claude_total = calculate_general_concordance_rate(claude_classifications)
        deepseek_rate, deepseek_concordant, deepseek_total = calculate_general_concordance_rate(deepseek_classifications)
        
        # Calculate distributions
        claude_dist = count_distributions(claude_classifications)
        deepseek_dist = count_distributions(deepseek_classifications)
        
        claude_dist_str = format_distribution(claude_dist)
        deepseek_dist_str = format_distribution(deepseek_dist)
        
        # Format the row
        claude_col = f"{claude_rate:5.1f}% ({claude_concordant}/{claude_total})"
        deepseek_col = f"{deepseek_rate:5.1f}% ({deepseek_concordant}/{deepseek_total})"
        
        table.append(f"| {field:<41} | {claude_col:<18} | {deepseek_col:<18} | {claude_dist_str:<26} | {deepseek_dist_str:<26} |")
    
    # Add description
    table.extend([
        "",
        "The table reports the General concordance (A+B+C), indicating overall alignment where all",
        "core information was retained, with extra details added in non-critical areas. Both models",
        "Claude 3.5 Sonnet and DeepSeek V3 achieved 100% concordance in the Author and",
        "Outcome Measure fields, demonstrating high reliability in validating these data types. A",
        "notable point in the Author field is that, although all 19 cases were successfully validated,",
        "DeepSeek had a single Category C occurrence, where the automated output returned",
        '"Borresen" while the manual reference read "Borreson." This highlights how subtle spelling',
        "variations can appear even in high-performing fields and reinforces that, while Claude tends",
        "to be more critical in overall validation, DeepSeek maintained consistent precision in",
        "extracting and validating author names across diverse publication formats.",
        "",
        "The most challenging fields for validation were Year, Key Findings, and Sample",
        "Size/Population Characteristics, where discrepancies or gaps were more frequent. The Year",
        "field achieved only 63.2% (12/19) for Claude and 68.4% (13/19) for DeepSeek, reflecting",
        "source-level date conflicts. Key Findings (84.2% for Claude vs. 73.6% for DeepSeek) and",
        "Limitations (63.2% vs. 94.7%) showed the greatest variation between models, illustrating",
        "the difficulty of validating complex narrative information. Sample Size and Population",
        "Characteristics reached 78.9% (15/19) for Claude versus 100% (19/19) for DeepSeek,",
        "indicating the latter's stronger capability in validating structured quantitative data. These",
        "results indicate that while both models maintain high concordance in objective fields, the",
        "validation of temporal and narrative information remains more prone to subtle",
        "inconsistencies, which subsequently guided the detailed discrepancy analysis in the",
        "following evaluation stage."
    ])
    
    return "\n".join(table)

def main():
    """
    Main function to generate field analysis table
    """
    print("📊 INFINITY RESEARCH - Field Analysis Table Generator")
    print("=" * 65)
    
    # File paths
    claude_file = "analysis/analysis_claude.json"
    deepseek_file = "analysis/analysis_deepseek.json"
    
    if not os.path.exists(claude_file):
        print(f"❌ Error: {claude_file} not found!")
        return
        
    if not os.path.exists(deepseek_file):
        print(f"❌ Error: {deepseek_file} not found!")
        return
    
    print("📊 Extracting field-specific classification data...")
    
    # Extract field classifications
    claude_fields = extract_field_classifications(claude_file)
    deepseek_fields = extract_field_classifications(deepseek_file)
    
    print(f"   Claude fields analyzed: {len(claude_fields)}")
    print(f"   DeepSeek fields analyzed: {len(deepseek_fields)}")
    
    # Display field-by-field analysis
    print(f"\n📈 FIELD-BY-FIELD ANALYSIS RESULTS:")
    print("=" * 50)
    
    field_order = [
        'Author', 'Year', 'Study Type', 'Methodology',
        'Sample Size (n), Population Characteristics',
        'Outcome Measure', 'Key Findings', 'Limitations'
    ]
    
    for field in field_order:
        claude_classifications = claude_fields.get(field, [])
        deepseek_classifications = deepseek_fields.get(field, [])
        
        claude_rate, claude_concordant, claude_total = calculate_general_concordance_rate(claude_classifications)
        deepseek_rate, deepseek_concordant, deepseek_total = calculate_general_concordance_rate(deepseek_classifications)
        
        print(f"🎯 {field}:")
        print(f"   Claude: {claude_rate:5.1f}% ({claude_concordant}/{claude_total})")
        print(f"   DeepSeek: {deepseek_rate:5.1f}% ({deepseek_concordant}/{deepseek_total})")
        
        # Show distributions
        claude_dist = count_distributions(claude_classifications)
        deepseek_dist = count_distributions(deepseek_classifications)
        
        print(f"   Claude distribution: {format_distribution(claude_dist)}")
        print(f"   DeepSeek distribution: {format_distribution(deepseek_dist)}")
        print()
    
    # Generate table
    print(f"📝 Generating field analysis table...")
    table_content = generate_field_analysis_table(claude_fields, deepseek_fields)
    
    # Save table
    output_file = "plots/field_analysis_table.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(table_content)
    
    print(f"   ✅ Table saved: {output_file}")
    
    print(f"\n🎯 Field analysis table generation complete!")
    print(f"   📊 Table: {output_file}")

if __name__ == "__main__":
    main()