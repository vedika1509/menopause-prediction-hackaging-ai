# Deployment Guide for MenoBalance AI

**Author:** Vedika  
**Project:** Hackaging AI - MenoBalance AI Platform  

This guide provides comprehensive instructions for deploying MenoBalance AI to various platforms.

## Prerequisites

- Python 3.9+
- Git
- Docker (optional, for containerized deployment)
- Nebius AI API key (for chatbot functionality)

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vedika1509/menopause-prediction-hackaging-ai.git
cd menopause-prediction-hackaging-ai/menobalance
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy the environment template and configure:

```bash
cp .env.example .env  # or create .env file manually
```

Edit `.env` file with your configuration:

```bash
# Required: Nebius AI API Key
NEBIUS_AI_API_KEY=your_actual_api_key_here

# Optional: Customize other settings
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_SERVER_PORT=8501
```

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)

Streamlit Cloud provides free hosting for Streamlit applications.

#### Steps:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository: `vedika1509/menopause-prediction-hackaging-ai`
   - Set main file path: `menobalance/src/app_streamlit_main.py`
   - Click "Deploy!"

3. **Configure Secrets**
   - In your Streamlit Cloud app settings
   - Go to "Secrets" tab
   - Add your environment variables:
     ```toml
     [secrets]
     NEBIUS_AI_API_KEY = "your_api_key_here"
     ```

4. **Redeploy**
   - Save secrets and redeploy your app

#### Streamlit Cloud Configuration

Create `.streamlit/secrets.toml` in your repository:

```toml
[secrets]
NEBIUS_AI_API_KEY = "your_api_key_here"
```

### Option 2: Docker Deployment

#### Build Docker Image

```bash
# Build the image
docker build -t menobalance-ai .

# Run the container
docker run -p 8501:8501 \
  -e NEBIUS_AI_API_KEY=your_api_key_here \
  menobalance-ai
```

#### Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  menobalance:
    build: .
    ports:
      - "8501:8501"
    environment:
      - NEBIUS_AI_API_KEY=${NEBIUS_AI_API_KEY}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

Run with Docker Compose:

```bash
docker-compose up -d
```

### Option 3: Local Development

#### Run Streamlit App

```bash
streamlit run src/app_streamlit_main.py
```

#### Run API Server (Optional)

In a separate terminal:

```bash
cd src
python api_endpoint.py
```

Access the application:
- Streamlit UI: http://localhost:8501
- API Documentation: http://localhost:8000/docs

### Option 4: Cloud Platforms

#### Heroku

1. Create `Procfile`:
   ```
   web: streamlit run src/app_streamlit_main.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

#### AWS EC2

1. Launch EC2 instance (Ubuntu 20.04+)
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx
   pip3 install -r requirements.txt
   ```
3. Configure Nginx reverse proxy
4. Run with systemd service

#### Google Cloud Platform

1. Use Cloud Run for containerized deployment
2. Or use App Engine with custom runtime

## Configuration

### Streamlit Configuration

The app uses `.streamlit/config.toml` for configuration:

```toml
[theme]
primaryColor = "#9B59B6"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F8F4FF"
textColor = "#262730"
font = "Inter"

[server]
headless = true
port = 8501
address = "0.0.0.0"
```

### API Configuration

The FastAPI backend can be configured via environment variables:

- `API_HOST`: Host address (default: 0.0.0.0)
- `API_PORT`: Port number (default: 8000)
- `LOG_LEVEL`: Logging level (default: INFO)

## Monitoring and Logging

### Log Files

Logs are stored in the `logs/` directory:

- `api.log`: API server logs
- `app.log`: Application logs

### Health Checks

The application provides health check endpoints:

- Streamlit: `/_stcore/health`
- API: `/health`

### Monitoring

For production deployments, consider:

- Application monitoring (e.g., New Relic, DataDog)
- Error tracking (e.g., Sentry)
- Performance monitoring
- Uptime monitoring

## Security Considerations

### Environment Variables

- Never commit API keys or secrets to version control
- Use environment variables for sensitive configuration
- Rotate API keys regularly

### CORS Configuration

Configure CORS appropriately for your deployment:

```python
# In api_endpoint.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### HTTPS

For production deployments:

- Use HTTPS certificates (Let's Encrypt for free certificates)
- Configure secure headers
- Use secure session management

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path configuration

2. **API Connection Issues**
   - Verify Nebius AI API key is correct
   - Check network connectivity
   - Review API endpoint configuration

3. **Model Loading Errors**
   - Ensure model files exist in `models/` directory
   - Check file permissions
   - Verify model file integrity

4. **Port Conflicts**
   - Change port numbers in configuration
   - Check for running processes on ports 8501/8000

### Debug Mode

Enable debug mode for development:

```bash
export STREAMLIT_LOGGER_LEVEL=debug
streamlit run src/app_streamlit_main.py
```

### Log Analysis

View logs for debugging:

```bash
# Streamlit logs
tail -f ~/.streamlit/logs/streamlit.log

# Application logs
tail -f logs/app.log
```

## Performance Optimization

### Caching

The application uses Streamlit caching for:

- Model loading (`@st.cache_resource`)
- Data processing (`@st.cache_data`)
- API responses

### Resource Management

- Monitor memory usage
- Optimize model loading
- Use lazy loading for heavy computations

### Scaling

For high-traffic deployments:

- Use load balancers
- Implement horizontal scaling
- Consider microservices architecture
- Use CDN for static assets

## Backup and Recovery

### Data Backup

- Backup model files
- Backup configuration files
- Backup logs (for debugging)

### Recovery Procedures

1. Restore from backup
2. Verify configuration
3. Test functionality
4. Monitor for issues

## Support and Maintenance

### Regular Maintenance

- Update dependencies regularly
- Monitor security advisories
- Review and rotate API keys
- Clean up log files

### Support Channels

- GitHub Issues: For bug reports and feature requests
- Documentation: This deployment guide
- Community: GitHub Discussions

## Conclusion

This deployment guide covers the main deployment options for MenoBalance AI. Choose the option that best fits your needs:

- **Streamlit Cloud**: Best for demos and small applications
- **Docker**: Best for consistent deployment across environments
- **Local**: Best for development and testing
- **Cloud Platforms**: Best for production applications

For additional support or questions, please refer to the project documentation or create an issue on GitHub.
