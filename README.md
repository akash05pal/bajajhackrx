# 🚀 HackRx 6.0 - LLM-Powered Document Query System

An intelligent query-retrieval system for processing large documents and answering questions using LLM and vector search.

## 🎯 Features

- **Fast Response Times**: Under 30 seconds for multiple questions
- **Groq Integration**: Ultra-fast LLM responses (< 1 second)
- **Document Processing**: Supports PDF and DOCX files
- **Vector Search**: Semantic search with Pinecone/fallback
- **Caching**: Document caching for improved performance
- **Competition Ready**: Matches HackRx 6.0 requirements

## 📋 Requirements

- Python 3.8+
- FastAPI
- Groq API key (primary LLM)
- OpenAI API key (fallback)
- Pinecone API key (optional)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```env
# Required API Keys
GROQ_API_KEY=gsk_your_groq_api_key_here
OPENAI_API_KEY=sk-your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=bajaj-documents

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 3. Run the Server
```bash
python main.py
```

### 4. Test the API
```bash
python test_endpoints.py
```

## 📡 API Endpoints

### Main Competition Endpoint
**POST** `/hackrx/run`

**Headers:**
```
Authorization: Bearer d809808918dd2a7d6b11fa5b23fa01e3abf9814dd225582d4d5674dc2138be0b
Content-Type: application/json
```

**Request Body:**
```json
{
  "documents": "https://example.com/document.pdf",
  "questions": [
    "What is the grace period for premium payment?",
    "What are the coverage conditions?"
  ]
}
```

**Response:**
```json
{
  "answers": [
    "The grace period is thirty days.",
    "Coverage conditions include..."
  ]
}
```

### Other Endpoints
- **GET** `/` - Root endpoint
- **GET** `/health` - Health check
- **GET** `/api/v1/config` - Configuration info
- **GET** `/api/v1/cache/info` - Cache information

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Document      │    │   Vector        │    │   LLM           │
│   Processor     │───▶│   Store         │───▶│   Processor     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PDF/DOCX      │    │   Pinecone      │    │   Groq/OpenAI   │
│   Extraction    │    │   Fallback      │    │   Integration   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## ⚡ Performance Optimizations

- **Groq LLM**: Primary LLM for ultra-fast responses
- **Reduced Chunk Size**: 800 characters for faster processing
- **Parallel Processing**: Multiple questions processed simultaneously
- **Document Caching**: Prevents reprocessing same documents
- **Optimized Search**: Reduced search results (3 instead of 5)
- **Limited Context**: 1500 character context limit

## 📊 Performance Results

| Test Case | Response Time | Status |
|-----------|---------------|---------|
| Single Question | ~5 seconds | ✅ |
| Multiple Questions | ~4 seconds | ✅ |
| 10 Questions | ~15 seconds | ✅ |

## 🚀 Deployment

### Railway
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

### Render
1. Create new Web Service
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python main.py`
4. Add environment variables

### Heroku
1. Create new app
2. Connect GitHub repository
3. Set environment variables
4. Deploy

## 🔧 Configuration

Key settings in `config.py`:
- `chunk_size`: 800 (reduced for speed)
- `max_tokens`: 2000 (reduced for speed)
- `llm_model`: "gpt-3.5-turbo" (fallback)
- `embedding_model`: "text-embedding-3-small"

## 📝 Competition Requirements

✅ **Response Time**: Under 30 seconds  
✅ **Authentication**: Bearer token  
✅ **JSON Format**: Only answers array  
✅ **Document Processing**: PDF/DOCX support  
✅ **Multiple Questions**: Batch processing  
✅ **Error Handling**: Graceful failures  

## 🎉 Ready for Submission!

Your system is now:
- ✅ Optimized for speed
- ✅ Matches competition format
- ✅ Handles multiple questions
- ✅ Uses fast LLM (Groq)
- ✅ Ready for deployment

**Next Steps:**
1. Deploy to Railway/Render/Heroku
2. Test with competition data
3. Submit webhook URL to HackRx 6.0

## 📞 Support

For issues or questions, check the deployment guide or test scripts included in the project. 