#!/usr/bin/env python3
"""
Investment Report Generator
生成完整的 Berkshire Hathaway 投资分析报告
"""

import json
import os
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
REPORT_DIR = Path(__file__).parent.parent / "reports"
REPORT_DIR.mkdir(exist_ok=True)


def load_latest_data():
    """加载最新数据"""
    data = {}
    
    # 13F 持仓
    f13f_file = DATA_DIR / "latest_13f.json"
    if f13f_file.exists():
        with open(f13f_file, "r") as f:
            holdings = json.load(f)
            # 兼容列表格式
            if isinstance(holdings, list):
                data["holdings_list"] = holdings
                data["holdings"] = {"holdings": holdings, "date": datetime.now().strftime("%Y-%m-%d")}
            else:
                data["holdings"] = holdings
    
    # 新闻
    news_file = DATA_DIR / "latest_news.json"
    if news_file.exists():
        with open(news_file, "r") as f:
            data["news"] = json.load(f)
    
    # 汇总
    summary_file = DATA_DIR / "summary.json"
    if summary_file.exists():
        with open(summary_file, "r") as f:
            data["summary"] = json.load(f)
    
    return data


def generate_markdown_report(data):
    """生成 Markdown 报告"""
    
    report = f"""# 📊 Berkshire Hathaway 投资监控报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📈 持仓概览

"""
    
    if "summary" in data:
        summary = data["summary"]
        report += f"""
| 指标 | 数值 |
|------|------|
| 报告期 | {summary.get('report_date', 'N/A')} |
| 公司名称 | {summary.get('company', 'Berkshire Hathaway')} |
| 持仓数量 | {summary.get('total_holdings', 'N/A')} |
| 数据生成时间 | {summary.get('generated_at', 'N/A')} |

"""
    
    if "holdings" in data and data["holdings"]:
        holdings = data["holdings"]
        holdings_list = data.get("holdings_list", [])
        
        if isinstance(holdings, dict):
            holdings_date = holdings.get('date', 'N/A')
            holdings_company = holdings.get('company', 'Berkshire Hathaway')
            holdings_items = holdings.get('holdings', [])
        else:
            holdings_date = 'N/A'
            holdings_company = 'Berkshire Hathaway'
            holdings_items = []
        
        report += f"""
### 持仓明细

**公司**: {holdings_company}
**报告期**: {holdings_date}

"""
        if holdings_list:
            report += f"| 股票代码 | 公司名称 | 持仓价值 | 股份数 |\n"
            report += f"|----------|----------|----------|--------|\n"
            for h in holdings_list[:10]:
                value_str = f"${h.get('value', 0)/1e9:.2f}B" if h.get('value', 0) > 1e9 else f"${h.get('value', 0)/1e6:.2f}M"
                shares_str = f"{h.get('shares', 0)/1e6:.2f}M" if h.get('shares', 0) > 1e6 else str(h.get('shares', 0))
                report += f"| {h.get('ticker', 'N/A')} | {h.get('name', 'N/A')[:30]} | {value_str} | {shares_str} |\n"
            report += "\n"
        
        report += "> 📝 注: 完整持仓数据请查看 `data/latest_13f.json` 文件\n\n"
    else:
        report += """
> ⚠️ 暂无持仓数据，请先运行 `python src/fetch_13f.py` 抓取数据

"""
    
    if "news" in data and data["news"]:
        report += f"""
---

## 📰 最新新闻 ({len(data['news'])} 条)

"""
        for i, article in enumerate(data["news"][:10], 1):
            report += f"""
### {i}. {article.get('title', 'N/A')}

- **来源**: {article.get('source', 'N/A')}
- **链接**: [查看原文]({article.get('link', '#')})
- **时间**: {article.get('published', article.get('updated', 'N/A'))}

"""
    
    report += f"""
---

## 🔧 自动化信息

- **数据目录**: `data/`
- **报告目录**: `reports/`
- **最后更新**: {datetime.now().isoformat()}

## 📌 后续步骤

1. 运行 `python src/fetch_13f.py` 抓取最新持仓
2. 运行 `python src/news_monitor.py` 更新新闻
3. 运行 `python src/visualize.py` 生成图表
4. 提交变更到 GitHub: `git add . && git commit -m "Update: {datetime.now().strftime('%Y-%m-%d')}"`

---

*此报告由 investrepo 自动生成*
"""
    
    return report


def save_report(report, filename=None):
    """保存报告"""
    if filename is None:
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    filepath = REPORT_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)
    
    logger.info(f"报告已保存: {filepath}")
    
    # 同时保存为 latest.md
    latest_path = REPORT_DIR / "latest.md"
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    logger.info(f"最新报告: {latest_path}")
    
    return filepath


def main():
    logger.info("="*50)
    logger.info("生成投资监控报告")
    logger.info("="*50)
    
    # 加载数据
    data = load_latest_data()
    
    if not data:
        logger.warning("没有找到数据，生成空白报告")
        data = {}
    
    # 生成报告
    report = generate_markdown_report(data)
    
    # 保存
    filepath = save_report(report)
    
    print(f"\n✅ 报告已生成: {filepath}")
    print(f"\n{report}")
    
    return report


if __name__ == "__main__":
    main()
