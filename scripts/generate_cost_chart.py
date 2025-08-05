#!/usr/bin/env python3
"""
📊 COST CHART GENERATOR - Infinity Research Paper
=================================================

Generates the cost analysis chart and legend following the exact same pattern 
as the word_generator.py from the core system.

Input: JSON files from infinity-research-paper/json/Article_XX/
Output: cost_chart.png + cost_legend.txt
"""

import json
import os
import glob
from typing import Dict, List, Optional
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import io

# Configure matplotlib for better performance
plt.ioff()  # Turn off interactive mode
matplotlib.rcParams['figure.max_open_warning'] = 0

def extract_cost_data_from_articles() -> Dict:
    """
    Extract cost data from all articles following the same pattern as word_generator
    """
    print("📊 Extracting cost data from article JSONs...")
    
    # Initialize lists for chart data (4 phases)
    costs = []
    vision_costs = []
    topics_costs = []
    consensus_costs = []
    questions_costs = []
    labels = []
    
    # Get all article folders in order
    article_folders = glob.glob("json/Article_*")
    article_folders.sort()
    
    print(f"📁 Found {len(article_folders)} article folders")
    
    for folder in article_folders:
        folder_name = os.path.basename(folder)
        article_num = int(folder_name.split('_')[1])
        
        print(f"   Processing {folder_name}...")
        
        # Initialize costs for this article
        vision_cost = 0.0
        consensus_cost = 0.0
        topics_cost = 0.0
        questions_cost = 0.0
        
        # Extract vision cost from vision_json.json
        vision_json_path = os.path.join(folder, "vision_json.json")
        if os.path.exists(vision_json_path):
            try:
                with open(vision_json_path, 'r', encoding='utf-8') as f:
                    vision_data = json.load(f)
                
                # Look for cost in cost_tracking section
                if 'cost_tracking' in vision_data:
                    vision_cost = float(vision_data['cost_tracking'].get('total_cost', 0))
                elif 'total_cost' in vision_data:
                    vision_cost = float(vision_data.get('total_cost', 0))
                    
            except Exception as e:
                print(f"      ⚠️ Error reading vision costs: {e}")
        
        # Extract consensus cost from apis_clean_json.json
        consensus_json_path = os.path.join(folder, "apis_clean_json.json")
        if os.path.exists(consensus_json_path):
            try:
                with open(consensus_json_path, 'r', encoding='utf-8') as f:
                    consensus_data = json.load(f)
                
                # Look for cost in cost_tracking section
                if 'cost_tracking' in consensus_data:
                    consensus_cost = float(consensus_data['cost_tracking'].get('total_cost', 0))
                elif 'total_cost' in consensus_data:
                    consensus_cost = float(consensus_data.get('total_cost', 0))
                    
            except Exception as e:
                print(f"      ⚠️ Error reading consensus costs: {e}")
        
        # Extract topics cost from llm_topics_json.json
        topics_json_path = os.path.join(folder, "llm_topics_json.json")
        if os.path.exists(topics_json_path):
            try:
                with open(topics_json_path, 'r', encoding='utf-8') as f:
                    topics_data = json.load(f)
                
                # Look for cost in cost_tracking section
                if 'cost_tracking' in topics_data:
                    topics_cost = float(topics_data['cost_tracking'].get('total_cost', 0))
                elif 'total_cost' in topics_data:
                    topics_cost = float(topics_data.get('total_cost', 0))
                    
            except Exception as e:
                print(f"      ⚠️ Error reading topics costs: {e}")
        
        # Extract questions cost (Phase 4) - might not exist in all articles
        questions_json_path = os.path.join(folder, "questions_json.json")
        if os.path.exists(questions_json_path):
            try:
                with open(questions_json_path, 'r', encoding='utf-8') as f:
                    questions_data = json.load(f)
                
                # Look for cost in cost_tracking section
                if 'cost_tracking' in questions_data:
                    questions_cost = float(questions_data['cost_tracking'].get('total_cost', 0))
                elif 'total_cost' in questions_data:
                    questions_cost = float(questions_data.get('total_cost', 0))
                    
            except Exception as e:
                print(f"      ⚠️ Error reading questions costs: {e}")
        
        # Calculate total cost
        total_cost = vision_cost + consensus_cost + topics_cost + questions_cost
        
        # Add to lists
        costs.append(total_cost)
        vision_costs.append(vision_cost)
        topics_costs.append(topics_cost)
        consensus_costs.append(consensus_cost)
        questions_costs.append(questions_cost)
        labels.append(f"Art{article_num}")
        
        print(f"      💰 Total: ${total_cost:.6f} (V:${vision_cost:.6f}, T:${topics_cost:.6f}, C:${consensus_cost:.6f}, Q:${questions_cost:.6f})")
    
    return {
        'costs': costs,
        'vision_costs': vision_costs,
        'topics_costs': topics_costs,
        'consensus_costs': consensus_costs,
        'questions_costs': questions_costs,
        'labels': labels
    }

def create_cost_bar_chart(chart_data: Dict) -> Optional[bytes]:
    """
    Create cost analysis bar chart following the exact same pattern as word_generator
    """
    if not chart_data['costs']:
        return None
    
    try:
        # Use fast rendering style
        plt.style.use('fast')
        
        # Create figure with same size as word_generator
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Create bars
        x_pos = np.arange(len(chart_data['labels']))
        bars = ax.bar(x_pos, chart_data['costs'], color='steelblue', alpha=0.8, 
                     edgecolor='black', linewidth=0.5)
        
        # Add value labels on bars (only for <15 articles to avoid clutter)
        if len(chart_data['costs']) < 15:
            for i, (bar, value) in enumerate(zip(bars, chart_data['costs'])):
                height = bar.get_height()
                label = f'${value:.4f}'
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       label, ha='center', va='bottom', fontsize=8)
        
        # Add average line
        if len(chart_data['costs']) > 0:
            avg = sum(chart_data['costs']) / len(chart_data['costs'])
            ax.axhline(y=avg, color='red', linestyle='--', alpha=0.7, 
                      label=f'Average: ${avg:.4f}')
            ax.legend()
        
        # Styling - EXACT same as word_generator
        ax.set_xlabel('Articles', fontsize=12)
        ax.set_ylabel('Cost (USD)', fontsize=12)
        ax.set_title('Processing Cost Analysis by Article', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(chart_data['labels'], rotation=45, ha='right')
        
        # Grid
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Tight layout
        plt.tight_layout()
        
        # Save to bytes
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        plt.close()
        
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        print(f"❌ Error creating cost chart: {e}")
        return None

def generate_cost_legend(chart_data: Dict) -> str:
    """
    Generate cost legend following the EXACT same pattern as word_generator.py lines 243-254
    """
    costs = chart_data['costs']
    vision_costs = chart_data['vision_costs']
    topics_costs = chart_data['topics_costs']
    consensus_costs = chart_data['consensus_costs']
    questions_costs = chart_data['questions_costs']
    
    if not costs:
        return "Figure 2. No cost data available for this project."
    
    # Calculate comprehensive cost statistics (4 phases) - EXACT same as word_generator
    total_cost = sum(costs)
    avg_cost = total_cost / len(costs) if len(costs) > 0 else 0
    min_cost = min(costs) if costs else 0
    max_cost = max(costs) if costs else 0
    vision_total = sum(vision_costs)
    topics_total = sum(topics_costs)
    consensus_total = sum(consensus_costs)
    questions_total = sum(questions_costs) if questions_costs else 0
    articles_with_cost = sum(1 for c in costs if c > 0)
    articles_zero_cost = len(costs) - articles_with_cost
    
    vision_pct = (vision_total / total_cost * 100) if total_cost > 0 else 0
    topics_pct = (topics_total / total_cost * 100) if total_cost > 0 else 0
    consensus_pct = (consensus_total / total_cost * 100) if total_cost > 0 else 0
    questions_pct = (questions_total / total_cost * 100) if total_cost > 0 else 0
    cost_efficiency = total_cost / articles_with_cost if articles_with_cost > 0 else 0
    
    # Technical figure legend with comprehensive metrics (4 phases) - EXACT same format
    cost_text = (
        f"Figure 2. Cost distribution across processing phases for {len(costs)} articles. "
        f"Total cost: ${total_cost:.6f}. Vision: ${vision_total:.6f} ({vision_pct:.2f}%), "
        f"Topics: ${topics_total:.6f} ({topics_pct:.2f}%), "
        f"Consensus: ${consensus_total:.6f} ({consensus_pct:.2f}%), "
        f"Questions: ${questions_total:.6f} ({questions_pct:.2f}%). "
        f"Average cost per article: ${avg_cost:.6f}. "
        f"Range: ${min_cost:.6f} - ${max_cost:.6f}. "
        f"Articles with cost data: {articles_with_cost}/{len(costs)} ({articles_with_cost/len(costs)*100:.2f}%). "
        f"Cost efficiency: ${cost_efficiency:.6f} per successful extraction. "
        f"Zero-cost articles: {articles_zero_cost} (processing failures)."
    )
    
    return cost_text

def main():
    """
    Main function to generate cost chart and legend
    """
    print("🚀 INFINITY RESEARCH - Cost Chart Generator")
    print("=" * 50)
    
    # Change to infinity-research-paper directory
    if os.path.exists("infinity-research-paper"):
        os.chdir("infinity-research-paper")
        print("📁 Changed to infinity-research-paper directory")
    
    # Extract cost data
    chart_data = extract_cost_data_from_articles()
    
    if not chart_data['costs']:
        print("❌ No cost data found!")
        return
    
    print(f"\n📊 Summary:")
    print(f"   Articles processed: {len(chart_data['costs'])}")
    print(f"   Total cost: ${sum(chart_data['costs']):.6f}")
    print(f"   Average cost: ${sum(chart_data['costs'])/len(chart_data['costs']):.6f}")
    
    # Generate chart
    print("\n🎨 Generating cost chart...")
    chart_bytes = create_cost_bar_chart(chart_data)
    
    if chart_bytes:
        # Save chart
        with open("plots/cost_chart.png", "wb") as f:
            f.write(chart_bytes)
        print("   ✅ Chart saved: plots/cost_chart.png")
    else:
        print("   ❌ Failed to generate chart")
    
    # Generate legend
    print("\n📝 Generating cost legend...")
    legend_text = generate_cost_legend(chart_data)
    
    # Save legend
    with open("plots/cost_legend.txt", "w", encoding='utf-8') as f:
        f.write(legend_text)
    print("   ✅ Legend saved: plots/cost_legend.txt")
    
    print(f"\n🎯 Cost chart generation complete!")
    print(f"   📊 Chart: plots/cost_chart.png")
    print(f"   📝 Legend: plots/cost_legend.txt")

if __name__ == "__main__":
    main()