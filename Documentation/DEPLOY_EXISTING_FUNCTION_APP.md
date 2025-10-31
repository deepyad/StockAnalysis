# Deploy to Existing Function App: StockResearchFunctionApp

You already have an Azure Function App! Here's how to deploy your stock analysis code to it.

## Option 1: Deploy via VS Code Azure Extension ⚡ (RECOMMENDED)

### Prerequisites
- VS Code with Azure Functions extension installed
- Logged into Azure in VS Code

### Steps

1. **Right-click on StockResearchFunctionApp in Azure sidebar**
   - Click "Deploy to Function App"

2. **Or use Command Palette:**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type: "Azure Functions: Deploy to Function App"
   - Select: `StockResearchFunctionApp`

3. **Select deployment folder:**
   - Choose your current directory: `D:\MyDrive\Technology\StockAnalysisProj\StockResearch\StockAnalysis`

4. **Wait for deployment:**
   - VS Code will package and deploy your code
   - Watch the Output window for progress

5. **Done!** Your code is deployed.

---

## Option 2: Deploy via Azure Portal 🌐

### Steps

1. **Go to Azure Portal**
   - Navigate to: portal.azure.com
   - Find your Function App: `StockResearchFunctionApp`

2. **Open Deployment Center**
   - Click on `StockResearchFunctionApp`
   - Left sidebar → Click "Deployment Center"

3. **Setup Source**
   - Select: "Local Git" or "GitHub"
   - Follow prompts to configure

4. **Push your code:**
   ```bash
   # If using Local Git
   git add .
   git commit -m "Initial stock analysis deployment"
   git push azure main
   ```

---

## Option 3: Deploy via Azure CLI 💻

### Prerequisites
- Azure CLI installed
- Logged in: `az login`

### Steps

1. **Create deployment package:**
   ```bash
   # In your project directory
   cd D:\MyDrive\Technology\StockAnalysisProj\StockResearch\StockAnalysis
   
   # Package files (exclude unnecessary items)
   powershell Compress-Archive -Path function_app.py,requirements.txt,host.json,StockAnalyser_Final.py,holdings_with_changes_14_Aug.csv,local.settings.json -DestinationPath deploy.zip -Force
   ```

2. **Deploy to Function App:**
   ```bash
   az functionapp deployment source config-zip \
     --resource-group <your-resource-group-name> \
     --name StockResearchFunctionApp \
     --src deploy.zip
   ```

   **Find your resource group:**
   - Azure Portal → StockResearchFunctionApp → Overview
   - Look for "Resource group" field

3. **Clean up:**
   ```bash
   Remove-Item deploy.zip
   ```

---

## After Deployment: Configure Email ⚙️

Your function needs email settings to send reports!

### Steps

1. **Azure Portal** → `StockResearchFunctionApp` → **Configuration**

2. **Add Application Settings:**
   - Click "+ New application setting"
   - Add these 5 settings:

   ```
   Name: SMTP_SERVER
   Value: smtp.gmail.com

   Name: SMTP_PORT
   Value: 587

   Name: SENDER_EMAIL
   Value: your-email@gmail.com

   Name: SENDER_PASSWORD
   Value: your-app-password-here

   Name: RECIPIENT_EMAIL
   Value: your-email@gmail.com
   ```

3. **Save** all settings

4. **Restart** Function App (optional but recommended)

---

## Test Your Deployment 🧪

### Method 1: VS Code

1. **Right-click StockResearchFunctionApp**
2. **Click "Start Streaming Logs"**
3. **Right-click StockAnalysisTimer function**
4. **Click "Execute Function Now"** (if available)

### Method 2: Azure Portal

1. **Azure Portal** → `StockResearchFunctionApp` → **Functions**
2. **Click on** `StockAnalysisTimer`
3. **Click "Test/Run"**
4. **Click "Run"** button
5. **Watch logs** scroll

### Method 3: HTTP Call

```bash
curl -X POST https://stockresearchfunctionapp.azurewebsites.net/api/run
```

---

## Upload CSV File 📄

Your function needs the holdings CSV file.

### Option A: Commit to Git
```bash
git add holdings_with_changes_14_Aug.csv
git commit -m "Add holdings CSV"
git push azure main  # or push to GitHub
```

### Option B: Azure Files/Storage
- Upload CSV to Azure Storage
- Update path in `function_app.py` line 42

---

## Troubleshooting 🔧

### "Import errors"
- **Cause:** Dependencies not installed
- **Fix:** Check `requirements.txt` deployed correctly
- **Action:** Redeploy with all files

### "File not found"
- **Cause:** CSV path incorrect
- **Fix:** Verify `holdings_with_changes_14_Aug.csv` location
- **Action:** Check path in `function_app.py` line 42

### "Email not sending"
- **Cause:** SMTP settings missing/wrong
- **Fix:** Verify all 5 settings in Configuration
- **Action:** Check App Password (not regular password)

### "Function not appearing"
- **Cause:** Deployment incomplete
- **Fix:** Wait 3-5 minutes, refresh Azure Portal
- **Action:** Check Deployment Center for errors

### "Timer not working"
- **Cause:** Timer schedule issue
- **Fix:** Check `function_app.py` line 17
- **Action:** Verify cron expression

---

## Verify Deployment ✅

Check these to confirm success:

- [ ] Functions appear in Azure Portal
- [ ] `StockAnalysisTimer` function visible
- [ ] `StockAnalysisManual` function visible
- [ ] No errors in Deployment Center
- [ ] Application settings saved
- [ ] Test run successful
- [ ] Email received

---

## Next Steps 🚀

After successful deployment:

1. **Set timer schedule** (optional)
   - Edit `function_app.py` line 17
   - Redeploy

2. **Monitor execution**
   - Functions → Monitor tab
   - Check execution history

3. **Set up alerts** (optional)
   - Application Insights
   - Email notifications on failure

---

## Need Help?

- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed steps
- Review [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- Check Azure Portal logs

---

**Quick Command Reference:**

```bash
# Login to Azure
az login

# List your Function Apps
az functionapp list

# Get Function App details
az functionapp show --name StockResearchFunctionApp --resource-group <rg-name>

# Stream logs
az functionapp log tail --name StockResearchFunctionApp --resource-group <rg-name>
```

