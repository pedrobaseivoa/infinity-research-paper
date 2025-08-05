#!/usr/bin/env python3
"""
📊 TOKEN CHART GENERATOR - Infinity Research Paper
==================================================

Generates the token usage chart and legend following the exact same pattern 
as the word_generator.py from the core system.

Input: JSON files from infinity-research-paper/json/Article_XX/
Output: token_chart.png + token_legend.txt
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

def extract_token_data_from_articles() -> Dict:
    """
    Extract token data from all articles following the same pattern as word_generator
    """
    print("📊 Extracting token data from article JSONs...")
    
    # Initialize lists for chart data (4 phases)
    tokens = []
    vision_tokens = []
    topics_tokens = []
    consensus_tokens = []
    questions_tokens = []
    labels = []
    
    # Get all article folders in order
    article_folders = glob.glob("json/Article_*")
    article_folders.sort()
    
    print(f"📁 Found {len(article_folders)} article folders")
    
    for folder in article_folders:
        folder_name = os.path.basename(folder)
        article_num = int(folder_name.split('_')[1])
        
        print(f"   Processing {folder_name}...")
        
        # Initialize tokens for this article
        vision_token = 0
        consensus_token = 0
        topics_token = 0
        questions_token = 0
        
        # Extract vision tokens from vision_json.json
        vision_json_path = os.path.join(folder, "vision_json.json")
        if os.path.exists(vision_json_path):
            try:
                with open(vision_json_path, 'r', encoding='utf-8') as f:
                    vision_data = json.load(f)
                
                # Look for tokens in cost_tracking section
                if 'cost_tracking' in vision_data:
                    vision_token = int(vision_data['cost_tracking'].get('total_tokens', 0))
                elif 'total_tokens' in vision_data:
                    vision_token = int(vision_data.get('total_tokens', 0))
                    
            except Exception as e:
                print(f"      ⚠️ Error reading vision tokens: {e}")
        
        # Extract consensus tokens from apis_clean_json.json
        consensus_json_path = os.path.join(folder, "apis_clean_json.json")
        if os.path.exists(consensus_json_path):
            try:
                with open(consensus_json_path, 'r', encoding='utf-8') as f:
                    consensus_data = json.load(f)
                
                # Look for tokens in cost_tracking section
                if 'cost_tracking' in consensus_data:
                    consensus_token = int(consensus_data['cost_tracking'].get('total_tokens', 0))
                elif 'total_tokens' in consensus_data:
                    consensus_token = int(consensus_data.get('total_tokens', 0))
                    
            except Exception as e:
                print(f"      ⚠️ Error reading consensus tokens: {e}")
        
        # Extract topics tokens from llm_topics_json.json
        topics_json_path = os.path.join(folder, "llm_topics_json.json")
        if os.path.exists(topics_json_path):
            try:
                with open(topics_json_path, 'r', encoding='utf-8') as f:
                    topics_data = json.load(f)
                
                # Look for tokens in cost_tracking section
                if 'cost_tracking' in topics_data:
                    topics_token = int(topics_data['cost_tracking'].get('total_tokens', 0))
                elif 'total_tokens' in topics_data:
                    topics_token = int(topics_data.get('total_tokens', 0))
                    
            except Exception as e:
                print(f"      ⚠️ Error reading topics tokens: {e}")
        
        # Extract questions tokens (Phase 4) - might not exist in all articles
        questions_json_path = os.path.join(folder, "questions_json.json")
        if os.path.exists(questions_json_path):
            try:
                with open(questions_json_path, 'r', encoding='utf-8') as f:
                    questions_data = json.load(f)
                
                # Look for tokens in cost_tracking section
                if 'cost_tracking' in questions_data:
                    questions_token = int(questions_data['cost_tracking'].get('total_tokens', 0))
                elif 'total_tokens' in questions_data:
                    questions_token = int(questions_data.get('total_tokens', 0))
                    
            except Exception as e:
                print(f"      ⚠️ Error reading questions tokens: {e}")
        
        # Calculate total tokens
        total_token = vision_token + consensus_token + topics_token + questions_token
        
        # Add to lists
        tokens.append(total_token)
        vision_tokens.append(vision_token)
        topics_tokens.append(topics_token)
        consensus_tokens.append(consensus_token)
        questions_tokens.append(questions_token)
        labels.append(f"Art{article_num}")
        
        print(f"      🎯 Total: {total_token:,} tokens (V:{vision_token:,}, T:{topics_token:,}, C:{consensus_token:,}, Q:{questions_token:,})")
    
    return {
        'tokens': tokens,
        'vision_tokens': vision_tokens,
        'topics_tokens': topics_tokens,
        'consensus_tokens': consensus_tokens,
        'questions_tokens': questions_tokens,
        'labels': labels
    }

def create_token_bar_chart(chart_data: Dict) -> Optional[bytes]:
    """
    Create token usage bar chart following the exact same pattern as word_generator
    """
    if not chart_data['tokens']:
        return None
    
    try:
        # Use fast rendering style
        plt.style.use('fast')
        
        # Create figure with same size as word_generator
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Create bars
        x_pos = np.arange(len(chart_data['labels']))
        bars = ax.bar(x_pos, chart_data['tokens'], color='forestgreen', alpha=0.8, 
                     edgecolor='black', linewidth=0.5)
        
        # Add value labels on bars (only for <15 articles to avoid clutter)
        if len(chart_data['tokens']) < 15:
            for i, (bar, value) in enumerate(zip(bars, chart_data['tokens'])):
                height = bar.get_height()
                label = f'{int(value):,}'
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       label, ha='center', va='bottom', fontsize=8)
        
        # Add average line
        if len(chart_data['tokens']) > 0:
            avg = sum(chart_data['tokens']) / len(chart_data['tokens'])
            ax.axhline(y=avg, color='red', linestyle='--', alpha=0.7, 
                      label=f'Average: {avg:,.0f}')
            ax.legend()
        
        # Styling - EXACT same as word_generator
        ax.set_xlabel('Articles', fontsize=12)
        ax.set_ylabel('Tokens', fontsize=12)
        ax.set_title('Token Usage Analysis by Article', fontsize=14, fontweight='bold', pad=20)
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
        print(f"❌ Error creating token chart: {e}")
        return None

def generate_token_legend(chart_data: Dict) -> str:
    """
    Generate token legend following the same pattern as cost legend
    """
    tokens = chart_data['tokens']
    vision_tokens = chart_data['vision_tokens']
    topics_tokens = chart_data['topics_tokens']
    consensus_tokens = chart_data['consensus_tokens']
    questions_tokens = chart_data['questions_tokens']
    
    if not tokens:
        return "Figure 3. No token data available for this project."
    
    # Calculate comprehensive token statistics (4 phases)
    total_tokens = sum(tokens)
    avg_tokens = total_tokens / len(tokens) if len(tokens) > 0 else 0
    min_tokens = min(tokens) if tokens else 0
    max_tokens = max(tokens) if tokens else 0
    vision_total = sum(vision_tokens)
    topics_total = sum(topics_tokens)
    consensus_total = sum(consensus_tokens)
    questions_total = sum(questions_tokens) if questions_tokens else 0
    articles_with_tokens = sum(1 for t in tokens if t > 0)
    articles_zero_tokens = len(tokens) - articles_with_tokens
    
    vision_pct = (vision_total / total_tokens * 100) if total_tokens > 0 else 0
    topics_pct = (topics_total / total_tokens * 100) if total_tokens > 0 else 0
    consensus_pct = (consensus_total / total_tokens * 100) if total_tokens > 0 else 0
    questions_pct = (questions_total / total_tokens * 100) if total_tokens > 0 else 0
    token_efficiency = total_tokens / articles_with_tokens if articles_with_tokens > 0 else 0
    
    # Technical figure legend with comprehensive metrics (4 phases)
    token_text = (
        f"Figure 3. Token consumption distribution across processing phases for {len(tokens)} articles. "
        f"Total consumption: {total_tokens:,} tokens. Vision: {vision_total:,} ({vision_pct:.2f}%), "
        f"Topics: {topics_total:,} ({topics_pct:.2f}%), "
        f"Consensus: {consensus_total:,} ({consensus_pct:.2f}%), "
        f"Questions: {questions_total:,} ({questions_pct:.2f}%). "
        f"Average tokens per article: {avg_tokens:,.0f}. "
        f"Range: {min_tokens:,} - {max_tokens:,}. "
        f"Articles with token data: {articles_with_tokens}/{len(tokens)} ({articles_with_tokens/len(tokens)*100:.2f}%). "
        f"Token efficiency: {token_efficiency:,.0f} per successful extraction. "
        f"Zero-token articles: {articles_zero_tokens} (processing failures)."
    )
    
    return token_text

def main():
    """
    Main function to generate token chart and legend
    """
    print("🚀 INFINITY RESEARCH - Token Chart Generator")
    print("=" * 50)
    
    # Change to infinity-research-paper directory
    if os.path.exists("infinity-research-paper"):
        os.chdir("infinity-research-paper")
        print("📁 Changed to infinity-research-paper directory")
    
    # Extract token data
    chart_data = extract_token_data_from_articles()
    
    if not chart_data['tokens']:
        print("❌ No token data found!")
        return
    
    print(f"\n📊 Summary:")
    print(f"   Articles processed: {len(chart_data['tokens'])}")
    print(f"   Total tokens: {sum(chart_data['tokens']):,}")
    print(f"   Average tokens: {sum(chart_data['tokens'])/len(chart_data['tokens']):,.0f}")
    
    # Generate chart
    print("\n🎨 Generating token chart...")
    chart_bytes = create_token_bar_chart(chart_data)
    
    if chart_bytes:
        # Save chart
        with open("plots/token_chart.png", "wb") as f:
            f.write(chart_bytes)
        print("   ✅ Chart saved: plots/token_chart.png")
    else:
        print("   ❌ Failed to generate chart")
    
    # Generate legend
    print("\n📝 Generating token legend...")
    legend_text = generate_token_legend(chart_data)
    
    # Save legend
    with open("plots/token_legend.txt", "w", encoding='utf-8') as f:
        f.write(legend_text)
    print("   ✅ Legend saved: plots/token_legend.txt")
    
    print(f"\n🎯 Token chart generation complete!")
    print(f"   📊 Chart: plots/token_chart.png")
    print(f"   📝 Legend: plots/token_legend.txt")

if __name__ == "__main__":
    main()