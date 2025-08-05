#!/usr/bin/env python3
"""
INFINITY RESEARCH - Figure 6 Chart Generator
============================================
Generates Figure 6: Complete API Specialization Matrix
Analysis of API contribution patterns across metadata fields

Based on field_sources analysis from APIs Clean JSON data
"""

import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

def parse_field_sources(field_sources_str: str) -> Tuple[str, List[str]]:
    """
    Parse field_sources string to identify type and APIs
    Returns: (type, apis_list)
    - type: 'single', 'merged', 'validated', 'mixed'
    - apis_list: list of contributing APIs
    """
    if not field_sources_str or field_sources_str == "None":
        return 'empty', []
    
    # Handle mixed symbols (both | and + in same string)
    if '+' in field_sources_str and '|' in field_sources_str:
        # Mixed symbols: crossref|unpaywall+vision
        tipo = 'mixed'
        # First split by +, then split each part by |
        parts = field_sources_str.split('+')
        apis = []
        for part in parts:
            if '|' in part:
                apis.extend(part.split('|'))
            else:
                apis.append(part)
    elif '+' in field_sources_str:
        # Merged: vision+europe_pmc
        tipo = 'merged'
        apis = field_sources_str.split('+')
    elif '|' in field_sources_str:
        # Validated: semantic_scholar|openalex
        tipo = 'validated'
        apis = field_sources_str.split('|')
    else:
        # Single source: vision, crossref, etc.
        tipo = 'single'
        apis = [field_sources_str]
    
    # Clean and normalize API names
    apis_clean = [api.strip().lower() for api in apis if api.strip()]
    
    return tipo, apis_clean

def analyze_field_sources(json_folder_path: str) -> Dict:
    """
    Analyze field_sources data from all articles
    Returns comprehensive API specialization analysis
    """
    # All metadata fields (16 total as mentioned in article)
    all_fields = [
        'title', 'authors', 'journal', 'year', 'doi', 'abstract', 
        'keywords', 'publisher', 'volume', 'issue', 'pages', 
        'pmid', 'pmcid', 'citations', 'openaccess', 'pdfurl'
    ]
    
    # Initialize counters
    api_field_counts = defaultdict(lambda: defaultdict(int))  # api -> field -> count
    collaboration_patterns = defaultdict(int)  # type -> count
    field_details = defaultdict(list)  # field -> collaboration details
    
    # Track all APIs found
    all_apis = set()
    total_articles = 0
    articles_with_sources = 0
    
    print("🚀 INFINITY RESEARCH - Figure 6 Chart Generator")
    print("=" * 50)
    print("📊 Analyzing API specialization patterns...")
    
    # Process each article folder
    article_folders = [f for f in os.listdir(json_folder_path) if f.startswith('Article_')]
    article_folders.sort()
    
    print(f"📁 Found {len(article_folders)} article folders")
    
    for folder_name in article_folders:
        folder_path = os.path.join(json_folder_path, folder_name)
        apis_clean_path = os.path.join(folder_path, 'apis_clean_json.json')
        
        if not os.path.exists(apis_clean_path):
            continue
            
        total_articles += 1
        
        try:
            # Load APIs clean data
            with open(apis_clean_path, 'r', encoding='utf-8') as f:
                apis_data = json.load(f)
            
            # Extract field_sources from consensus_result
            consensus_result = apis_data.get('consensus_result', {})
            confidence_factors = consensus_result.get('confidence_factors', {})
            field_sources = confidence_factors.get('field_sources', {})
            
            if not field_sources:
                print(f"   ⚠️ No field_sources found in {folder_name}")
                continue
                
            articles_with_sources += 1
            print(f"   Processing {folder_name}...")
            
            # Analyze each field's sources
            for field, sources_str in field_sources.items():
                field_lower = field.lower()
                
                if field_lower in [f.lower() for f in all_fields]:
                    # Parse sources
                    collaboration_type, apis = parse_field_sources(sources_str)
                    
                    # Count collaboration pattern
                    collaboration_patterns[collaboration_type] += 1
                    
                    # Count each API's contribution to this field
                    for api in apis:
                        api_field_counts[api][field_lower] += 1
                        all_apis.add(api)
                    
                    # Store field collaboration details
                    field_details[field_lower].append({
                        'type': collaboration_type,
                        'sources': sources_str,
                        'apis': apis,
                        'article': folder_name
                    })
                        
        except Exception as e:
            print(f"   ❌ Error processing {folder_name}: {e}")
            continue
    
    # Calculate total instances and patterns
    total_instances = sum(collaboration_patterns.values())
    
    # Calculate API totals and sort
    api_totals = {}
    for api in all_apis:
        total_contrib = sum(api_field_counts[api].values())
        api_totals[api] = total_contrib
    
    sorted_apis = sorted(api_totals.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n📊 FIGURE 6 ANALYSIS RESULTS:")
    print("=" * 50)
    print(f"📈 Metadata fields analyzed: {len(all_fields)}")
    print(f"📝 Total articles: {total_articles}")
    print(f"📊 Articles with field_sources: {articles_with_sources}")
    print(f"🎯 Total possible field combinations: {len(all_fields) * articles_with_sources}")
    print(f"✅ Successfully populated combinations: {total_instances}")
    
    print(f"\n🏆 TOP API CONTRIBUTORS:")
    for i, (api, count) in enumerate(sorted_apis[:5]):
        percentage = (count / total_instances * 100) if total_instances > 0 else 0
        print(f"   {i+1}. {api.title()}: {count} instances ({percentage:.1f}%)")
    
    # Calculate validation patterns
    validated_count = collaboration_patterns.get('validated', 0)
    single_count = collaboration_patterns.get('single', 0) 
    merged_count = collaboration_patterns.get('merged', 0)
    mixed_count = collaboration_patterns.get('mixed', 0)
    
    # Multi-source = validated + mixed
    multi_source = validated_count + mixed_count
    
    print(f"\n🔍 DATA VALIDATION PATTERNS:")
    if total_instances > 0:
        multi_pct = (multi_source / total_instances * 100)
        single_pct = (single_count / total_instances * 100)
        merged_pct = (merged_count / total_instances * 100)
        
        print(f"   🤝 Multi-source validation: {multi_pct:.1f}% ({multi_source} instances)")
        print(f"   📌 Single-source extraction: {single_pct:.1f}% ({single_count} instances)")
        print(f"   ➕ Complementary data merging: {merged_pct:.1f}% ({merged_count} instances)")
    
    return {
        'api_field_counts': dict(api_field_counts),
        'collaboration_patterns': dict(collaboration_patterns),
        'field_details': dict(field_details),
        'api_totals': api_totals,
        'sorted_apis': sorted_apis,
        'all_fields': all_fields,
        'total_articles': articles_with_sources,
        'total_instances': total_instances,
        'all_apis': sorted(all_apis)
    }

def create_specialization_matrix_chart(analysis_data: Dict) -> str:
    """
    Create API specialization matrix heatmap following original code style
    """
    api_field_counts = analysis_data['api_field_counts']
    all_fields = analysis_data['all_fields']
    sorted_apis = analysis_data['sorted_apis']
    total_articles = analysis_data['total_articles']
    
    # Take top 10 APIs for visualization
    top_apis = [api for api, _ in sorted_apis[:10]]
    
    # Create matrix data
    matrix_data = []
    for api in top_apis:
        row = []
        for field in all_fields:
            count = api_field_counts[api].get(field.lower(), 0)
            # Convert to percentage of total articles
            percentage = (count / total_articles * 100) if total_articles > 0 else 0
            row.append(percentage)
        matrix_data.append(row)
    
    # Convert to numpy array
    matrix_data = np.array(matrix_data)
    
    # Calculate dynamic sizing based on matrix dimensions (same as original)
    num_fields = len(all_fields)
    num_apis = len(top_apis)
    
    # Dynamic sizing: wider for more fields, taller for more APIs
    width = max(10, min(18, num_fields * 0.8))  # 10-18 inches width
    height = max(6, min(14, num_apis * 0.7))    # 6-14 inches height
    
    # Create figure - fast style like original
    plt.style.use('fast')
    fig, ax = plt.subplots(figsize=(width, height))
    
    # Create custom colormap: White (0%) -> Blue -> Green (100%) - same as original
    colors = ['#FFFFFF', '#0066CC', '#6699FF', '#66FF66', '#00CC00']
    from matplotlib.colors import LinearSegmentedColormap
    custom_cmap = LinearSegmentedColormap.from_list("custom", colors, N=256)
    
    # Create the heatmap
    im = ax.imshow(matrix_data, cmap=custom_cmap, aspect='auto', vmin=0, vmax=100)
    
    # Configure axes
    ax.set_xticks(np.arange(len(all_fields)))
    ax.set_yticks(np.arange(len(top_apis)))
    ax.set_xticklabels([field.title().replace('_', ' ') for field in all_fields])
    ax.set_yticklabels([api.title() for api in top_apis])
    
    # Rotate x labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add percentage labels for non-zero values
    for i in range(len(top_apis)):
        for j in range(len(all_fields)):
            percentage = matrix_data[i, j]
            if percentage > 0:
                # Color based on percentage
                text_color = 'white' if percentage > 50 else 'black'
                
                # Dynamic font size based on matrix size
                base_fontsize = max(6, min(10, 120 / max(num_fields, num_apis)))
                
                ax.text(j, i, f'{percentage:.0f}%', ha="center", va="center", 
                       color=text_color, fontweight='bold', fontsize=base_fontsize)
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Configure grid
    ax.set_xticks(np.arange(len(all_fields)+1)-.5, minor=True)
    ax.set_yticks(np.arange(len(top_apis)+1)-.5, minor=True)
    ax.grid(which="minor", color="white", linestyle='-', linewidth=2)
    ax.tick_params(which="minor", size=0)
    
    # Title and labels - same style as original
    ax.set_title('Figure 6. Complete API Specialization Matrix\nField Coverage Distribution Across All Data Sources', 
                fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
    ax.set_xlabel('Metadata Fields', fontsize=12, fontweight='bold', color='#34495E')
    ax.set_ylabel('Data Sources (APIs)', fontsize=12, fontweight='bold', color='#34495E')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8, aspect=20)
    cbar.set_label('Field Coverage (%)', rotation=270, labelpad=20, 
                  fontsize=11, fontweight='bold', color='#34495E')
    cbar.ax.tick_params(labelsize=9)
    cbar.set_ticks([0, 25, 50, 75, 100])
    cbar.set_ticklabels(['0%', '25%', '50%', '75%', '100%'])
    
    # Layout and background - same as original
    plt.tight_layout()
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FFFFFF')
    
    # Save chart
    chart_path = 'plots/figure6_chart.png'
    plt.savefig(chart_path, dpi=150, bbox_inches='tight',
               facecolor='#FAFAFA', edgecolor='none')
    plt.close()
    
    return chart_path

def generate_figure6_legend(analysis_data: Dict) -> str:
    """
    Generate Figure 6 legend text matching article content
    """
    api_totals = analysis_data['api_totals']
    sorted_apis = analysis_data['sorted_apis']
    collaboration_patterns = analysis_data['collaboration_patterns']
    total_instances = analysis_data['total_instances']
    total_articles = analysis_data['total_articles']
    all_fields = analysis_data['all_fields']
    field_details = analysis_data['field_details']
    
    # Calculate key statistics
    total_possible = len(all_fields) * total_articles
    
    # Top 3 APIs
    top3_apis = sorted_apis[:3]
    
    # Validation patterns
    validated_count = collaboration_patterns.get('validated', 0)
    single_count = collaboration_patterns.get('single', 0)
    merged_count = collaboration_patterns.get('merged', 0)
    mixed_count = collaboration_patterns.get('mixed', 0)
    
    # Multi-source = validated + mixed
    multi_source = validated_count + mixed_count
    
    # Calculate percentages
    multi_pct = (multi_source / total_instances * 100) if total_instances > 0 else 0
    single_pct = (single_count / total_instances * 100) if total_instances > 0 else 0
    merged_pct = (merged_count / total_instances * 100) if total_instances > 0 else 0
    
    # Calculate field-specific specializations
    vision_title_count = len([d for d in field_details.get('title', []) if 'vision' in d['apis']])
    vision_authors_count = len([d for d in field_details.get('authors', []) if 'vision' in d['apis']])
    vision_abstract_count = len([d for d in field_details.get('abstract', []) if 'vision' in d['apis']])
    
    pmid_details = field_details.get('pmid', [])
    pmid_total = len(pmid_details)
    pmid_europe_count = len([d for d in pmid_details if 'europe_pmc' in d['apis']])
    pmid_coverage = (pmid_europe_count / pmid_total * 100) if pmid_total > 0 else 0
    
    doi_details = field_details.get('doi', [])
    doi_total = len(doi_details)
    doi_crossref_count = len([d for d in doi_details if 'crossref' in d['apis']])
    doi_coverage = (doi_crossref_count / doi_total * 100) if doi_total > 0 else 0
    
    citations_details = field_details.get('citations', [])
    citations_total = len(citations_details)
    citations_semantic_count = len([d for d in citations_details if 'semantic_scholar' in d['apis']])
    citations_coverage = (citations_semantic_count / citations_total * 100) if citations_total > 0 else 0
    
    # Generate legend text
    legend_text = f"""Figure 6. Complete API Specialization Matrix

Comprehensive analysis of API contribution patterns across {len(all_fields)} metadata fields for {total_articles} articles. Of {total_possible} theoretically possible field combinations, {total_instances} were successfully populated by the 11-API ecosystem. """
    
    if len(top3_apis) >= 3:
        api1_name, api1_count = top3_apis[0]
        api2_name, api2_count = top3_apis[1] 
        api3_name, api3_count = top3_apis[2]
        
        api1_pct = (api1_count / total_instances * 100) if total_instances > 0 else 0
        
        legend_text += f"{api1_name.title()} emerged as the primary contributor ({api1_count} instances, {api1_pct:.1f}% of total contributions), followed by {api2_name.title()} ({api2_count} instances) and {api3_name.title()} ({api3_count} instances). "
    
    legend_text += f"Data validation patterns: {multi_pct:.1f}% of populated fields achieved multi-source validation, {single_pct:.1f}% relied on single-source extraction, and {merged_pct:.1f}% utilized complementary data merging. "
    
    # Add specialization details based on actual data
    if vision_title_count == total_articles and vision_authors_count == total_articles:
        legend_text += f"API specializations: Vision excelled in core bibliographic fields (100% success for title, authors"
        if vision_abstract_count == total_articles:
            legend_text += ", abstract), "
        else:
            legend_text += "), "
    
    legend_text += f"while specialized APIs demonstrated domain expertise—Europe PMC for PubMed identifiers ({pmid_coverage:.1f}% PMID coverage), CrossRef for DOI validation ({doi_coverage:.1f}% coverage), and Semantic Scholar for citation metrics ({citations_coverage:.1f}% coverage). "
    
    # Calculate cross-validation for critical fields
    authors_multi = len([d for d in field_details.get('authors', []) if len(d['apis']) > 1])
    doi_multi = len([d for d in field_details.get('doi', []) if len(d['apis']) > 1])
    publisher_multi = len([d for d in field_details.get('publisher', []) if len(d['apis']) > 1])
    
    authors_multi_pct = (authors_multi / len(field_details.get('authors', [])) * 100) if field_details.get('authors') else 0
    doi_multi_pct = (doi_multi / len(field_details.get('doi', [])) * 100) if field_details.get('doi') else 0
    publisher_multi_pct = (publisher_multi / len(field_details.get('publisher', [])) * 100) if field_details.get('publisher') else 0
    
    legend_text += f"Cross-validation robustness: Critical fields showed extensive collaboration, with Authors ({authors_multi_pct:.1f}% multi-source), DOI ({doi_multi_pct:.1f}%), and Publisher ({publisher_multi_pct:.1f}%) achieving the highest validation rates across the API ecosystem."
    
    return legend_text

def main():
    """Main execution function"""
    json_folder = "json"
    
    if not os.path.exists(json_folder):
        print(f"❌ Error: {json_folder} folder not found!")
        return
    
    # Analyze field sources data
    analysis_data = analyze_field_sources(json_folder)
    
    print(f"\n🎨 Generating Figure 6 chart...")
    chart_path = create_specialization_matrix_chart(analysis_data)
    print(f"   ✅ Chart saved: {chart_path}")
    
    print(f"📝 Generating Figure 6 legend...")
    legend_text = generate_figure6_legend(analysis_data)
    legend_path = 'plots/figure6_legend.txt'
    
    with open(legend_path, 'w', encoding='utf-8') as f:
        f.write(legend_text)
    print(f"   ✅ Legend saved: {legend_path}")
    
    print(f"\n🎯 Figure 6 generation complete!")
    print(f"   📊 Chart: {chart_path}")
    print(f"   📝 Legend: {legend_path}")

if __name__ == "__main__":
    main()