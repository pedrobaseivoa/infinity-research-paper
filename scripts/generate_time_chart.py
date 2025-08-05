#!/usr/bin/env python3
"""
📊 TIME CHART GENERATOR - Infinity Research Paper
=================================================

Generates the processing time chart and legend following the exact same pattern 
as the word_generator.py from the core system.

Input: JSON files from infinity-research-paper/json/Article_XX/
Output: time_chart.png + time_legend.txt
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

def extract_time_data_from_articles() -> Dict:
    """
    Extract processing time data from all articles following the same pattern as word_generator
    """
    print("📊 Extracting time data from article JSONs...")
    
    # Initialize lists for chart data (4 phases)
    times = []
    vision_times = []
    topics_times = []
    apis_times = []  # Consensus + APIs processing
    questions_times = []
    labels = []
    
    # Get all article folders in order
    article_folders = glob.glob("json/Article_*")
    article_folders.sort()
    
    print(f"📁 Found {len(article_folders)} article folders")
    
    for folder in article_folders:
        folder_name = os.path.basename(folder)
        article_num = int(folder_name.split('_')[1])
        
        print(f"   Processing {folder_name}...")
        
        # Initialize times for this article (in milliseconds, will convert to seconds)
        vision_time = 0
        apis_time = 0  # This includes consensus processing
        topics_time = 0
        questions_time = 0
        
        # 🎯 FIXED: Extract times from final_json.json (same as platform database query)
        final_json_path = os.path.join(folder, "final_json.json")
        if os.path.exists(final_json_path):
            try:
                with open(final_json_path, 'r', encoding='utf-8') as f:
                    final_data = json.load(f)
                
                # Extract times exactly like the platform database query does:
                # CAST(COALESCE(final_json->'vision_json'->>'processing_time_ms', '0') AS INTEGER) as vision_time,
                # CAST(COALESCE(final_json->'apis_clean_json'->>'processing_time_ms', '0') AS INTEGER) as apis_time,
                # CAST(COALESCE(final_json->'llm_topics_json'->>'processing_time_ms', '0') AS INTEGER) as topics_time,
                
                vision_time = int(final_data.get('vision_json', {}).get('processing_time_ms', 0))
                apis_time = int(final_data.get('apis_clean_json', {}).get('processing_time_ms', 0))
                topics_time = int(final_data.get('llm_topics_json', {}).get('processing_time_ms', 0))
                questions_time = int(final_data.get('questions_json', {}).get('processing_time_ms', 0))
                    
            except Exception as e:
                print(f"      ⚠️ Error reading final_json time data: {e}")
        
        # Calculate total time (in milliseconds)
        total_time = vision_time + apis_time + topics_time + questions_time
        
        # Add to lists (keep in milliseconds for calculations, will convert for display)
        times.append(total_time)
        vision_times.append(vision_time)
        apis_times.append(apis_time)
        topics_times.append(topics_time)
        questions_times.append(questions_time)
        labels.append(f"Art{article_num}")
        
        print(f"      ⏱️ Total: {total_time/1000:.1f}s (V:{vision_time/1000:.1f}s, A:{apis_time/1000:.1f}s, T:{topics_time/1000:.1f}s, Q:{questions_time/1000:.1f}s)")
    
    return {
        'times': times,
        'vision_times': vision_times,
        'apis_times': apis_times,
        'topics_times': topics_times,
        'questions_times': questions_times,
        'labels': labels
    }

def create_time_bar_chart(chart_data: Dict) -> Optional[bytes]:
    """
    Create processing time bar chart following the exact same pattern as word_generator
    """
    if not chart_data['times']:
        return None
    
    try:
        # Use fast rendering style
        plt.style.use('fast')
        
        # Create figure with same size as word_generator
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Convert milliseconds to seconds for chart display
        times_in_seconds = [t / 1000 for t in chart_data['times']]
        
        # Create bars
        x_pos = np.arange(len(chart_data['labels']))
        bars = ax.bar(x_pos, times_in_seconds, color='darkorange', alpha=0.8, 
                     edgecolor='black', linewidth=0.5)
        
        # Add value labels on bars (only for <15 articles to avoid clutter)
        if len(times_in_seconds) < 15:
            for i, (bar, value) in enumerate(zip(bars, times_in_seconds)):
                height = bar.get_height()
                label = f'{value:.1f}s'
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       label, ha='center', va='bottom', fontsize=8)
        
        # Add average line
        if len(times_in_seconds) > 0:
            avg = sum(times_in_seconds) / len(times_in_seconds)
            ax.axhline(y=avg, color='red', linestyle='--', alpha=0.7, 
                      label=f'Average: {avg:.1f}s')
            ax.legend()
        
        # Styling - EXACT same as word_generator
        ax.set_xlabel('Articles', fontsize=12)
        ax.set_ylabel('Time (seconds)', fontsize=12)
        ax.set_title('Processing Time Analysis by Article', fontsize=14, fontweight='bold', pad=20)
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
        print(f"❌ Error creating time chart: {e}")
        return None

def generate_time_legend(chart_data: Dict) -> str:
    """
    Generate time legend following the same pattern as cost legend
    """
    times = chart_data['times']
    vision_times = chart_data['vision_times']
    apis_times = chart_data['apis_times']
    topics_times = chart_data['topics_times']
    questions_times = chart_data['questions_times']
    
    if not times:
        return "Figure 4. No processing time data available for this project."
    
    # Calculate comprehensive time statistics (4 phases) - convert ms to seconds
    total_time = sum(times) / 1000  # Convert to seconds
    avg_time = total_time / len(times) if len(times) > 0 else 0
    min_time = min(times) / 1000 if times else 0
    max_time = max(times) / 1000 if times else 0
    vision_total = sum(vision_times) / 1000
    apis_total = sum(apis_times) / 1000
    topics_total = sum(topics_times) / 1000
    questions_total = sum(questions_times) / 1000 if questions_times else 0
    articles_with_time = sum(1 for t in times if t > 0)
    articles_zero_time = len(times) - articles_with_time
    
    vision_pct = (vision_total / total_time * 100) if total_time > 0 else 0
    apis_pct = (apis_total / total_time * 100) if total_time > 0 else 0
    topics_pct = (topics_total / total_time * 100) if total_time > 0 else 0
    questions_pct = (questions_total / total_time * 100) if total_time > 0 else 0
    time_efficiency = total_time / articles_with_time if articles_with_time > 0 else 0
    
    # Technical figure legend with comprehensive metrics (4 phases)
    time_text = (
        f"Figure 4. Processing time performance analysis for {len(times)} articles. "
        f"Total processing time: {total_time:.1f} seconds ({total_time/60:.1f} minutes). "
        f"Vision: {vision_total:.1f}s ({vision_pct:.2f}%), "
        f"Topics: {topics_total:.1f}s ({topics_pct:.2f}%), "
        f"APIs+Consensus: {apis_total:.1f}s ({apis_pct:.2f}%), "
        f"Questions: {questions_total:.1f}s ({questions_pct:.2f}%). "
        f"Average time per article: {avg_time:.1f} seconds. "
        f"Range: {min_time:.1f}s - {max_time:.1f}s. "
        f"Articles with time data: {articles_with_time}/{len(times)} ({articles_with_time/len(times)*100:.2f}%). "
        f"Time efficiency: {time_efficiency:.1f}s per successful extraction. "
        f"Zero-time articles: {articles_zero_time} (processing failures). "
        f"System achieved {len(times)/total_time*60:.1f} articles per minute throughput."
    )
    
    return time_text

def main():
    """
    Main function to generate time chart and legend
    """
    print("🚀 INFINITY RESEARCH - Time Chart Generator")
    print("=" * 50)
    
    # Change to infinity-research-paper directory
    if os.path.exists("infinity-research-paper"):
        os.chdir("infinity-research-paper")
        print("📁 Changed to infinity-research-paper directory")
    
    # Extract time data
    chart_data = extract_time_data_from_articles()
    
    if not chart_data['times']:
        print("❌ No time data found!")
        return
    
    total_seconds = sum(chart_data['times']) / 1000
    print(f"\n📊 Summary:")
    print(f"   Articles processed: {len(chart_data['times'])}")
    print(f"   Total time: {total_seconds:.1f} seconds ({total_seconds/60:.1f} minutes)")
    print(f"   Average time: {total_seconds/len(chart_data['times']):.1f} seconds")
    
    # Generate chart
    print("\n🎨 Generating time chart...")
    chart_bytes = create_time_bar_chart(chart_data)
    
    if chart_bytes:
        # Save chart
        with open("plots/time_chart.png", "wb") as f:
            f.write(chart_bytes)
        print("   ✅ Chart saved: plots/time_chart.png")
    else:
        print("   ❌ Failed to generate chart")
    
    # Generate legend
    print("\n📝 Generating time legend...")
    legend_text = generate_time_legend(chart_data)
    
    # Save legend
    with open("plots/time_legend.txt", "w", encoding='utf-8') as f:
        f.write(legend_text)
    print("   ✅ Legend saved: plots/time_legend.txt")
    
    print(f"\n🎯 Time chart generation complete!")
    print(f"   📊 Chart: plots/time_chart.png")
    print(f"   📝 Legend: plots/time_legend.txt")

if __name__ == "__main__":
    main()