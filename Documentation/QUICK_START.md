# Quick Start Guide - 15 Minutes to Live

Get your stock analysis running on Azure Functions in 15 minutes!

## ⚡ Rapid Deployment

### Step 1: Create Azure Function App (3 min)

1. Go to [portal.azure.com](https://portal.azure.com)
2. Click **"Create a resource"**
3. Search **"Function App"** → Click **Create**
4. Fill in:
   - **Subscription**: Your subscription
   - **Resource Group**: `stock-analysis-rg` (create new)
   - **Function App name**: `stockanalysis-YOURNAME` (must be unique)
   - **Publish**: `Code`
   - **Runtime stack**: `Python`
   - **Version**: `3.10` or `3.11`
   - **Region**: `East US` or `India Central`
   - **Operating System**: `Linux`
   - **Plan Type**: `Consumption (Serverless)`
5. Click **"Review + create"** → **Create**
6. Wait 2 minutes for deployment

### Step 2: Setup GitHub Repository (2 min)

1. Create a **NEW** repository on GitHub:
   - Name: `stock-analysis-azure`
   - Visibility: Private (recommended)
   - Don't initialize with README

2. Push this code to it:
   ```bash
   # In your local project directory
   git init
   git add .
   git commit -m "Initial Azure Functions setup"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/stock-analysis-azure.git
   git push -u origin main
   ```

### Step 3: Connect Azure to GitHub (2 min)

1. In Azure Portal, go to your Function App
2. Click **Deployment Center** (left sidebar)
3. Choose **External** → **GitHub**
4. Authorize Azure access to GitHub
5. Select:
   - **Organization**: Your username
   - **Repository**: `stock-analysis-azure`
   - **Branch**: `main`
6. Click **Save**

Azure will auto-deploy your code! (Takes 2-3 minutes)

### Step 4: Configure Email (3 min)

1. **Get Gmail App Password:**
   - Go to [myaccount.google.com](https://myaccount.google.com)
   - Security → Enable **2-Step Verification** (if not already)
   - Security → **App passwords** → Generate
   - Select **Mail** and **Other**
   - Save the 16-character password

2. **Add to Azure:**
   - Function App → **Configuration** → **Application settings**
   - Click **"+ New application setting"**
   - Add these 5 settings:
     ```
     SMTP_SERVER = smtp.gmail.com
     SMTP_PORT = 587
     SENDER_EMAIL = your-email@gmail.com
     SENDER_PASSWORD = xxxx xxxx xxxx xxxx (your app password)
     RECIPIENT_EMAIL = your-email@gmail.com
     ```
   - Click **Save**

### Step 5: Add CSV File (2 min)

**Option A: Commit to Repository**
```bash
# Copy your CSV to the project folder
cp /path/to/holdings_with_changes_14_Aug.csv .
git add holdings_with_changes_14_Aug.csv
git commit -m "Add holdings CSV"
git push
```

**Option B: Azure Storage (if file is large)**
- Upload to Azure Blob Storage
- Update path in function_app.py

### Step 6: Test! (3 min)

1. Go to Function App → **Functions**
2. Click **StockAnalysisTimer**
3. Click **"Test/Run"** (right side)
4. Click **"Run"** button
5. Watch logs scroll...
6. Check your email! 📧

## ✅ Verification Checklist

- [ ] Function deployed (no errors in Deployment Center)
- [ ] Email settings configured
- [ ] CSV file accessible
- [ ] Test run completed successfully
- [ ] Email received with Excel attachment
- [ ] Timer schedule correct (in function_app.py)

## 🎯 Set Your Schedule

Default: 9:00 AM UTC (3:30 PM IST)

To change, edit `function_app.py` line 17:
```python
@app.timer_trigger(schedule="30 12 * * *", ...)  # 12:30 UTC = 6 PM IST
```

Restart function or wait for auto-deploy.

## 🐛 Common Issues

**"File not found"**
- Check CSV file is in repository
- Verify path in function_app.py line 42

**"Email not sending"**
- Verify App Password (not regular password)
- Check all 5 settings are added correctly

**"Import errors"**
- Wait for deployment to complete (3-5 min)
- Check Function App → Deployment Center shows "Success"

**"Function not running"**
- Check Monitor tab for errors
- Verify timer schedule syntax

## 📊 What Happens Next

Every day at your scheduled time:
1. ✅ Timer triggers automatically
2. ✅ Reads your holdings CSV
3. ✅ Fetches latest stock data
4. ✅ Calculates RSI, MACD, PE
5. ✅ Generates charts
6. ✅ Creates Excel report
7. ✅ Emails it to you!

**You'll receive an email like:**
```
Subject: Stock Analysis Report - 23 Jan 2025 15:30

Hello,

Please find attached the daily stock analysis report.

Generated on: 23 Jan 2025 at 15:30 IST
```

## 🔗 Useful Links

- **Azure Portal**: [portal.azure.com](https://portal.azure.com)
- **Monitor Logs**: Function App → Functions → Monitor
- **Deployment Status**: Function App → Deployment Center
- **Application Settings**: Function App → Configuration

## 💰 Cost Check

**FREE TIER:** 1M executions/month

Your usage:
- 30 days × 1 run/day = 30 executions
- **COST: $0** ✅

## 🎉 You're Done!

Your stock analysis now runs automatically every day!

**Next Steps:**
- Customize the schedule
- Add more holdings
- Monitor logs for first week
- Set up error alerts (optional)

---

**Questions?** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed help.

