# MenoBalance AI Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying MenoBalance AI in various environments, from local development to production deployment.

## Prerequisites

### System Requirements
- **Python 3.9+** - Required for the application
- **Docker** - For containerized deployment
- **Git** - For version control
- **Memory** - Minimum 4GB RAM, 8GB recommended
- **Storage** - Minimum 10GB free space
- **Network** - Internet connection for API calls

### Required Accounts
- **Nebius.ai** - API key for chatbot functionality
- **GitHub** - For code repository access
- **Render/Streamlit Cloud** - For cloud deployment (optional)

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/vedika1509/menopause-prediction.git
cd menopause-prediction
```

### 2. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your values
NEBIUS_API_KEY=your_nebius_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
LOG_LEVEL=INFO
```

### 4. Run Application
```bash
# Start API server
python src/predict_api.py

# Start Streamlit app (in another terminal)
streamlit run src/app_streamlit_main.py
```

## Docker Deployment

### 1. Build Docker Image
```bash
# Build the image
docker build -t menobalance-ai .

# Tag for registry
docker tag menobalance-ai your-registry/menobalance-ai:latest
```

### 2. Run with Docker Compose
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Environment Configuration
```bash
# Set environment variables
export NEBIUS_API_KEY=your_api_key
export FLASK_SECRET_KEY=your_secret_key

# Or use .env file
echo "NEBIUS_API_KEY=your_api_key" > .env
echo "FLASK_SECRET_KEY=your_secret_key" >> .env
```

## Cloud Deployment

### Streamlit Cloud Deployment (Recommended)

#### 1. Prepare Repository
```bash
# Ensure requirements.txt is in root
# Ensure main app file is src/app_streamlit_main.py
# Add secrets to Streamlit Cloud
```

#### 2. Deploy to Streamlit Cloud
1. **Connect Repository** - Link GitHub repository
2. **Configure App**:
   - **Main file**: `src/app_streamlit_main.py`
   - **Python version**: 3.9
3. **Add Secrets**:
   - `NEBIUS_API_KEY` - Your Nebius.ai API key
   - `FLASK_SECRET_KEY` - Random secret key
4. **Deploy** - Click deploy button


### AWS Deployment

#### 1. EC2 Instance Setup
```bash
# Launch EC2 instance (t3.medium or larger)
# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. Deploy Application
```bash
# Clone repository
git clone https://github.com/vedika1509/menopause-prediction.git
cd menopause-prediction

# Set environment variables
export NEBIUS_API_KEY=your_api_key
export FLASK_SECRET_KEY=your_secret_key

# Start services
docker-compose up -d
```

#### 3. Configure Security Groups
- **Port 80** - HTTP traffic
- **Port 443** - HTTPS traffic
- **Port 8501** - Streamlit (if direct access needed)
- **Port 5000** - API (if direct access needed)

### Google Cloud Platform

#### 1. Cloud Run Deployment
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/menobalance-ai

# Deploy to Cloud Run
gcloud run deploy menobalance-ai \
  --image gcr.io/PROJECT-ID/menobalance-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### 2. Environment Variables
```bash
# Set environment variables in Cloud Run
gcloud run services update menobalance-ai \
  --set-env-vars NEBIUS_API_KEY=your_api_key,FLASK_SECRET_KEY=your_secret_key
```

## Production Configuration

### 1. Environment Variables
```bash
# Production environment variables
ENVIRONMENT=production
LOG_LEVEL=INFO
FLASK_ENV=production
NEBIUS_API_KEY=your_production_api_key
FLASK_SECRET_KEY=your_production_secret_key
```

### 2. Security Configuration
```bash
# Enable HTTPS
# Configure SSL certificates
# Set up firewall rules
# Enable access logging
# Configure rate limiting
```

### 3. Monitoring and Logging
```bash
# Set up monitoring
# Configure log aggregation
# Set up alerts
# Monitor performance metrics
# Track error rates
```

## Health Checks and Monitoring

### 1. Health Check Endpoints
```bash
# API health check
curl http://localhost:5000/health

# Streamlit health check
curl http://localhost:8501/_stcore/health
```

### 2. Monitoring Setup
```bash
# Set up monitoring dashboard
# Configure alerts for:
# - High error rates
# - Slow response times
# - Service downtime
# - Resource usage
```

### 3. Log Management
```bash
# Configure log rotation
# Set up log aggregation
# Monitor log levels
# Track user activity
```

## Troubleshooting

### Common Issues

#### 1. API Connection Issues
```bash
# Check if API is running
curl http://localhost:5000/health

# Check logs
docker-compose logs api

# Restart API service
docker-compose restart api
```

#### 2. Streamlit Issues
```bash
# Check if Streamlit is running
curl http://localhost:8501/_stcore/health

# Check logs
docker-compose logs streamlit

# Restart Streamlit service
docker-compose restart streamlit
```

#### 3. Model Loading Issues
```bash
# Check if models exist
ls -la models/

# Check model files
ls -la models/task_specific_*/

# Verify model loading
python -c "import pickle; pickle.load(open('models/task_specific_survival/best_model.pkl', 'rb'))"
```

#### 4. Database Issues
```bash
# Check Redis connection
redis-cli ping

# Check Redis logs
docker-compose logs redis

# Restart Redis
docker-compose restart redis
```

### Performance Optimization

#### 1. API Performance
```bash
# Increase worker processes
gunicorn -w 4 -b 0.0.0.0:5000 src.predict_api:app

# Enable caching
# Configure Redis caching
# Optimize model loading
```

#### 2. Streamlit Performance
```bash
# Optimize Streamlit configuration
# Enable caching
# Reduce memory usage
# Optimize data processing
```

## Backup and Recovery

### 1. Data Backup
```bash
# Backup models
tar -czf models_backup.tar.gz models/

# Backup logs
tar -czf logs_backup.tar.gz logs/

# Backup configuration
cp .env env_backup
```

### 2. Recovery Procedures
```bash
# Restore models
tar -xzf models_backup.tar.gz

# Restore logs
tar -xzf logs_backup.tar.gz

# Restore configuration
cp env_backup .env
```

## Scaling and Load Balancing

### 1. Horizontal Scaling
```bash
# Scale API service
docker-compose up -d --scale api=3

# Scale Streamlit service
docker-compose up -d --scale streamlit=2
```

### 2. Load Balancing
```bash
# Configure Nginx load balancer
# Set up health checks
# Configure sticky sessions
# Monitor load distribution
```

## Security Considerations

### 1. API Security
```bash
# Enable HTTPS
# Configure CORS
# Set up rate limiting
# Implement authentication
# Monitor for attacks
```

### 2. Data Security
```bash
# Encrypt sensitive data
# Secure API keys
# Monitor access logs
# Implement data retention
# Regular security audits
```

## Maintenance and Updates

### 1. Regular Maintenance
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Update Docker images
docker-compose pull
docker-compose up -d

# Clean up old logs
# Monitor disk usage
# Update security patches
```

### 2. Model Updates
```bash
# Backup current models
# Deploy new models
# Test new models
# Monitor performance
# Rollback if needed
```

## Support and Documentation

### 1. Getting Help
- **GitHub Issues** - Report bugs and issues
- **Documentation** - Check this guide and README
- **Community** - Join our community forum
- **Email Support** - Contact support@menobalance.ai

### 2. Contributing
- **Fork Repository** - Create your own fork
- **Create Branch** - Create feature branch
- **Submit PR** - Submit pull request
- **Code Review** - Participate in code review

---

*This deployment guide is regularly updated. Check for the latest version and updates.*

**Last Updated**: [Current Date]
**Version**: 1.0
**Next Review**: [3 months from current date]
