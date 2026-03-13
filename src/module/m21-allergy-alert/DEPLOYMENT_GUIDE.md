# Deployment Guide: Streamlit Cloud + MongoDB Atlas

**Cloud-Only Deployment** - No local development support

This guide will help you deploy the M21 Allergy Alert System exclusively to Streamlit Cloud using MongoDB Atlas.

## 🚀 Quick Deployment Steps

### 1. Setup MongoDB Atlas

1. **Create MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for a free account
   - Create a new cluster (M0 Sandbox is free)

2. **Configure Database Access**
   - Go to Database Access → Add New Database User
   - Create a user with read/write permissions
   - Note down the username and password

3. **Configure Network Access**
   - Go to Network Access → Add IP Address
   - Add `0.0.0.0/0` to allow access from anywhere (for Streamlit Cloud)
   - Or add specific Streamlit Cloud IP ranges if preferred

4. **Get Connection String**
   - Go to Clusters → Connect → Connect your application
   - Choose Python driver version 3.6+
   - Copy the connection string
   - Replace `<password>` with your actual password
   - Replace `<dbname>` with `m21_allergy_alert`

   Example:
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/m21_allergy_alert?retryWrites=true&w=majority
   ```

### 2. Deploy to Streamlit Cloud

1. **Push Code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `src/module/m21-allergy-alert/streamlit_app.py`
   - Click "Deploy"

3. **Configure Secrets**
   - In your Streamlit Cloud app dashboard
   - Go to Settings → Secrets
   - Add your MongoDB connection string:
   ```toml
   MONGODB_URL = "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/m21_allergy_alert?retryWrites=true&w=majority"
   ```

### 3. Database Auto-Initialization

The database will automatically initialize when you first access the app:
- Collections are created automatically
- Test data is seeded on first run
- No manual setup required!

### 4. Test Your Deployment

1. **Verify Connection**
   - Check that the sidebar shows "✅ Database Connected"
   - Navigate through all 5 pages of the dashboard

2. **Test Core Functionality**
   - Try the Prescription Validator with test data
   - View patient allergy profiles
   - Check alert logs and statistics

## 📁 File Structure for Deployment

```
your-repo/
├── src/module/m21-allergy-alert/
│   ├── streamlit_app.py          # Main entry point for Streamlit Cloud
│   ├── requirements.txt          # Dependencies
│   ├── packages.txt             # System packages (if needed)
│   ├── .streamlit/
│   │   └── secrets.toml.example # Template for secrets
│   ├── frontend/
│   │   └── app.py              # Main Streamlit application
│   ├── shared/
│   │   ├── models.py           # Data models
│   │   └── database.py         # Database connection
│   └── database/
│       └── setup_db.py         # Database seeding (auto-run)
```

## 🔧 Configuration Details

### Streamlit Secrets Format
```toml
# For Streamlit Cloud only - add this in Settings → Secrets
MONGODB_URL = "mongodb+srv://username:password@cluster.mongodb.net/m21_allergy_alert?retryWrites=true&w=majority"
```

### Environment Variables
The app is designed exclusively for Streamlit Cloud:
- **Streamlit Cloud**: Uses `st.secrets["MONGODB_URL"]` (required)
- **No Local Support**: This system only works on Streamlit Cloud

## 🛠️ Troubleshooting

### Common Issues

#### 1. Database Connection Failed
**Error**: `ServerSelectionTimeoutError`

**Solutions**:
- Verify MongoDB Atlas connection string is correct
- Check that network access allows connections from `0.0.0.0/0`
- Ensure database user has proper permissions
- Verify the database name in connection string

#### 2. Secrets Not Found
**Error**: `KeyError: 'MONGODB_URL'`

**Solutions**:
- Add the connection string to Streamlit Cloud secrets
- Ensure the secret key is exactly `MONGODB_URL`
- Redeploy the app after adding secrets

#### 3. Import Errors
**Error**: `ModuleNotFoundError`

**Solutions**:
- Ensure all dependencies are in `requirements.txt`
- Check that file paths are correct in `streamlit_app.py`
- Verify the main file path in Streamlit Cloud settings

#### 4. Database Empty
**Error**: No data showing in the app

**Solutions**:
- Database initializes automatically on first run
- Check MongoDB Atlas data browser to verify collections exist
- Restart the Streamlit app to trigger re-initialization
- Ensure the database name matches in connection string

### Performance Optimization

#### 1. Connection Pooling
The app uses MongoDB connection pooling automatically. For better performance:
- Keep connections alive between requests
- Use connection caching in Streamlit

#### 2. Query Optimization
- Indexes are automatically created during setup
- Use aggregation pipelines for complex queries
- Limit result sets for large collections

#### 3. Streamlit Caching
```python
@st.cache_data
def get_cached_data():
    # Cache expensive database operations
    pass
```

## 🔒 Security Best Practices

### 1. Database Security
- Use strong passwords for database users
- Limit network access to necessary IP ranges
- Enable MongoDB Atlas security features
- Regularly rotate database credentials

### 2. Application Security
- Never commit secrets to version control
- Use Streamlit Cloud secrets for sensitive data
- Validate all user inputs
- Implement proper error handling

### 3. Access Control
- Consider implementing user authentication
- Add role-based access if needed
- Monitor database access logs
- Set up alerts for unusual activity

## 📊 Monitoring & Maintenance

### 1. MongoDB Atlas Monitoring
- Use Atlas monitoring dashboard
- Set up alerts for performance issues
- Monitor connection counts and query performance
- Review slow query logs

### 2. Streamlit Cloud Monitoring
- Check app logs in Streamlit Cloud dashboard
- Monitor app performance and uptime
- Set up health checks if needed
- Review usage analytics

### 3. Regular Maintenance
- Update dependencies regularly
- Monitor database storage usage
- Backup important data
- Test disaster recovery procedures

## 🚀 Going to Production

### 1. Upgrade Database
- Consider upgrading from M0 (free) to paid tier for production
- Enable backups and point-in-time recovery
- Set up multiple regions if needed
- Configure proper monitoring and alerting

### 2. Custom Domain
- Set up custom domain in Streamlit Cloud
- Configure SSL certificates
- Set up proper DNS records
- Test domain configuration

### 3. Advanced Features
- Implement user authentication
- Add audit logging
- Set up data export capabilities
- Configure automated backups

---

## 📞 Support

If you encounter issues:

1. **Check Streamlit Cloud logs** in your app dashboard
2. **Verify MongoDB Atlas** connection and permissions
3. **Review this guide** for common solutions
4. **Test locally first** before deploying to cloud

Your M21 Allergy Alert System should now be running smoothly on Streamlit Cloud with MongoDB Atlas! 🎉