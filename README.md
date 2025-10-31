# Stock Analysis - Azure Functions

Automated daily stock analysis with email delivery using Azure Functions.

## 🎯 Overview

This project analyzes your stock portfolio daily, calculates technical indicators (RSI, MACD, PE), generates charts, and emails you a comprehensive Excel report - all automatically!

**Key Features:**
- ✅ Daily automated execution
- ✅ Email delivery with Excel reports
- ✅ FREE tier compatible ($0/month)
- ✅ Serverless - no infrastructure management
- ✅ Separate repository from your main web app

## 📁 Project Structure

```
StockAnalysis/
├── 📄 Core Files
│   ├── function_app.py              # Azure Functions entry point
│   ├── StockAnalyser_Final.py       # Main stock analysis logic
│   ├── requirements.txt             # Python dependencies
│   └── host.json                    # Azure Functions config
│
├── 📊 Data Files
│   ├── holdings_with_changes_14_Aug.csv  # Input holdings
│   ├── charts/                      # Generated PNG charts
│   └── Reports/                     # Output Excel files
│
└── 📚 Documentation/
    ├── START_HERE.md                # ← Begin here!
    ├── QUICK_START.md               # 15-min deployment
    ├── DEPLOYMENT_GUIDE.md          # Detailed guide
    └── ... more docs
```

## 🚀 Quick Start

### Prerequisites
- Azure account (free tier OK)
- GitHub account
- Gmail account with App Password

### Deploy in 15 Minutes

1. **Read** → [Documentation/START_HERE.md](Documentation/START_HERE.md)
2. **Follow** → [Documentation/QUICK_START.md](Documentation/QUICK_START.md)
3. **Deploy** → Your `StockResearchFunctionApp` in Azure
4. **Configure** → Email settings
5. **Test** → First run!

## 📖 Documentation

All documentation is in the **[Documentation/](Documentation/)** folder.

### Essential Reading
- **[START_HERE.md](Documentation/START_HERE.md)** - Overview and navigation
- **[QUICK_START.md](Documentation/QUICK_START.md)** - Fast deployment guide
- **[DEPLOY_EXISTING_FUNCTION_APP.md](Documentation/DEPLOY_EXISTING_FUNCTION_APP.md)** - Deploy to your existing Function App

### Reference
- **[DEPLOYMENT_GUIDE.md](Documentation/DEPLOYMENT_GUIDE.md)** - Comprehensive instructions
- **[PROJECT_STRUCTURE.md](Documentation/PROJECT_STRUCTURE.md)** - Architecture details
- **[DEPLOYMENT_CHECKLIST.md](Documentation/DEPLOYMENT_CHECKLIST.md)** - Track progress

## ⚙️ Configuration

### Environment Variables

Configure in Azure Portal → Configuration:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=your-email@gmail.com
```

### Timer Schedule

Default: 9:00 AM UTC (daily)

Edit in `function_app.py` to customize.

## 📧 Email Setup

1. Enable 2-Step Verification in Google Account
2. Generate App Password from Google Account
3. Use App Password in Azure (NOT regular password)

## 💰 Cost

**FREE TIER:**
- 1M executions/month: FREE
- Your usage: ~30/month
- **Total: $0/month** ✅

## 🛠️ Technologies

- **Azure Functions** - Serverless execution
- **Python 3.10+** - Core language
- **yfinance** - Stock data
- **pandas** - Data analysis
- **matplotlib** - Charts
- **openpyxl** - Excel generation

## 📂 Folders

### `/Documentation`
All documentation files

### `/Reports`
Generated Excel files (gitignored)

### `/charts`
PNG chart images (gitignored)

## 🎯 For Existing Function App

You already have **StockResearchFunctionApp**?

See: **[DEPLOY_EXISTING_FUNCTION_APP.md](Documentation/DEPLOY_EXISTING_FUNCTION_APP.md)**

## ✅ Git Ignore

These are excluded from git:
- `Reports/` - Excel output files
- `charts/` - PNG chart images
- `content/` - Local data files
- `*.xlsx` - All Excel files
- `*.png` - All PNG images

## 🆘 Support

- Check **[DEPLOYMENT_GUIDE.md](Documentation/DEPLOYMENT_GUIDE.md)** troubleshooting
- Review Azure Function logs
- Check GitHub Issues

## 📝 License

MIT License - Free to use and modify

---

**Ready to deploy?** Start with **[Documentation/START_HERE.md](Documentation/START_HERE.md)**! 🚀
