# Azure Functions Deployment Guide for Stock Analysis

## Overview
This guide explains how to deploy your stock analysis code to Azure Functions as a timer-triggered function that runs daily and emails the results.

## Prerequisites
1. Azure account with active subscription
2. GitHub/Git repository for your code
3. Python 3.9+ installed locally (for testing)

## Step 1: Create Azure Resources

### Create Function App in Azure Portal
1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → Search "Function App"
3. Fill in details:
   - **Resource Group**: Create new or select existing
   - **Function App name**: `stockanalysis-[yourname]` (must be globally unique)
   - **Publish**: Code
   - **Runtime stack**: Python
   - **Version**: 3.9 or 3.10
   - **Region**: Choose closest to you (India Central recommended for Indian stocks)
   - **Operating System**: Linux (cheaper) or Windows
   - **Plan Type**: Consumption (Serverless) - FREE for 1M executions/month
4. Click "Review + create" → "Create"

## Step 2: Configure Function App Settings

### Add Environment Variables
1. In Azure Portal, go to your Function App
2. Navigate to **Configuration** → **Application settings**
3. Click **"+ New application setting"** and add:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=your-email@gmail.com
```

**For Gmail App Password:**
- Go to Google Account → Security
- Enable 2-Step Verification
- Go to "App passwords" → Generate password
- Use this 16-character password (not your regular Gmail password)

### Configure Storage Account
Azure Functions automatically creates a Storage Account. This is used for:
- Function code storage
- Function logs
- Temp file storage

## Step 3: Deploy Your Code

### Option A: Deploy via Azure Portal
1. In Function App, go to **Deployment Center**
2. Choose source: GitHub, Azure DevOps, or Local Git
3. Connect your repository
4. Configure branch and path
5. Azure will automatically deploy on every push

### Option B: Deploy via Azure CLI
```bash
# Login to Azure
az login

# Create deployment package
zip -r stockanalysis.zip . -x "*.git*" -x "*.vscode*"

# Deploy to Function App
az functionapp deployment source config-zip \
  --resource-group <your-resource-group> \
  --name <your-function-app-name> \
  --src stockanalysis.zip
```

### Option C: Deploy via Visual Studio Code
1. Install "Azure Functions" extension in VS Code
2. Open your project folder
3. Press F1 → "Azure Functions: Deploy to Function App"
4. Follow the prompts

## Step 4: Upload Input File

Your function needs the holdings CSV file. Options:

### Option 1: Azure Files (Recommended)
1. Go to your Function App → Configuration
2. Add setting: `FILE_PATH=/home/site/wwwroot/data/holdings_with_changes_14_Aug.csv`
3. Use Azure Storage Explorer to upload file to Function App

### Option 2: GitHub Repository
1. Commit the CSV file to your repo
2. Reference it in your code

### Option 3: Azure Blob Storage
1. Create a blob storage container
2. Upload CSV file
3. Modify code to download from blob storage

## Step 5: Configure Timer Schedule

The default schedule is **9:00 AM UTC** (not IST).

To change to India time (IST):
- 9:00 AM IST = 3:30 AM UTC (9:00 - 5:30)
- 6:00 PM IST = 12:30 PM UTC (18:00 - 5:30)

**Update in `host.json`:**
```json
{
  "schedule": "30 12 * * *"  // 12:30 UTC = 6:00 PM IST
}
```

**Cron format:** `minute hour day month dayOfWeek`

## Step 6: Test Your Function

### Test Timer Trigger Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run Azure Functions Core Tools
func start

# The timer will run on schedule or you can trigger manually
```

### Test on Azure
1. In Azure Portal, go to your Function App
2. Navigate to **Functions** → Click your function
3. Click **"Test/Run"** → "Run"
4. Check logs for execution

### Test Manual HTTP Trigger
```bash
# Get your function URL
curl -X POST https://your-function-app.azurewebsites.net/api/run
```

## Step 7: Monitor and Logs

### View Logs in Azure Portal
1. Go to Function App → **Functions**
2. Click your function → **Monitor**
3. View execution history and logs

### Enable Application Insights
1. In Function App, go to **Settings** → **Application Insights**
2. Enable Application Insights
3. View detailed telemetry and performance

### Log Storage
Logs are saved to Azure Blob Storage in:
`/AzureWebJobsStorage/{FUNCTION_APP_NAME}/logfiles/`

## Troubleshooting

### Function Not Running
- Check **Monitor** tab for errors
- Verify timer schedule is correct
- Check environment variables are set

### Email Not Sending
- Verify SMTP credentials in Application Settings
- Check Sender Email has App Password (not regular password)
- Enable SMTP debugging in logs

### Import Errors
- Ensure all packages in `requirements.txt` are deployed
- Check Python version matches (3.9 or 3.10)
- Review Function App logs for missing modules

### File Not Found
- Verify CSV file path is correct
- Check file permissions
- Use absolute paths in code

### Timeout Errors
- Increase timeout in `host.json` (default 10 minutes)
- For >10 minutes, consider upgrading to Premium/App Service plan

## Cost Estimation

### Consumption Plan (FREE TIER)
- **1 million executions/month**: FREE
- **Duration**: First 400,000 GB-seconds: FREE
- **Additional**: ~$0.16 per million GB-seconds

**Your use case:** ~30 runs/month, 5 minutes each = **FREE**

### Data Storage
- CSV file: Negligible cost
- Excel output: Negligible cost
- Logs: First 5 GB FREE per month

**Estimated monthly cost: $0-1 USD**

## Security Best Practices

1. **Never commit credentials** to GitHub
2. Use **Azure Key Vault** for sensitive data
3. Use **Managed Identity** for Azure resource access
4. Enable **HTTPS only** for Function App
5. Use **App Passwords** for email (not real passwords)
6. Enable **Authentication** for manual HTTP trigger

## Advanced Configuration

### Multiple Output Locations
Modify `StockAnalyser_Final.py` to save to:
- Azure Blob Storage
- Azure Files
- OneDrive/Dropbox via API

### Error Notifications
Already configured to send error emails on failure.

### Parallel Processing
For faster execution, split stock list and process in parallel.

### Caching
Cache yfinance data to reduce API calls and improve speed.

## Support and Resources

- [Azure Functions Python Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Timer Trigger Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer)
- [Azure Functions Cost Calculator](https://azure.microsoft.com/pricing/details/functions/)

## Next Steps

1. Test function locally
2. Deploy to Azure
3. Configure email settings
4. Upload CSV file
5. Test first run
6. Set timer schedule
7. Monitor for a week
8. Optimize as needed

---

**Questions?** Check Azure Function logs or raise an issue in your repository.

