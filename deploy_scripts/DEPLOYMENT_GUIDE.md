# 🚀 HackRx 6.0 Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Code Review Complete
- [x] All imports working correctly
- [x] Missing httpx dependency added to requirements.txt
- [x] Version consistency fixed (2.0 throughout)
- [x] .gitignore expanded for proper deployment
- [x] All app components tested

### ✅ Files Ready for Deployment
- [x] `main.py` - FastAPI application
- [x] `config.py` - Configuration settings
- [x] `requirements.txt` - All dependencies including httpx
- [x] `Procfile` - Heroku deployment
- [x] `runtime.txt` - Python version specification
- [x] `README.md` - Project documentation
- [x] `.gitignore` - Proper exclusions
- [x] `app/` directory with all modules

## 🎯 Deployment Options

### 1. Railway (Recommended)
**Fastest deployment with automatic scaling**

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Initialize project
railway init

# 4. Set environment variables
railway variables set GROQ_API_KEY=your_groq_key
railway variables set OPENAI_API_KEY=your_openai_key
railway variables set PINECONE_API_KEY=your_pinecone_key
railway variables set PINECONE_ENVIRONMENT=us-east-1-aws

# 5. Deploy
railway up
```

### 2. Render
**Free tier with good performance**

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python main.py`
6. Add environment variables:
   - `GROQ_API_KEY`
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
   - `PINECONE_ENVIRONMENT`

### 3. Heroku
**Classic deployment option**

```bash
# 1. Install Heroku CLI
# 2. Login
heroku login

# 3. Create app
heroku create your-app-name

# 4. Set environment variables
heroku config:set GROQ_API_KEY=your_groq_key
heroku config:set OPENAI_API_KEY=your_openai_key
heroku config:set PINECONE_API_KEY=your_pinecone_key
heroku config:set PINECONE_ENVIRONMENT=us-east-1-aws

# 5. Deploy
git push heroku main
```

## 🔧 Environment Variables

### Required Variables
```env
# Primary LLM (Fastest)
GROQ_API_KEY=gsk_your_groq_api_key_here

# Fallback LLM
OPENAI_API_KEY=sk-your_openai_api_key_here

# Vector Database (Optional)
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=bajaj-documents
```

### Optional Variables
```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False  # Set to False for production
```

## 🧪 Testing Deployment

### 1. Run Local Tests
```bash
python deploy_scripts/test_deployment.py
```

### 2. Test API Endpoints
```bash
# Health check
curl -X GET "https://your-app-url.railway.app/health"

# Main endpoint
curl -X POST "https://your-app-url.railway.app/hackrx/run" \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/test.pdf",
    "questions": ["What is the grace period?"]
  }'
```

## 📊 Performance Monitoring

### Expected Performance
- **Single Question**: ~5 seconds
- **Multiple Questions**: ~4 seconds per question
- **10 Questions**: ~15 seconds total
- **Response Format**: JSON with answers array only

### Monitoring Endpoints
- `/health` - System health check
- `/api/v1/config` - Configuration status
- `/api/v1/cache/info` - Cache information

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Solution: Check requirements.txt includes all dependencies
   pip install -r requirements.txt
   ```

2. **Environment Variables Not Set**
   ```bash
   # Solution: Verify all required variables are set
   railway variables list
   ```

3. **Port Issues**
   ```bash
   # Solution: Use $PORT environment variable
   # Already configured in main.py
   ```

4. **Memory Issues**
   ```bash
   # Solution: Reduce chunk_size in config.py
   # Currently set to 800 for optimal performance
   ```

### Debug Mode
```bash
# Enable debug logging
DEBUG=True
```

## 🎉 Post-Deployment Checklist

- [ ] All tests pass locally
- [ ] Environment variables set correctly
- [ ] API endpoints responding
- [ ] Health check working
- [ ] Performance within limits (< 30 seconds)
- [ ] Error handling working
- [ ] Documentation updated

## 📞 Support

If you encounter issues:
1. Check the logs: `railway logs` or `heroku logs`
2. Verify environment variables
3. Test locally first
4. Check the test script output

## 🏆 Ready for HackRx 6.0!

Your deployment is ready for the competition. The system includes:
- ✅ Fast response times (< 30 seconds)
- ✅ Proper authentication
- ✅ JSON response format
- ✅ Error handling
- ✅ Document processing (PDF/DOCX)
- ✅ Multiple question support
- ✅ Fallback mechanisms

**Next Steps:**
1. Deploy to your chosen platform
2. Test with competition data
3. Submit webhook URL to HackRx 6.0
4. Monitor performance during competition 