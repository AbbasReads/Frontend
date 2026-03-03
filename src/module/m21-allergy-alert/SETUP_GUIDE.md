# Module 21: Setup Guide (Python/MongoDB)
## Allergy-Aware Medication Alert System

This guide will help you set up and run the complete M21 system using Python, Streamlit, and MongoDB.

## Prerequisites

### Required Software
- **Python** (3.8 or higher) - [Download here](https://python.org/downloads/)
- **MongoDB** (4.4 or higher) - [Download here](https://www.mongodb.com/try/download/community)
- **Git** - [Download here](https://git-scm.com/)

### Verify Installation
```bash
python --version    # Should show 3.8+
pip --version       # Should show pip version
mongod --version    # Should show MongoDB version
```

## Quick Start (Automated)

### Option 1: Use the Setup Script
```bash
cd src/module/m21-allergy-alert-python
python setup.py
```

### Option 2: Use the Start Script
```bash
cd src/module/m21-allergy-alert-python
./start.sh
```

This will:
1. Check all prerequisites
2. Install Python dependencies
3. Set up MongoDB database
4. Start both backend and frontend servers
5. Open the application in your browser

## Manual Setup (Step by Step)

### Step 1: MongoDB Setup

1. **Install MongoDB:**
   ```bash
   # macOS with Homebrew
   brew tap mongodb/brew
   brew install mongodb-community
   
   # Ubuntu/Debian
   sudo apt-get install mongodb
   
   # Windows
   # Download and install from MongoDB website
   ```

2. **Start MongoDB service:**
   ```bash
   # macOS
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   
   # Windows
   # Start MongoDB service from Services panel
   ```

3. **Verify MongoDB is running:**
   ```bash
   mongo --eval "db.adminCommand('ping')"
   ```

### Step 2: Python Environment Setup

1. **Create virtual environment (recommended):**
   ```bash
   cd src/module/m21-allergy-alert-python
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Database Setup

1. **Run database setup script:**
   ```bash
   cd database
   python setup_db.py
   ```

   This will:
   - Create the `m21_allergy_alert` database
   - Create all collections with proper indexes
   - Insert comprehensive test data

### Step 4: Start Backend API

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Start FastAPI server:**
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```

   You should see:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ```

3. **Test API health:**
   ```bash
   curl http://localhost:8000/health
   ```

### Step 5: Start Frontend Dashboard

1. **Open new terminal and navigate to frontend:**
   ```bash
   cd src/module/m21-allergy-alert-python/frontend
   ```

2. **Start Streamlit server:**
   ```bash
   streamlit run app.py
   ```

   You should see:
   ```
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

### Step 6: Access the Application

- **Streamlit Dashboard:** http://localhost:8501
- **FastAPI Backend:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **MongoDB:** mongodb://localhost:27017/m21_allergy_alert

## Testing the System

### 1. Test API Health
```bash
curl http://localhost:8000/health
```

### 2. Test Database Connection
```bash
curl http://localhost:8000/api/v1/patients
```

### 3. Test Prescription Validation
```bash
curl -X POST http://localhost:8000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient_1",
    "med_id": "med_1",
    "dose": "500mg",
    "frequency": "Three times daily",
    "start_date": "2026-03-20"
  }'
```

### 4. Test MongoDB Directly
```bash
mongo m21_allergy_alert --eval "db.patients.find().pretty()"
```

## Troubleshooting

### Common Issues

#### 1. MongoDB Connection Failed
**Error:** `pymongo.errors.ServerSelectionTimeoutError`

**Solutions:**
- Ensure MongoDB is running: `brew services start mongodb-community` (macOS)
- Check MongoDB status: `brew services list | grep mongodb` (macOS)
- Verify port 27017 is available: `lsof -i :27017`
- Check MongoDB logs: `tail -f /usr/local/var/log/mongodb/mongo.log` (macOS)

#### 2. Port Already in Use
**Error:** `OSError: [Errno 48] Address already in use`

**Solutions:**
- Kill existing processes:
  ```bash
  lsof -ti:8000 | xargs kill -9  # Backend
  lsof -ti:8501 | xargs kill -9  # Frontend
  ```
- Use different ports:
  ```bash
  uvicorn main:app --port 8001    # Backend
  streamlit run app.py --server.port 8502  # Frontend
  ```

#### 3. Module Not Found
**Error:** `ModuleNotFoundError: No module named 'streamlit'`

**Solutions:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python path: `which python`

#### 4. Database Setup Failed
**Error:** Database connection or insertion errors

**Solutions:**
- Verify MongoDB is running and accessible
- Check database permissions
- Reset database:
  ```bash
  mongo m21_allergy_alert --eval "db.dropDatabase()"
  python database/setup_db.py
  ```

### MongoDB Troubleshooting

#### Reset Database
```bash
mongo m21_allergy_alert --eval "db.dropDatabase()"
cd database && python setup_db.py
```

#### Check Collections
```bash
mongo m21_allergy_alert --eval "show collections"
```

#### View Sample Data
```bash
mongo m21_allergy_alert --eval "db.patients.findOne()"
```

### Clean Installation

To start completely fresh:
```bash
# Remove virtual environment
rm -rf venv

# Drop MongoDB database
mongo m21_allergy_alert --eval "db.dropDatabase()"

# Recreate virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall everything
pip install -r requirements.txt
python database/setup_db.py
```

## Development Mode

### Backend Development
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
# Auto-reloads on code changes
```

### Frontend Development
```bash
cd frontend
streamlit run app.py --server.runOnSave true
# Auto-reloads on file changes
```

### Database Development
- **MongoDB Compass:** Visual database management tool
- **Studio 3T:** Advanced MongoDB IDE
- **Command Line:** `mongo m21_allergy_alert`

## Production Deployment

### Environment Variables
Create `.env` file:
```
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=m21_allergy_alert
API_BASE_URL=http://localhost:8000
ENVIRONMENT=production
```

### Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000 8501

CMD ["python", "start_production.py"]
```

### Process Management
Use PM2 or systemd for production:
```bash
# Install PM2
npm install -g pm2

# Start services
pm2 start backend/main.py --name "m21-backend" --interpreter python
pm2 start "streamlit run frontend/app.py" --name "m21-frontend"

# Save configuration
pm2 startup
pm2 save
```

## System Requirements

### Minimum Requirements
- **RAM:** 4GB
- **Storage:** 2GB free space
- **CPU:** Dual-core processor
- **OS:** Windows 10, macOS 10.14, Ubuntu 18.04+
- **Python:** 3.8+
- **MongoDB:** 4.4+

### Recommended Requirements
- **RAM:** 8GB or more
- **Storage:** 5GB free space
- **CPU:** Quad-core processor
- **SSD:** For better MongoDB performance

## Performance Optimization

### MongoDB Optimization
```javascript
// Create compound indexes for better performance
db.patient_allergies.createIndex({ patient_id: 1, allergy_id: 1 })
db.cross_reactivity_rules.createIndex({ allergen_id: 1, risk_score: -1 })
db.alert_log.createIndex({ patient_id: 1, logged_at: -1 })

// Enable profiling for slow queries
db.setProfilingLevel(2, { slowms: 100 })
```

### Python Optimization
- Use virtual environments for dependency isolation
- Enable FastAPI's automatic documentation
- Implement connection pooling for MongoDB
- Use async/await for better concurrency

## Useful Commands

### MongoDB Commands
```bash
# Connect to database
mongo m21_allergy_alert

# Show collections
show collections

# Count documents
db.patients.count()

# Find with pretty formatting
db.medications.find().pretty()

# Aggregation example
db.alert_log.aggregate([
  { $group: { _id: "$alert_type", count: { $sum: 1 } } }
])
```

### Python Commands
```bash
# Check installed packages
pip list

# Update all packages
pip install --upgrade -r requirements.txt

# Run specific tests
python -m pytest tests/

# Check code style
black --check .
flake8 .
```

### System Commands
```bash
# Check running processes
ps aux | grep python
ps aux | grep mongod

# Check port usage
lsof -i :8000  # FastAPI
lsof -i :8501  # Streamlit
lsof -i :27017 # MongoDB

# Monitor system resources
htop
```

## Next Steps

Once the system is running:

1. **Explore the Dashboard:** Navigate through all 5 sections
2. **Test Prescriptions:** Try different patient/medication combinations
3. **Review MongoDB Data:** Use MongoDB Compass or command line
4. **Examine API Documentation:** Visit http://localhost:8000/docs
5. **Test API Endpoints:** Use the interactive Swagger UI
6. **Review Code Structure:** Understand the Python/MongoDB implementation

## Support Resources

### Documentation
- **FastAPI:** https://fastapi.tiangolo.com/
- **Streamlit:** https://docs.streamlit.io/
- **MongoDB:** https://docs.mongodb.com/
- **PyMongo:** https://pymongo.readthedocs.io/

### Community
- **FastAPI GitHub:** https://github.com/tiangolo/fastapi
- **Streamlit Community:** https://discuss.streamlit.io/
- **MongoDB Community:** https://community.mongodb.com/

---

**Need Help?** Check the troubleshooting section above or review the error messages carefully. Most issues are related to MongoDB connectivity or Python environment setup.