#!/usr/bin/env python3
"""
Portfolio Visualizer
生成持仓可视化图表
"""

import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 无 GUI 后端
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "reports"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_holdings_data():
    """加载持仓数据"""
    f13f_file = DATA_DIR / "latest_13f.json"
    
    if not f13f_file.exists():
        logger.warning("没有找到持仓数据")
        return None
    
    with open(f13f_file, "r") as f:
        return json.load(f)


def create_pie_chart(holdings_data):
    """创建持仓饼图"""
    if not holdings_data or "holdings" not in holdings_data:
        logger.warning("没有持仓数据可可视化")
        return
    
    holdings = holdings_data["holdings"]
    
    if not holdings:
        logger.warning("持仓列表为空")
        return
    
    # 取前 10 大持仓
    top_holdings = holdings[:10]
    
    names = [h.get("name", "Unknown")[:20] for h in top_holdings]
    values = [float(h.get("value", 0)) for h in top_holdings]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = plt.cm.Set3(range(len(names)))
    
    wedges, texts, autotexts = ax.pie(
        values, 
        labels=names, 
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )
    
    # 调整标签
    for text in texts:
        text.set_fontsize(9)
    for autotext in autotexts:
        autotext.set_fontsize(8)
    
    ax.set_title(
        f"Berkshire Hathaway Top 10 Holdings\n(as of {holdings_data.get('date', 'N/A')})",
        fontsize=14,
        fontweight='bold'
    )
    
    plt.tight_layout()
    
    filepath = OUTPUT_DIR / "holdings_pie.png"
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    logger.info(f"饼图已保存: {filepath}")
    return filepath


def create_bar_chart(holdings_data):
    """创建持仓柱状图"""
    if not holdings_data or "holdings" not in holdings_data:
        return
    
    holdings = holdings_data["holdings"]
    
    if not holdings:
        return
    
    top_holdings = holdings[:15]
    
    names = [h.get("name", "Unknown")[:15] for h in top_holdings]
    values = [float(h.get("value", 0)) / 1e9 for h in top_holdings]  # 转换为十亿
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors = plt.cm.Blues(range(50, 250, 200 // len(names)))
    
    bars = ax.barh(names, values, color=colors)
    
    ax.set_xlabel("Value (Billions USD)", fontsize=11)
    ax.set_title(
        f"Berkshire Hathaway Holdings\n(as of {holdings_data.get('date', 'N/A')})",
        fontsize=14,
        fontweight='bold'
    )
    
    # 添加数值标签
    for bar, val in zip(bars, values):
        ax.text(val + 0.1, bar.get_y() + bar.get_height()/2, 
                f"${val:.1f}B", va='center', fontsize=9)
    
    ax.invert_yaxis()  # 最大的在上面
    ax.set_xlim(0, max(values) * 1.2)
    
    plt.tight_layout()
    
    filepath = OUTPUT_DIR / "holdings_bar.png"
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    logger.info(f"柱状图已保存: {filepath}")
    return filepath


def create_news_timeline(news_data):
    """创建新闻时间线图表"""
    if not news_data:
        return
    
    # 按来源统计
    sources = {}
    for article in news_data:
        source = article.get("source", "Unknown")
        sources[source] = sources.get(source, 0) + 1
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    labels = list(sources.keys())
    sizes = list(sources.values())
    colors = plt.cm.Pastel1(range(len(labels)))
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct='%1.0f%%',
        colors=colors,
        startangle=90
    )
    
    ax.set_title(
        f"News Sources Distribution\n({len(news_data)} articles)",
        fontsize=14,
        fontweight='bold'
    )
    
    plt.tight_layout()
    
    filepath = OUTPUT_DIR / "news_sources.png"
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    logger.info(f"新闻来源图已保存: {filepath}")
    return filepath


def generate_summary_image(holdings_data, news_data):
    """生成汇总图片"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. 标题
    fig.suptitle(
        "Berkshire Hathaway Investment Monitor\n" + 
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        fontsize=16,
        fontweight='bold',
        y=0.98
    )
    
    # 2. 基本信息
    ax1 = axes[0, 0]
    ax1.axis('off')
    
    if holdings_data:
        info_text = f"""
        📊 Portfolio Summary
        
        Company: {holdings_data.get('company', 'Berkshire Hathaway')}
        Report Date: {holdings_data.get('date', 'N/A')}
        Total Holdings: {len(holdings_data.get('holdings', []))}
        """
    else:
        info_text = "\n\n📊 No holdings data available\n\nPlease run fetch_13f.py first"
    
    ax1.text(0.1, 0.5, info_text, fontsize=14, verticalalignment='center',
             family='monospace', bbox=dict(boxstyle='round', facecolor='lightgray'))
    
    # 3. 新闻统计
    ax2 = axes[0, 1]
    ax2.axis('off')
    
    if news_data:
        news_text = f"""
        📰 News Summary
        
        Total Articles: {len(news_data)}
        Latest Source: {news_data[0].get('source', 'N/A') if news_data else 'N/A'}
        """
    else:
        news_text = "\n\n📰 No news data available\n\nPlease run news_monitor.py first"
    
    ax2.text(0.1, 0.5, news_text, fontsize=14, verticalalignment='center',
             family='monospace', bbox=dict(boxstyle='round', facecolor='lightblue'))
    
    # 4. 持仓饼图
    ax3 = axes[1, 0]
    if holdings_data and holdings_data.get("holdings"):
        holdings = holdings_data["holdings"][:5]
        names = [h.get("name", "Unknown")[:10] for h in holdings]
        values = [float(h.get("value", 1)) for h in holdings]
        
        ax3.pie(values, labels=names, autopct='%1.1f%%', startangle=90)
        ax3.set_title('Top 5 Holdings', fontsize=12, fontweight='bold')
    else:
        ax3.text(0.5, 0.5, 'No Holdings Data', ha='center', va='center', fontsize=12)
        ax3.set_title('Top 5 Holdings', fontsize=12, fontweight='bold')
    
    # 5. 新闻来源
    ax4 = axes[1, 1]
    if news_data:
        sources = {}
        for article in news_data:
            source = article.get("source", "Unknown")
            sources[source] = sources.get(source, 0) + 1
        
        labels = list(sources.keys())[:5]
        sizes = [sources[l] for l in labels]
        
        ax4.bar(labels, sizes, color=plt.cm.Set3(range(len(labels))))
        ax4.set_title('News by Source', fontsize=12, fontweight='bold')
        ax4.tick_params(axis='x', rotation=45)
    else:
        ax4.text(0.5, 0.5, 'No News Data', ha='center', va='center', fontsize=12)
        ax4.set_title('News by Source', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    
    filepath = OUTPUT_DIR / "summary_dashboard.png"
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    logger.info(f"汇总图表已保存: {filepath}")
    return filepath


def main():
    logger.info("="*50)
    logger.info("生成持仓可视化")
    logger.info("="*50)
    
    # 加载数据
    holdings_data = load_holdings_data()
    
    news_file = DATA_DIR / "latest_news.json"
    news_data = []
    if news_file.exists():
        with open(news_file, "r") as f:
            news_data = json.load(f)
    
    # 生成图表
    charts = []
    
    if holdings_data:
        charts.append(create_pie_chart(holdings_data))
        charts.append(create_bar_chart(holdings_data))
    
    if news_data:
        charts.append(create_news_timeline(news_data))
    
    charts.append(generate_summary_image(holdings_data, news_data))
    
    print("\n✅ 可视化完成!")
    print(f"📊 生成图表: {len([c for c in charts if c])} 张")
    for chart in charts:
        if chart:
            print(f"   - {chart}")


if __name__ == "__main__":
    main()
