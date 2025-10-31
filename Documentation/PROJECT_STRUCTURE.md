# Project Structure for Azure Functions Deployment

## Directory Structure

```
StockAnalysis/
├── StockAnalyser_Final.py          # Main analysis code (your existing file)
├── function_app.py                 # Azure Functions entry point
├── requirements.txt                # Python dependencies
├── host.json                       # Azure Functions host configuration
├── local.settings.json             # Local development settings (DO NOT COMMIT)
├── .gitignore                      # Git ignore rules
│
├── StockAnalysisTimer/             # Timer trigger function folder
│   └── function.json               # Timer function config
│
├── holdings_with_changes_14_Aug.csv  # Input CSV file
├── charts/                         # Output charts directory
│   └── (generated *.png files)
│
├── OUTPUT_*.xlsx                   # Generated Excel outputs (gitignored)
│
├── DEPLOYMENT_GUIDE.md             # This deployment guide
└── PROJECT_STRUCTURE.md            # Project structure documentation
```

## File Descriptions

### Core Application Files

**StockAnalyser_Final.py**
- Your existing stock analysis code
- Contains all RSI, MACD, PE calculations
- Processes holdings CSV and generates output
- No modifications needed for Azure Functions!

**function_app.py**
- Azure Functions entry point
- Timer trigger function: `StockAnalysisTimer()` - runs daily at scheduled time
- HTTP trigger function: `StockAnalysisManual()` - manual trigger via URL
- Email sending functions
- Calls your `process_holdings_file()` function

### Configuration Files

**requirements.txt**
- All Python dependencies
- Used by Azure to install packages on deployment
- Includes: pandas, yfinance, numpy, matplotlib, openpyxl, requests, etc.

**host.json**
- Azure Functions host configuration
- Sets timeout to 10 minutes (can be increased)
- Configures logging and health monitoring

**local.settings.json**
- **DO NOT COMMIT TO GIT** (in .gitignore)
- Contains local development settings
- Copy to your Azure Function App → Configuration → Application Settings
- Includes email credentials and SMTP settings

**function.json** (in StockAnalysisTimer/)
- Defines the timer trigger
- Schedule format: cron expression
- Links to function_app.py

### Input/Output Files

**holdings_with_changes_14_Aug.csv**
- Your input holdings data
- Must be accessible to Azure Function
- Options: commit to repo, upload to Azure Storage, or use Azure Files

**charts/**
- Directory for generated PNG charts
- Created automatically by matplotlib
- Files: `{TICKER}_chart.png`

**OUTPUT_*.xlsx**
- Generated Excel reports
- Attached to email
- Timestamped with date/time

### Documentation

**DEPLOYMENT_GUIDE.md**
- Step-by-step deployment instructions
- Azure portal setup guide
- Troubleshooting tips
- Configuration examples

**PROJECT_STRUCTURE.md** (this file)
- Overview of project organization
- File descriptions and purposes

## Azure Functions Architecture

### Function App Structure

```
Azure Function App (stockanalysis-xxxxx)
├── Configuration
│   ├── Application Settings (env vars)
│   └── Connection Strings
├── Functions
│   ├── StockAnalysisTimer (timer trigger)
│   └── StockAnalysisManual (HTTP trigger)
├── Deployment Center
│   └── GitHub/DevOps integration
└── Storage Account
    └── Code, logs, temp files
```

### Execution Flow

1. **Timer Trigger** (Daily at 9 AM IST)
   ```
   Azure Scheduler → StockAnalysisTimer() 
   → process_holdings_file() 
   → Generate OUTPUT.xlsx 
   → send_email_with_attachment() 
   → Send to your email
   ```

2. **Manual Trigger** (On-demand)
   ```
   HTTP POST /api/run 
   → StockAnalysisManual() 
   → Same process as above
   ```

### Dependencies Flow

```
requirements.txt 
→ pip install (on deployment)
→ Python packages installed in Azure
→ StockAnalyser_Final.py uses packages
→ function_app.py imports StockAnalyser_Final
→ Azure Functions executes
```

## Environment Variables

These settings are configured in Azure Portal:

| Variable | Example | Purpose |
|----------|---------|---------|
| SMTP_SERVER | smtp.gmail.com | Email server |
| SMTP_PORT | 587 | Email port |
| SENDER_EMAIL | your@gmail.com | From address |
| SENDER_PASSWORD | xxxx xxxx xxxx xxxx | App password |
| RECIPIENT_EMAIL | your@gmail.com | To address |
| AzureWebJobsStorage | Connection string | Auto-generated |
| FUNCTIONS_WORKER_RUNTIME | python | Runtime version |

## Deployment Checklist

- [ ] Code committed to GitHub repository
- [ ] Azure Function App created
- [ ] Deployment Center connected to GitHub
- [ ] Environment variables configured
- [ ] CSV file uploaded/accessible
- [ ] Timer schedule set correctly
- [ ] Test function executed successfully
- [ ] Email received with attachment

## Repository Setup

### Separate Repository Structure

Create a new repository (e.g., `stock-analysis-azure-function`):

```
stock-analysis-azure-function/
├── .git/
├── .gitignore
├── README.md
├── StockAnalyser_Final.py
├── function_app.py
├── requirements.txt
├── host.json
├── local.settings.json.example
├── StockAnalysisTimer/
│   └── function.json
├── holdings_with_changes_14_Aug.csv
├── DEPLOYMENT_GUIDE.md
└── PROJECT_STRUCTURE.md
```

### Git Workflow

1. **Initialize repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial Azure Functions setup"
   ```

2. **Connect to GitHub:**
   ```bash
   git remote add origin https://github.com/yourusername/stock-analysis-azure-function.git
   git push -u origin main
   ```

3. **Azure auto-deploys** on every push

### Keeping Separate Repos Synchronized

If you have two repositories:
- **Repo 1**: Original web app (untouched)
- **Repo 2**: Azure Functions deployment (this one)

**Benefits:**
- Independent deployment cycles
- Different access controls
- Separate versioning
- No interference between projects

## Testing Workflow

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Run locally
func start
```

### Azure Testing
```bash
# Deploy
func azure functionapp publish stockanalysis-xxxxx

# Monitor logs
func azure functionapp logstream stockanalysis-xxxxx
```

## Next Steps

1. Review this structure
2. Create new GitHub repository
3. Push code to repository
4. Follow DEPLOYMENT_GUIDE.md
5. Test locally
6. Deploy to Azure
7. Configure email
8. Run first test
9. Monitor results

