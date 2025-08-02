# 🚀 Render Deployment Guide - HackRx 6.0

## Prerequisites

Before starting, ensure you have:
- ✅ GitHub account
- ✅ Render account (free at render.com)
- ✅ All API keys ready (Groq, OpenAI, Pinecone)

## Step 1: Prepare Your Repository

### 1.1 Create a new GitHub repository
```bash
# Create a new repository on GitHub
# Name it: hackrx-6.0-system
# Make it public
```

### 1.2 Push your code to GitHub
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - HackRx 6.0 system"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/hackrx-6.0-system.git

# Push to GitHub
git push -u origin main
```

## Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Verify your email

## Step 3: Create New Web Service

### 3.1 Start New Service
1. Click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub account if not already connected

### 3.2 Configure Repository
1. **Repository**: Select your `hackrx-6.0-system` repository
2. **Branch**: `main`
3. **Root Directory**: Leave empty (default)

### 3.3 Service Configuration
```
Name: hackrx-6-0-system
Environment: Python 3
Region: Choose closest to you (e.g., Frankfurt)
Branch: main
Root Directory: (leave empty)
```

### 3.4 Build & Deploy Settings
```
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

## Step 4: Environment Variables

Add these environment variables in Render dashboard:

### 4.1 Required Variables
```
GROQ_API_KEY = your_groq_api_key_here
OPENAI_API_KEY = your_openai_api_key_here
PINECONE_API_KEY = your_pinecone_api_key_here
PINECONE_ENVIRONMENT = us-east-1-aws
PINECONE_INDEX_NAME = bajaj-documents
```

### 4.2 Server Configuration
```
HOST = 0.0.0.0
PORT = 10000
DEBUG = False
```

### 4.3 Model Configuration
```
LLM_MODEL = gpt-3.5-turbo
EMBEDDING_MODEL = text-embedding-3-small
MAX_TOKENS = 2000
TEMPERATURE = 0.1
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
MAX_DOCUMENT_SIZE = 10485760
```

## Step 5: Advanced Settings

### 5.1 Auto-Deploy
- ✅ **Auto-Deploy**: Enabled
- ✅ **Deploy on Push**: Enabled

### 5.2 Health Check Path
```
Health Check Path: /health
```

### 5.3 Instance Type
```
Instance Type: Free (768 MB RAM, 0.1 CPU)
```

## Step 6: Deploy

1. Click **"Create Web Service"**
2. Wait for build to complete (2-3 minutes)
3. Check build logs for any errors

## Step 7: Verify Deployment

### 7.1 Check Service Status
- Go to your service dashboard
- Status should be **"Live"**
- URL will be: `https://your-app-name.onrender.com`

### 7.2 Test Endpoints
```bash
# Test root endpoint
curl https://your-app-name.onrender.com/

# Test health endpoint
curl https://your-app-name.onrender.com/health
```

### 7.3 Test Main Endpoint
```bash
curl -X POST https://your-app-name.onrender.com/hackrx/run \
  -H "Authorization: Bearer d809808918dd2a7d6b11fa5b23fa01e3abf9814dd225582d4d5674dc2138be0b" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
      "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"
    ]
  }'
```

## Step 8: Troubleshooting

### 8.1 Common Build Errors

**Error: Module not found**
```bash
# Solution: Check requirements.txt has all dependencies
pip install -r requirements.txt
```

**Error: Port binding**
```bash
# Solution: Use PORT environment variable
# main.py already handles this
```

**Error: Environment variables not found**
```bash
# Solution: Check all variables are set in Render dashboard
# No spaces around = sign
```

### 8.2 Runtime Errors

**Error: LLM not available**
```bash
# Check GROQ_API_KEY and OPENAI_API_KEY are set correctly
# Check API keys are valid
```

**Error: Pinecone connection failed**
```bash
# System will use fallback search automatically
# Not critical for functionality
```

### 8.3 Performance Issues

**Slow response times**
```bash
# Free tier has limitations
# Consider upgrading to paid plan for better performance
```

## Step 9: Final Verification

### 9.1 Test with Postman
1. Open Postman
2. Create new request:
   - **Method**: POST
   - **URL**: `https://your-app-name.onrender.com/hackrx/run`
   - **Headers**:
     ```
     Authorization: Bearer d809808918dd2a7d6b11fa5b23fa01e3abf9814dd225582d4d5674dc2138be0b
     Content-Type: application/json
     ```
   - **Body** (JSON):
     ```json
     {
       "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
       "questions": [
         "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"
       ]
     }
     ```

### 9.2 Expected Response
```json
{
  "answers": [
    "The grace period for premium payment under the National Parivar Mediclaim Plus Policy is thirty days."
  ]
}
```

## Step 10: Submit to Competition

1. **Copy your webhook URL**: `https://your-app-name.onrender.com/hackrx/run`
2. **Go to HackRx 6.0 submission page**
3. **Paste the webhook URL**
4. **Add description**: "FastAPI + Groq + Pinecone - Optimized for speed"
5. **Submit**

## ✅ Success Checklist

- [ ] Repository pushed to GitHub
- [ ] Render service created
- [ ] Environment variables set
- [ ] Build successful
- [ ] Service is live
- [ ] Health endpoint working
- [ ] Main endpoint responding
- [ ] Response format correct
- [ ] Response time under 30 seconds
- [ ] Webhook URL submitted to competition

## 🎉 Deployment Complete!

Your HackRx 6.0 system is now:
- ✅ Deployed on Render
- ✅ Accessible via HTTPS
- ✅ Ready for competition testing
- ✅ Optimized for performance

**Your webhook URL**: `https://your-app-name.onrender.com/hackrx/run` 