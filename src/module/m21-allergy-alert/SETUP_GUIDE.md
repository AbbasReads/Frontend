# MongoDB Atlas Setup Guide
## M21 Allergy Alert System - Cloud Deployment Only

This system is designed exclusively for **Streamlit Cloud + MongoDB Atlas** deployment. No local database setup required!

## 🚀 Quick Deployment (5 minutes)

### Step 1: Setup MongoDB Atlas (3 minutes)

1. **Create MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for a free account (no credit card required)
   - Create a new M0 Sandbox cluster (free forever)

2. **Configure Database Access**
   - Go to Database Access → Add New Database User
   - Create username/password (save these!)
   - Grant "Read and write to any database" permissions

3. **Configure Network Access**
   - Go to Network Access → Add IP Address
   - Add `0.0.0.0/0` (allows access from Streamlit Cloud)
   - Click "Confirm"

4. **Get Connection String**
   - Go to Clusters → Connect → Connect your application
   - Choose "Python" and version "3.6 or later"
   - Copy the connection string
   - Replace `<password>` with your actual password
   - Replace `<dbname>` with `m21_allergy_alert`

   **Example:**
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/m21_allergy_alert?retryWrites=true&w=majority
   ```

### Step 2: Deploy to Streamlit Cloud (2 minutes)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy M21 to Streamlit Cloud"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Repository: Select your repo
   - Branch: `main`
   - Main file path: `src/module/m21-allergy-alert/streamlit_app.py`
   - Click "Deploy!"

3. **Add MongoDB Connection**
   - In Streamlit Cloud app settings
   - Go to "Secrets" tab
   - Add:
   ```toml
   MONGODB_URL = "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/m21_allergy_alert?retryWrites=true&w=majority"
   ```
   - Save and the app will restart

### Step 3: Initialize Database (30 seconds)

1. **Access Your App**
   - Your app will be available at: `https://your-app-name.streamlit.app`
   - Wait for initial deployment (1-2 minutes)

2. **Setup Database**
   - In the sidebar, you'll see database connection status
   - If it shows "✅ Database Connected", you're ready!
   - The app will automatically create collections and seed test data on first run

## ✅ That's It!

Your M21 Allergy Alert System is now live with:
- **5 Patients** with varied allergy profiles
- **16 Medications** across 6 drug classes  
- **12 Allergies** with cross-reactivity rules
- **Complete test scenarios** for all alert types

## 🎯 What You Get

### Dashboard Features:
1. **💊 Prescription Validator** - Real-time allergy checking
2. **👤 Patient Allergies** - Complete profiles with risk assessment
3. **📋 Alert Log** - Audit trail with filtering capabilities
4. **📊 Statistics** - Interactive charts and metrics
5. **💊 Medications** - Drug database with alternatives

### Cloud Benefits:
- **Zero Infrastructure** - No servers to manage
- **Auto Scaling** - Handles any traffic load
- **Global CDN** - Fast access worldwide
- **99.9% Uptime** - Reliable cloud hosting
- **Free Hosting** - No hosting costs

## 🔧 Troubleshooting

### Database Connection Issues

**Problem:** "❌ Database Disconnected" in sidebar

**Solutions:**
1. **Check Connection String**
   - Verify it starts with `mongodb+srv://`
   - Ensure password is correct (no special characters issues)
   - Database name should be `m21_allergy_alert`

2. **Check Network Access**
   - In MongoDB Atlas → Network Access
   - Ensure `0.0.0.0/0` is added
   - Wait 2-3 minutes for changes to take effect

3. **Check Database User**
   - In MongoDB Atlas → Database Access
   - User should have "Read and write to any database" permissions
   - Try creating a new user if issues persist

### Streamlit Cloud Issues

**Problem:** App won't deploy or crashes

**Solutions:**
1. **Check File Path**
   - Main file should be: `src/module/m21-allergy-alert/streamlit_app.py`
   - Case sensitive!

2. **Check Secrets**
   - Secrets key must be exactly: `MONGODB_URL`
   - No extra spaces or characters

3. **Check Logs**
   - In Streamlit Cloud → Manage app → View logs
   - Look for specific error messages

### Data Issues

**Problem:** No data showing in app

**Solutions:**
1. **Restart App**
   - In Streamlit Cloud → Reboot app
   - This will re-run database initialization

2. **Check MongoDB Atlas**
   - Go to Collections tab in Atlas
   - Should see 9 collections with data
   - If empty, restart the Streamlit app

## 🎉 Success Indicators

Your deployment is successful when you see:

✅ **Sidebar shows:** "✅ Database Connected"  
✅ **Prescription Validator:** Shows patient and medication dropdowns  
✅ **Patient Allergies:** Shows 5 patients to select from  
✅ **Statistics:** Shows charts with alert data  
✅ **Alert Log:** Shows historical allergy checks  

## 🔒 Security Notes

- **Connection String:** Keep your MongoDB connection string secure
- **Network Access:** `0.0.0.0/0` allows global access (fine for demo/educational use)
- **Production:** For production, restrict to specific IP ranges
- **Credentials:** Never commit connection strings to GitHub

## 📊 MongoDB Atlas Free Tier

Your free M0 cluster includes:
- **512 MB Storage** (plenty for this project)
- **100 Connections** (more than enough)
- **No Time Limit** (free forever)
- **Shared RAM/CPU** (sufficient for educational use)

## 🚀 Going Live

Your M21 system is now:
- **Publicly accessible** via your Streamlit Cloud URL
- **Professionally hosted** with 99.9% uptime
- **Automatically backed up** by MongoDB Atlas
- **Scalable** to handle increased usage
- **Maintainable** through cloud dashboards

Perfect for demonstrations, portfolio projects, or educational use! 🎯