"""
Backend Deployment Script for MenoBalance AI
Deploy FastAPI backend separately from Streamlit frontend
"""

import os
import subprocess
import sys
from pathlib import Path

def deploy_to_render():
    """Deploy backend to Render.com"""
    print("🚀 Deploying MenoBalance AI Backend to Render.com")
    
    # Check if we're in the right directory
    if not os.path.exists("src/api_endpoint.py"):
        print("❌ Error: api_endpoint.py not found. Run from project root.")
        return False
    
    print("✅ Backend files found")
    print("📋 Next steps for Render deployment:")
    print("1. Create new Web Service on Render.com")
    print("2. Connect your GitHub repository")
    print("3. Set build command: pip install -r requirements.txt")
    print("4. Set start command: uvicorn src.api_endpoint:app --host 0.0.0.0 --port $PORT")
    print("5. Set environment: PYTHON_VERSION=3.9")
    
    return True

def deploy_to_railway():
    """Deploy backend to Railway"""
    print("🚀 Deploying MenoBalance AI Backend to Railway")
    
    print("📋 Railway deployment steps:")
    print("1. Install Railway CLI: npm install -g @railway/cli")
    print("2. Login: railway login")
    print("3. Initialize: railway init")
    print("4. Deploy: railway up")
    
    return True

def deploy_to_heroku():
    """Deploy backend to Heroku"""
    print("🚀 Deploying MenoBalance AI Backend to Heroku")
    
    # Create Procfile for Heroku
    procfile_content = "web: uvicorn src.api_endpoint:app --host 0.0.0.0 --port $PORT"
    
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    
    print("✅ Created Procfile for Heroku")
    print("📋 Heroku deployment steps:")
    print("1. Install Heroku CLI")
    print("2. Login: heroku login")
    print("3. Create app: heroku create menobalance-api")
    print("4. Deploy: git push heroku main")
    
    return True

def create_docker_compose():
    """Create docker-compose for local development"""
    docker_compose_content = """version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    command: uvicorn src.api_endpoint:app --host 0.0.0.0 --port 8000
    environment:
      - PYTHONPATH=/app
    volumes:
      - ./models:/app/models
      - ./data:/app/data

  frontend:
    build: .
    ports:
      - "8501:8501"
    command: streamlit run src/app_streamlit_main.py --server.port=8501 --server.address=0.0.0.0
    environment:
      - API_URL=http://backend:8000
    depends_on:
      - backend
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content)
    
    print("✅ Created docker-compose.yml for local development")
    print("📋 To run locally:")
    print("docker-compose up --build")

def main():
    """Main deployment function"""
    print("🌸 MenoBalance AI Backend Deployment")
    print("=" * 50)
    
    print("\nChoose deployment option:")
    print("1. Render.com (Recommended)")
    print("2. Railway")
    print("3. Heroku")
    print("4. Local Docker Compose")
    print("5. Show all options")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        deploy_to_render()
    elif choice == "2":
        deploy_to_railway()
    elif choice == "3":
        deploy_to_heroku()
    elif choice == "4":
        create_docker_compose()
    elif choice == "5":
        print("\n📋 All deployment options:")
        deploy_to_render()
        print("\n" + "="*50)
        deploy_to_railway()
        print("\n" + "="*50)
        deploy_to_heroku()
        print("\n" + "="*50)
        create_docker_compose()
    else:
        print("❌ Invalid choice. Please run again.")

if __name__ == "__main__":
    main()
