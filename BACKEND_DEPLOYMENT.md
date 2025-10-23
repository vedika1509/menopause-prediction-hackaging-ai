# 🚀 Backend API Deployment Guide

## Current Architecture

### ✅ **What's Working:**
- **Streamlit Frontend**: Fully functional on Streamlit Cloud
- **Integrated Predictions**: Models loaded directly in Streamlit
- **All Features**: Working without external API

### ❌ **What's Missing:**
- **Separate Backend API**: No standalone FastAPI server
- **External Endpoints**: No REST API for external access
- **Scalability**: Limited by Streamlit Cloud resources

## 🎯 **Deployment Options**

### **Option 1: Render.com (Recommended)**

#### **Step 1: Prepare Backend**
```bash
# Create backend directory
mkdir menobalance-backend
cd menobalance-backend

# Copy API files
cp ../src/api_endpoint.py .
cp ../src/prediction_service.py .
cp ../src/prediction_service_fallback.py .
cp ../requirements.txt .

# Copy models and data
cp -r ../models .
cp -r ../data .
```

#### **Step 2: Create Render Configuration**
Create `render.yaml`:
```yaml
services:
  - type: web
    name: menobalance-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api_endpoint:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.9
```

#### **Step 3: Deploy to Render**
1. Connect GitHub repository
2. Select "Web Service"
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn api_endpoint:app --host 0.0.0.0 --port $PORT`
5. Deploy!

### **Option 2: Railway**

#### **Step 1: Install Railway CLI**
```bash
npm install -g @railway/cli
```

#### **Step 2: Deploy**
```bash
railway login
railway init
railway up
```

### **Option 3: Heroku**

#### **Step 1: Create Procfile**
```
web: uvicorn src.api_endpoint:app --host 0.0.0.0 --port $PORT
```

#### **Step 2: Deploy**
```bash
heroku create menobalance-api
git push heroku main
```

### **Option 4: Local Docker**

#### **Step 1: Create Dockerfile for Backend**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY models/ ./models/
COPY data/ ./data/

EXPOSE 8000

CMD ["uvicorn", "src.api_endpoint:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **Step 2: Run with Docker Compose**
```bash
docker-compose up --build
```

## 🔧 **Update Streamlit to Use External API**

### **Step 1: Add API URL to Streamlit Secrets**
Create `.streamlit/secrets.toml`:
```toml
API_URL = "https://your-backend-url.com"
```

### **Step 2: Update Prediction Function**
The app will automatically try external API first, then fallback to integrated service.

## 📊 **API Endpoints**

Once deployed, your backend will have:

- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Get predictions
- `GET /docs` - Swagger documentation

## 🧪 **Testing the API**

### **Local Testing**
```bash
# Start backend locally
uvicorn src.api_endpoint:app --reload

# Test health endpoint
curl http://localhost:8000/health

# Test prediction endpoint
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 45, "bmi": 25.5, "fsh": 15.2}'
```

### **Production Testing**
```bash
# Test deployed API
curl https://your-backend-url.com/health
curl -X POST https://your-backend-url.com/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 45, "bmi": 25.5, "fsh": 15.2}'
```

## 🎯 **Recommended Deployment Strategy**

### **For Production:**
1. **Backend**: Deploy to Render.com (free tier available)
2. **Frontend**: Keep on Streamlit Cloud
3. **Database**: Add PostgreSQL for user data (optional)

### **For Development:**
1. **Local**: Use Docker Compose
2. **Testing**: Use integrated prediction service
3. **Staging**: Deploy to Railway

## 📈 **Benefits of Separate Backend**

### **Advantages:**
- ✅ **Scalability**: Handle more concurrent users
- ✅ **Performance**: Dedicated resources for ML models
- ✅ **Flexibility**: Use API from multiple frontends
- ✅ **Monitoring**: Better logging and analytics
- ✅ **Security**: Separate authentication and authorization

### **Current Setup (Integrated):**
- ✅ **Simplicity**: Everything in one place
- ✅ **Cost**: Free on Streamlit Cloud
- ✅ **Maintenance**: Single deployment
- ❌ **Scalability**: Limited by Streamlit resources
- ❌ **Performance**: Models load on every request

## 🚀 **Quick Start Commands**

```bash
# Deploy backend to Render
python deploy_backend.py

# Test API locally
uvicorn src.api_endpoint:app --reload

# Update Streamlit to use external API
# Add API_URL to Streamlit secrets
```

## 📞 **Support**

If you need help with deployment:
1. Check the logs in your deployment platform
2. Test the API endpoints manually
3. Verify model files are accessible
4. Check environment variables

---

**Next Steps:**
1. Choose your deployment platform
2. Deploy the backend API
3. Update Streamlit secrets with API URL
4. Test the integration
5. Monitor performance and logs
