#!/usr/bin/env python3
"""
🚀 INFINITY RESEARCH - Figure 5 Chart Generator
==================================================
Generates Figure 5: Vision Baseline vs API-Enhanced Consensus Performance

Creates a 2x11 heatmap matrix comparing Vision vs Consensus completion rates
across 11 core bibliographic fields with improvement indicators.
"""

import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from typing import Dict, List

def is_field_filled(value) -> bool:
    """Check if a field is considered filled (non-null, non-empty)"""
    if value is None:
        return False
    if isinstance(value, str):
        return len(value.strip()) > 0
    if isinstance(value, list):
        return len(value) > 0
    return bool(value)

def extract_figure5_data() -> Dict:
    """
    Extract Vision vs Consensus data for Figure 5 analysis
    
    Returns:
        Dict with vision/consensus counts and percentages
    """
    
    # Core bibliographic fields (11 fields = 209 total combinations)
    core_fields = [
        'Title', 'Authors', 'Journal', 'Year', 'Volume', 'Issue', 
        'Pages', 'DOI', 'Publisher', 'Keywords', 'Abstract'
    ]
    
    # Initialize counters
    vision_counts = {field: 0 for field in core_fields}
    consensus_counts = {field: 0 for field in core_fields}
    
    articles_data = []
    
    print("🚀 INFINITY RESEARCH - Figure 5 Chart Generator")
    print("==================================================")
    print("📊 Extracting Vision vs Consensus field completion...")
    print("")
    
    # Process articles
    json_dir = "json"
    if not os.path.exists(json_dir):
        print(f"❌ Directory {json_dir} not found!")
        return {}
    
    article_folders = [f for f in os.listdir(json_dir) if f.startswith('Article_')]
    article_folders.sort()
    
    print(f"📁 Found {len(article_folders)} article folders")
    print("")
    
    for folder_name in article_folders:
        folder = os.path.join(json_dir, folder_name)
        if not os.path.isdir(folder):
            continue
            
        print(f"   Processing {folder_name}...")
        
        # Read final_json.json for Vision data
        final_json_path = os.path.join(folder, "final_json.json")
        apis_clean_path = os.path.join(folder, "apis_clean_json.json")
        
        if not os.path.exists(final_json_path):
            print(f"      ⚠️ No final_json.json found")
            continue
            
        try:
            # Extract Vision data (baseline extraction)
            with open(final_json_path, 'r', encoding='utf-8') as f:
                final_data = json.load(f)
            
            vision_data = final_data.get('vision_json', {})
            vision_response = vision_data.get('extracted_data', {})
            
            # Extract Consensus data from apis_clean_json.json
            consensus_data = {}
            if os.path.exists(apis_clean_path):
                with open(apis_clean_path, 'r', encoding='utf-8') as f:
                    apis_clean_data = json.load(f)
                consensus_data = apis_clean_data.get('consensus_result', {})
            
            # Skip if no consensus data found
            if not consensus_data:
                print(f"      ⚠️ No consensus_result found in {folder_name}")
                continue
            
            # Count filled fields for each source
            vision_filled = 0
            consensus_filled = 0
            
            for field in core_fields:
                # Vision baseline
                vision_value = None
                if isinstance(vision_response, dict):
                    vision_value = vision_response.get(field)
                
                if is_field_filled(vision_value):
                    vision_counts[field] += 1
                    vision_filled += 1
                
                # Consensus (enriched)
                consensus_value = consensus_data.get(field)
                if is_field_filled(consensus_value):
                    consensus_counts[field] += 1
                    consensus_filled += 1
            
            print(f"      📊 Vision: {vision_filled}/{len(core_fields)} fields, Consensus: {consensus_filled}/{len(core_fields)} fields")
            
            # Store article data
            articles_data.append({
                'folder': folder_name,
                'vision_counts': vision_filled,
                'consensus_counts': consensus_filled,
                'vision_data': vision_response,
                'consensus_data': consensus_data
            })
            
        except Exception as e:
            print(f"      ⚠️ Error processing {folder_name}: {e}")
            continue
    
    total_articles = len(articles_data)
    total_possible = total_articles * len(core_fields)
    
    # Calculate percentages for each field
    vision_percentages = {}
    consensus_percentages = {}
    
    for field in core_fields:
        vision_pct = (vision_counts[field] / total_articles * 100) if total_articles > 0 else 0
        consensus_pct = (consensus_counts[field] / total_articles * 100) if total_articles > 0 else 0
        
        vision_percentages[field] = vision_pct
        consensus_percentages[field] = consensus_pct
    
    # Calculate totals
    vision_total = sum(vision_counts.values())
    consensus_total = sum(consensus_counts.values())
    
    vision_completion = (vision_total / total_possible * 100) if total_possible > 0 else 0
    consensus_completion = (consensus_total / total_possible * 100) if total_possible > 0 else 0
    improvement = consensus_completion - vision_completion
    
    return {
        'total_articles': total_articles,
        'core_fields': core_fields,
        'vision_counts': vision_counts,
        'consensus_counts': consensus_counts,
        'vision_percentages': vision_percentages,
        'consensus_percentages': consensus_percentages,
        'vision_total': vision_total,
        'consensus_total': consensus_total,
        'total_possible': total_possible,
        'vision_completion': vision_completion,
        'consensus_completion': consensus_completion,
        'improvement': improvement,
        'articles_data': articles_data
    }

def create_figure5_chart(data: Dict):
    """Create Figure 5 heatmap chart (Vision vs Consensus)"""
    
    if not data or data['total_articles'] == 0:
        print("❌ No data available for chart generation")
        return
    
    core_fields = data['core_fields']
    vision_percentages = data['vision_percentages']
    consensus_percentages = data['consensus_percentages']
    
    # Prepare data matrix: [Vision, Consensus] x [core_fields]
    data_matrix = []
    source_names = ['Vision', 'Consensus']
    
    # Vision row
    vision_row = [vision_percentages[field] for field in core_fields]
    data_matrix.append(vision_row)
    
    # Consensus row  
    consensus_row = [consensus_percentages[field] for field in core_fields]
    data_matrix.append(consensus_row)
    
    # Convert to numpy array
    data_matrix = np.array(data_matrix)
    
    # Create figure - compact size for 2x11 matrix
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 4))  # Wider but shorter for 2 rows
    
    # Create custom colormap: White (0%) -> Blue -> Green (100%)
    colors = ['#FFFFFF', '#0066CC', '#6699FF', '#66FF66', '#00CC00']
    custom_cmap = LinearSegmentedColormap.from_list("custom", colors, N=256)
    
    # Create the heatmap
    im = ax.imshow(data_matrix, cmap=custom_cmap, aspect='auto', vmin=0, vmax=100)
    
    # Configure axes
    ax.set_xticks(np.arange(len(core_fields)))
    ax.set_yticks(np.arange(len(source_names)))
    ax.set_xticklabels([field.title() for field in core_fields])
    ax.set_yticklabels(source_names)
    
    # Rotate x labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add percentage labels and improvement indicators
    for i in range(len(source_names)):
        for j in range(len(core_fields)):
            percentage = data_matrix[i, j]
            
            # Color based on percentage
            text_color = 'white' if percentage > 50 else 'black'
            ax.text(j, i, f'{percentage:.1f}%', ha="center", va="center", 
                   color=text_color, fontweight='bold', fontsize=10)
            
            # Add improvement indicator for consensus row
            if i == 1:  # Consensus row
                vision_pct = data_matrix[0, j]  # Vision value for same field
                if percentage > vision_pct:
                    improvement = percentage - vision_pct
                    ax.text(j, i - 0.3, f'(+{improvement:.1f}%)', ha="center", va="center", 
                           color='#27ae60', fontweight='bold', fontsize=8)
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Configure grid
    ax.set_xticks(np.arange(len(core_fields)+1)-.5, minor=True)
    ax.set_yticks(np.arange(len(source_names)+1)-.5, minor=True)
    ax.grid(which="minor", color="white", linestyle='-', linewidth=2)
    ax.tick_params(which="minor", size=0)
    
    # Title and labels
    ax.set_title('Figure 5. Vision Baseline vs API-Enhanced Consensus Performance\nCore Bibliographic Fields Completion Rates', 
                fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
    ax.set_xlabel('Core Metadata Fields', fontsize=12, fontweight='bold', color='#34495E')
    ax.set_ylabel('Processing Stage', fontsize=12, fontweight='bold', color='#34495E')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.6, aspect=15)
    cbar.set_label('Field Completion (%)', rotation=270, labelpad=20, 
                  fontsize=11, fontweight='bold', color='#34495E')
    cbar.ax.tick_params(labelsize=9)
    cbar.set_ticks([0, 25, 50, 75, 100])
    cbar.set_ticklabels(['0%', '25%', '50%', '75%', '100%'])
    
    # Layout and background
    plt.tight_layout()
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FFFFFF')
    
    # Save chart
    plt.savefig("plots/figure5_chart.png", dpi=150, bbox_inches='tight',
               facecolor='#FAFAFA', edgecolor='none')
    plt.close()
    
    print("   ✅ Chart saved: plots/figure5_chart.png")

def generate_figure5_legend(data: Dict):
    """Generate Figure 5 legend text matching article format"""
    
    if not data or data['total_articles'] == 0:
        print("❌ No data available for legend generation")
        return
    
    total_articles = data['total_articles']
    vision_total = data['vision_total']
    consensus_total = data['consensus_total']
    total_possible = data['total_possible']
    vision_completion = data['vision_completion']
    consensus_completion = data['consensus_completion']
    improvement = data['improvement']
    improvement_count = consensus_total - vision_total
    core_fields = data['core_fields']
    
    vision_percentages = data['vision_percentages']
    consensus_percentages = data['consensus_percentages']
    
    # Count fields with improvement
    fields_improved = 0
    field_improvements = []
    
    for field in core_fields:
        vision_pct = vision_percentages[field]
        consensus_pct = consensus_percentages[field]
        diff_pct = consensus_pct - vision_pct
        
        if diff_pct > 0:
            fields_improved += 1
            field_improvements.append({
                'field': field,
                'vision_pct': vision_pct,
                'consensus_pct': consensus_pct,
                'diff_pct': diff_pct
            })
    
    # Generate technical legend
    legend_text = (
        f"Figure 5. Vision Baseline vs API-Enhanced Consensus Performance - Core Bibliographic Fields ({total_articles} articles). "
        f"Vision baseline: {vision_completion:.1f}% ({vision_total}/{total_possible} fields). "
        f"Final consensus: {consensus_completion:.1f}% ({consensus_total}/{total_possible} fields). "
        f"Overall improvement: {improvement:+.1f}% ({improvement_count:+d} fields). "
        f"Enhanced fields: {fields_improved}/{len(core_fields)} core fields. "
        f"API enrichment successfully filled {improvement_count} additional bibliographic fields across "
        f"{total_articles} articles, demonstrating the complementary value of automated metadata enhancement "
        f"over Vision-only baseline extraction. Fields with highest improvement: "
    )
    
    # Add top improvements
    field_improvements.sort(key=lambda x: x['diff_pct'], reverse=True)
    top_improvements = field_improvements[:3]
    
    improvement_details = []
    for imp in top_improvements:
        improvement_details.append(f"{imp['field']} (+{imp['diff_pct']:.1f}%)")
    
    legend_text += ", ".join(improvement_details) + "."
    
    # Save legend
    with open("plots/figure5_legend.txt", "w", encoding="utf-8") as f:
        f.write(legend_text)
    
    print("   ✅ Legend saved: plots/figure5_legend.txt")

def main():
    """Main execution function"""
    
    # Extract data
    data = extract_figure5_data()
    
    if not data or data['total_articles'] == 0:
        print("❌ No data extracted. Exiting.")
        return
    
    print("")
    print("📊 Summary:")
    print(f"   Articles processed: {data['total_articles']}")
    print(f"   Vision baseline: {data['vision_completion']:.1f}% ({data['vision_total']}/{data['total_possible']} fields)")
    print(f"   API consensus: {data['consensus_completion']:.1f}% ({data['consensus_total']}/{data['total_possible']} fields)")
    print(f"   Improvement: {data['improvement']:+.1f}% ({data['consensus_total'] - data['vision_total']:+d} fields)")
    
    print("🎨 Generating Figure 5 chart...")
    create_figure5_chart(data)
    
    print("📝 Generating Figure 5 legend...")
    generate_figure5_legend(data)
    
    print("🎯 Figure 5 generation complete!")
    print("   📊 Chart: plots/figure5_chart.png")
    print("   📝 Legend: plots/figure5_legend.txt")

if __name__ == "__main__":
    main()