# 🏢 Berkshire Hathaway Investment Monitor

监控伯克希尔哈撒韦公司的投资组合变化

## 功能特性

- 📊 **SEC 13F 持仓抓取** — 自动从 SEC EDGAR 获取最新持仓报告
- 📰 **新闻监控** — 追踪 BRK 相关新闻和公告  
- 📈 **持仓可视化** — 生成持仓结构和变化趋势图表
- 📝 **定期报告** — 自动生成 Markdown 格式投资报告

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
```

### 3. 运行

```bash
# 抓取最新 13F 持仓
python src/fetch_13f.py

# 运行新闻监控
python src/news_monitor.py

# 生成完整报告
python src/generate_report.py

# 可视化持仓
python src/visualize.py
```

## 项目结构

```
investrepo/
├── src/
│   ├── fetch_13f.py      # SEC 13F 数据抓取
│   ├── news_monitor.py    # 新闻监控
│   ├── generate_report.py # 报告生成
│   └── visualize.py       # 可视化
├── data/                  # 数据存储
├── reports/               # 生成的报告
├── configs/               # 配置文件
├── .env.example           # 环境变量模板
├── requirements.txt
└── README.md
```

## 自动化

项目包含 GitHub Actions 配置，可自动：
- 每周抓取最新持仓数据
- 每日检查新闻更新
- 自动生成报告并提交到仓库

## 数据来源

- [SEC EDGAR](https://www.sec.gov/) — 官方监管 filings
- [WhaleWisdom](https://whalewisdom.com) — 机构持仓数据
- Yahoo Finance — 实时行情

## 免责声明

本工具仅供学习和研究使用，投资决策请自行负责。
