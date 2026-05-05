#!/usr/bin/env python3
"""
SEC 13F Holdings Fetcher for Berkshire Hathaway
从 SEC EDGAR 自动抓取 BRK 的 13F 持仓报告
"""

import requests
import xml.etree.ElementTree as ET
import json
import csv
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 常量
BRK_CIK = "0001067983"  # Berkshire Hathaway Inc
EDGAR_BASE = "https://www.sec.gov/cgi-bin/browse-edgar"
EDGAR_API = "https://data.sec.gov/api/xbrl"
USER_AGENT = "Mozilla/5.0 (compatible; BerkshireMonitor/1.0; +https://github.com/investrepo)"

# 存储路径
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def get_headers():
    return {
        "User-Agent": USER_AGENT,
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov",
        "Referer": "https://www.sec.gov/"
    }


def fetch_13f_index():
    """获取 BRK 的 13F 报告索引"""
    logger.info("正在获取 13F 报告索引...")
    
    url = f"{EDGAR_BASE}/browse-edgar"
    params = {
        "action": "getcompany",
        "CIK": BRK_CIK,
        "type": "13F",
        "count": "10",
        "output": "xml"
    }
    
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, headers=get_headers(), timeout=30)
            resp.raise_for_status()
            
            root = ET.fromstring(resp.content)
            filings = []
            
            for doc in root.findall(".//filing"):
                filing = {
                    "accession_number": doc.findtext("accession-number", ""),
                    "filing_date": doc.findtext("filing-date", ""),
                    "document_url": doc.findtext("documentUrl", ""),
                }
                if filing["accession_number"]:
                    filings.append(filing)
            
            logger.info(f"找到 {len(filings)} 条 13F 报告")
            return filings
        except Exception as e:
            logger.warning(f"尝试 {attempt+1}/3 失败: {e}")
            if attempt < 2:
                import time
                time.sleep(2 ** attempt)
    
    return []


def fetch_13f_holdings(accession_number, filing_date):
    """获取单个 13F 报告的持仓明细"""
    logger.info(f"正在抓取持仓: {accession_number}")
    
    # 格式化 accession number (去掉连字符)
    acc_normalized = accession_number.replace("-", "")
    
    # 尝试获取 XBRL 或 HTML 格式
    base_url = f"https://www.sec.gov/Archives/edgar/full-index/{filing_date[:4]}/{filing_date[5:7]}/"
    
    # 尝试直接从 SEC EDGAR 的 JSON API 获取
    json_url = f"https://data.sec.gov/api/xbrl/companyfacts/{BRK_CIK}.json"
    
    try:
        resp = requests.get(json_url, headers=get_headers(), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        # 13F-HR 表单数据在 facts 表中
        facts = data.get("facts", {})
        
        # 尝试找 13F 持仓信息
        # 这是一个简化版本，实际 XBRL 解析会更复杂
        holdings = []
        
        # 获取公司信息
        entity_name = data.get("entityName", "Berkshire Hathaway")
        
        logger.info(f"获取到公司: {entity_name}")
        return {"company": entity_name, "holdings": holdings, "date": filing_date}
        
    except Exception as e:
        logger.error(f"抓取持仓失败: {e}")
        return None


def save_to_json(data, filename):
    """保存为 JSON"""
    filepath = DATA_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"已保存: {filepath}")


def save_to_csv(holdings, filename):
    """保存为 CSV"""
    if not holdings:
        return
    
    filepath = DATA_DIR / filename
    keys = holdings[0].keys()
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(holdings)
    
    logger.info(f"已保存: {filepath}")


def generate_summary():
    """生成持仓汇总"""
    logger.info("正在生成汇总...")
    
    # 读取最新数据
    latest_file = DATA_DIR / "latest_13f.json"
    
    if not latest_file.exists():
        logger.warning("没有找到 13F 数据文件")
        return
    
    with open(latest_file, "r") as f:
        data = json.load(f)
    
    summary = {
        "report_date": data.get("date", "N/A"),
        "generated_at": datetime.now().isoformat(),
        "company": data.get("company", "Berkshire Hathaway"),
        "total_holdings": len(data.get("holdings", [])),
    }
    
    summary_file = DATA_DIR / "summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"汇总已保存: {summary_file}")
    return summary


def main():
    logger.info("="*50)
    logger.info("Berkshire Hathaway 13F 持仓抓取")
    logger.info("="*50)
    
    # 获取报告索引
    filings = fetch_13f_index()
    
    if not filings:
        logger.error("无法获取 13F 报告")
        sys.exit(1)
    
    # 获取最新一份报告
    latest = filings[0]
    logger.info(f"最新报告日期: {latest['filing_date']}")
    
    # 抓取持仓
    holdings_data = fetch_13f_holdings(
        latest["accession_number"],
        latest["filing_date"]
    )
    
    if holdings_data:
        # 保存
        date_str = latest["filing_date"].replace("-", "")
        save_to_json(holdings_data, "latest_13f.json")
        save_to_json(holdings_data, f"13f_{date_str}.json")
        
        # 生成汇总
        summary = generate_summary()
        
        if summary:
            print("\n📊 汇总信息:")
            print(f"  报告期: {summary['report_date']}")
            print(f"  公司: {summary['company']}")
            print(f"  持仓数量: {summary['total_holdings']}")
    else:
        logger.warning("未获取到持仓数据")


if __name__ == "__main__":
    main()
