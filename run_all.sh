#!/bin/bash
# Berkshire Hathaway Investment Monitor
# 一键运行所有脚本

set -e

echo "=========================================="
echo "Berkshire Hathaway 投资监控"
echo "=========================================="

# 进入脚本目录
cd "$(dirname "$0")"

echo ""
echo "📊 抓取 13F 持仓数据..."
python3 src/fetch_13f.py

echo ""
echo "📰 抓取新闻..."
python3 src/news_monitor.py

echo ""
echo "📝 生成报告..."
python3 src/generate_report.py

echo ""
echo "📈 生成可视化..."
python3 src/visualize.py

echo ""
echo "=========================================="
echo "✅ 完成!"
echo "=========================================="
echo ""
echo "📁 查看报告: reports/latest.md"
echo "📊 查看图表: reports/*.png"
