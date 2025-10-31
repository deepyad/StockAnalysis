# ✅ Deployment Checklist

Use this checklist to track your deployment progress.

## 📋 Pre-Deployment

### Prerequisites
- [ ] Azure account created and active
- [ ] GitHub account ready
- [ ] Gmail account with 2-Step Verification enabled
- [ ] Downloaded/cloned this repository
- [ ] Read START_HERE.md and chosen deployment path

### Gmail App Password
- [ ] 2-Step Verification enabled in Google Account
- [ ] App Password generated from Google Account
- [ ] 16-character password saved securely

### CSV File Preparation
- [ ] CSV file: `holdings_with_changes_14_Aug.csv` ready
- [ ] File contains valid ticker symbols
- [ ] File location determined (repo OR Azure Storage)

## 🔨 Azure Setup

### Create Function App
- [ ] Logged into Azure Portal
- [ ] Created new Function App
- [ ] Selected Python 3.10 or 3.11
- [ ] Chose Consumption Plan (Serverless)
- [ ] Selected region (India Central / East US)
- [ ] Function App name is unique
- [ ] Resource Group created/selected
- [ ] Deployment completed successfully

### Configure Application Settings
- [ ] Navigated to Configuration → Application settings
- [ ] Added `SMTP_SERVER = smtp.gmail.com`
- [ ] Added `SMTP_PORT = 587`
- [ ] Added `SENDER_EMAIL = your-email@gmail.com`
- [ ] Added `SENDER_PASSWORD = your-app-password`
- [ ] Added `RECIPIENT_EMAIL = your-email@gmail.com`
- [ ] Saved all settings
- [ ] Verified settings persisted

## 📦 GitHub Setup

### Create Repository
- [ ] Created new GitHub repository
- [ ] Named appropriately (e.g., `stock-analysis-azure`)
- [ ] Set visibility (Private recommended)
- [ ] Did NOT initialize with README

### Push Code
- [ ] Initialized git in local project folder
- [ ] Added all files to git
- [ ] Committed with meaningful message
- [ ] Connected to GitHub remote
- [ ] Pushed to GitHub main branch
- [ ] Verified all files in GitHub web UI

### Code Review
- [ ] function_app.py uploaded
- [ ] StockAnalyser_Final.py uploaded
- [ ] requirements.txt uploaded
- [ ] host.json uploaded
- [ ] README.md and docs uploaded

## 🔗 Deployment

### Connect Azure to GitHub
- [ ] Opened Function App → Deployment Center
- [ ] Selected External → GitHub
- [ ] Authorized Azure access to GitHub
- [ ] Selected correct organization/repository
- [ ] Selected main branch
- [ ] Saved deployment configuration
- [ ] Deployment started successfully

### Verify Deployment
- [ ] Deployment completed without errors
- [ ] Deployment Center shows "Success"
- [ ] Functions appear in Function App dashboard
- [ ] All files in correct locations

## 📄 File Management

### CSV File Placement
**Choose ONE method:**

**Method A: Repository (Easiest)**
- [ ] CSV file copied to project folder
- [ ] Committed to git
- [ ] Pushed to GitHub
- [ ] Verified in repository web UI

**Method B: Azure Storage**
- [ ] Created Azure Blob Storage account
- [ ] Uploaded CSV to storage
- [ ] Updated path in function_app.py
- [ ] Redeployed function

**Method C: Azure Files**
- [ ] Created Azure Files share
- [ ] Uploaded CSV file
- [ ] Configured mount point
- [ ] Updated path in function_app.py

## 🧪 Testing

### First Test Run
- [ ] Opened Function App → Functions
- [ ] Clicked StockAnalysisTimer function
- [ ] Opened Test/Run panel
- [ ] Clicked "Run" button
- [ ] Monitored logs for errors
- [ ] Execution completed successfully

### Email Verification
- [ ] Checked email inbox
- [ ] Received stock analysis email
- [ ] Subject line correct
- [ ] Excel file attached
- [ ] Attachment downloaded successfully
- [ ] Excel file opens without errors
- [ ] All stock data present
- [ ] Charts visible in Excel
- [ ] News links working

### Log Review
- [ ] Logs show no errors
- [ ] All stocks processed
- [ ] Charts generated
- [ ] Email sent successfully
- [ ] Execution time reasonable (< 5 min)

## ⚙️ Configuration

### Timer Schedule
- [ ] Reviewed current schedule in function_app.py
- [ ] Verified time zone (UTC)
- [ ] Calculated IST equivalent
- [ ] Adjusted schedule if needed
- [ ] Redeployed if changes made

### Customization (Optional)
- [ ] Modified paths if needed
- [ ] Updated email template if desired
- [ ] Added additional settings
- [ ] Tested customizations

## 📊 Monitoring Setup

### Application Insights
- [ ] Enabled Application Insights (optional)
- [ ] Verified telemetry collection
- [ ] Set up custom dashboards (optional)

### Alerts (Optional)
- [ ] Configured error alerts
- [ ] Set up failure notifications
- [ ] Tested alert system

### Cost Monitoring
- [ ] Set up cost alerts
- [ ] Verified pricing tier
- [ ] Created budget (optional)

## ✅ Production Readiness

### Security
- [ ] No credentials in code
- [ ] All secrets in Azure App Settings
- [ ] .gitignore protects local.settings.json
- [ ] HTTPS only enabled
- [ ] Access control configured

### Reliability
- [ ] Test run successful
- [ ] Error handling working
- [ ] Logs monitored
- [ ] Backup plan considered

### Documentation
- [ ] Deployment documented
- [ ] Customization notes saved
- [ ] Support contacts ready

## 🎯 Go-Live

### Final Verification
- [ ] All tests passed
- [ ] Email received successfully
- [ ] Excel report accurate
- [ ] No errors in logs
- [ ] Timer schedule correct

### Launch
- [ ] Deployment checklist complete
- [ ] Ready for production
- [ ] Scheduled monitoring set up
- [ ] Support resources identified

## 📅 Post-Deployment

### Week 1 Monitoring
- [ ] Daily emails arriving
- [ ] No execution errors
- [ ] Excel files complete
- [ ] Performance acceptable
- [ ] Cost within budget

### Optimization
- [ ] Execution time reviewed
- [ ] Error patterns identified
- [ ] Improvements implemented
- [ ] Schedule adjusted if needed

## 🐛 Troubleshooting (If Needed)

### Common Issues
- [ ] File not found → CSV path verified
- [ ] Import errors → Dependencies checked
- [ ] Email failing → SMTP credentials verified
- [ ] Timeout errors → Schedule/timeout adjusted
- [ ] Timer not firing → Cron expression verified

## 🎉 Success!

### Congratulations!
- [ ] Deployment complete
- [ ] System running smoothly
- [ ] Daily reports arriving
- [ ] Zero maintenance required

### Next Steps (Optional)
- [ ] Add more stocks to CSV
- [ ] Customize analysis metrics
- [ ] Set up additional alerts
- [ ] Share with team

---

**Deployment Date:** _____________

**Deployed By:** _____________

**Function App URL:** _____________

**Test Email Received:** ☐ Yes / ☐ No

**Production Email Received:** ☐ Yes / ☐ No

---

**Need Help?** Refer to DEPLOYMENT_GUIDE.md troubleshooting section.

