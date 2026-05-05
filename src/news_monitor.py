#!/usr/bin/env python3
"""
News Monitor for Berkshire Hathaway
监控 BRK 相关新闻和公告
"""

import requests
import feedparser
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 常量
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# RSS 订阅源
RSS_FEEDS = {
    "yahoo_finance": "https://finance.yahoo.com/news/rssindex",
    "reuters_brk": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
    "wsj": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "cnbc": "http://www.cnbc.com/id/100003114/device/rss/rss.html",
}

# 搜索 API (免费)
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")


def fetch_rss_feed(name, url):
    """抓取 RSS 源"""
    logger.info(f"抓取 RSS: {name}")
    
    try:
        feed = feedparser.parse(url, agent=USER_AGENT)
        
        entries = []
        for entry in feed.entries[:10]:  # 只取最新10条
            entries.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")[:200],
                "source": name
            })
        
        logger.info(f"  {name}: {len(entries)} 条")
        return entries
        
    except Exception as e:
        logger.error(f"  {name} 抓取失败: {e}")
        return []


def fetch_yahoo_finance():
    """抓取 Yahoo Finance 巴菲特相关新闻"""
    logger.info("抓取 Yahoo Finance BRK 新闻...")
    
    try:
        # Yahoo Finance BRK 新闻页面
        url = "https://finance.yahoo.com/quote/BRK-A/news"
        headers = {"User-Agent": USER_AGENT}
        
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.content, "lxml")
        
        articles = []
        for item in soup.select("li.js-stream-content")[:10]:
            title_elem = item.select_one("h3 a")
            if title_elem:
                articles.append({
                    "title": title_elem.get_text(strip=True),
                    "link": "https://finance.yahoo.com" + title_elem.get("href", ""),
                    "source": "Yahoo Finance"
                })
        
        logger.info(f"  Yahoo Finance: {len(articles)} 条")
        return articles
        
    except Exception as e:
        logger.error(f"  Yahoo Finance 抓取失败: {e}")
        return []


def fetch_sec_updates():
    """抓取 SEC 关于 BRK 的最新更新"""
    logger.info("抓取 SEC EDGAR 更新...")
    
    try:
        url = f"https://www.sec.gov/cgi-bin/browse-edgar"
        params = {
            "action": "getcompany",
            "CIK": "0001067983",
            "count": "10",
            "output": "atom"
        }
        headers = {"User-Agent": "Mozilla/5.0 (compatible; BerkshireMonitor/1.0)"}
        
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.content, "lxml")
        
        filings = []
        for entry in soup.select("entry")[:10]:
            filings.append({
                "title": entry.select_one("title").get_text(strip=True) if entry.select_one("title") else "",
                "updated": entry.select_one("updated").get_text(strip=True) if entry.select_one("updated") else "",
                "link": entry.select_one("link").get("href", "") if entry.select_one("link") else "",
                "source": "SEC EDGAR"
            })
        
        logger.info(f"  SEC EDGAR: {len(filings)} 条")
        return filings
        
    except Exception as e:
        logger.error(f"  SEC EDGAR 抓取失败: {e}")
        return []


def search_google_news():
    """使用 Google 新闻搜索 (通过 RSS)"""
    logger.info("搜索 Google News...")
    
    try:
        # Google News RSS
        url = "https://news.google.com/rss/search?q=Berkshire%20Hathaway&hl=en&gl=US&ceid=US:en"
        feed = feedparser.parse(url, agent=USER_AGENT)
        
        articles = []
        for entry in feed.entries[:15]:
            articles.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": "Google News"
            })
        
        logger.info(f"  Google News: {len(articles)} 条")
        return articles
        
    except Exception as e:
        logger.error(f"  Google News 抓取失败: {e}")
        return []


def save_news(articles, filename="latest_news.json"):
    """保存新闻到文件"""
    filepath = DATA_DIR / filename
    
    # 读取现有数据，避免重复
    existing = []
    if filepath.exists():
        with open(filepath, "r") as f:
            existing = json.load(f)
    
    # 合并并去重 (基于 title)
    existing_titles = {a.get("title", "") for a in existing}
    new_articles = [a for a in articles if a.get("title") not in existing_titles]
    
    all_articles = new_articles + existing
    # 保留最新50条
    all_articles = all_articles[:50]
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)
    
    logger.info(f"已保存 {len(new_articles)} 条新新闻到 {filepath}")
    return new_articles


def generate_news_report():
    """生成新闻报告"""
    news_file = DATA_DIR / "latest_news.json"
    
    if not news_file.exists():
        logger.warning("没有找到新闻文件")
        return
    
    with open(news_file, "r") as f:
        articles = json.load(f)
    
    report = f"""# 📰 Berkshire Hathaway 新闻监控报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 最近动态 ({len(articles)} 条)

"""
    
    for i, article in enumerate(articles[:20], 1):
        report += f"""### {i}. {article.get('title', 'N/A')}

- **来源**: {article.get('source', 'N/A')}
- **链接**: {article.get('link', 'N/A')}
- **时间**: {article.get('published', article.get('updated', 'N/A'))}

---
"""
    
    report_file = DATA_DIR.parent / "reports" / f"news_{datetime.now().strftime('%Y%m%d')}.md"
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    logger.info(f"新闻报告已生成: {report_file}")
    return report


def main():
    logger.info("="*50)
    logger.info("Berkshire Hathaway 新闻监控")
    logger.info("="*50)
    
    all_articles = []
    
    # 抓取各来源新闻
    all_articles.extend(fetch_rss_feeds())
    all_articles.extend(fetch_yahoo_finance())
    all_articles.extend(fetch_sec_updates())
    all_articles.extend(search_google_news())
    
    # 去重并保存
    if all_articles:
        new_count = save_news(all_articles)
        
        # 生成报告
        report = generate_news_report()
        
        print(f"\n📰 本次抓取: {len(all_articles)} 条新闻")
        print(f"📁 数据已保存到: {DATA_DIR}")
    else:
        logger.warning("没有获取到任何新闻")


def fetch_rss_feeds():
    """抓取所有 RSS 源"""
    all_entries = []
    for name, url in RSS_FEEDS.items():
        entries = fetch_rss_feed(name, url)
        all_entries.extend(entries)
    return all_entries


if __name__ == "__main__":
    main()
