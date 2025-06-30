# The Lean Brief - Backend API 🚀

> **AI-Powered News Processing Engine**

The backend API for The Lean Brief processes financial news articles using OpenAI's GPT models, categorizes them by market sectors, and provides intelligent summaries for the frontend.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-blue)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   News Sources  │    │   Flask API     │    │   Data Storage  │
│                 │    │                 │    │                 │
│ • Guardian      │───▶│ • /api/summarize│◀───│ • JSON Files    │
│ • NewsAPI       │    │ • /api/trigger  │    │ • Processed Data│
│ • Webz          │    │ • CORS Enabled  │    │ • Cache Files   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- **Python 3.8+**
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)
- **NewsAPI Key** - [Get one here](https://newsapi.org/register)
- **Guardian API Key** - [Get one here](https://open-platform.theguardian.com/access/)
- **Webz API Key** - [Get one here](https://webz.io/)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository (if not already done)
cd backend

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### 2. Configuration

Create a `.env` file in the backend directory:

```env
# Required API Keys
OPENAI_API_KEY=sk-your-openai-api-key-here
NEWSAPI_KEY=your-newsapi-key-here
GUARDIAN_API_KEY=your-guardian-api-key-here
WEBZ_API_KEY=your-webz-api-key-here

# Optional Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

### 3. Run the Application

```bash
# Development mode
python app.py

# Or with Flask CLI
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### 4. Verify Installation

```bash
# Test the health endpoint
curl http://localhost:5000/

# Test the main API endpoint
curl http://localhost:5000/api/summarize_news
```

## 📊 API Endpoints

### Health Check
```
GET /
```
Returns server status and basic information.

### Get Summarized News
```
GET /api/summarize_news
```
Returns processed and categorized news data for all market sectors.

**Response Format:**
```json
{
  "Technology & Software": {
    "landingSummary": "Recent developments in AI and cloud computing...",
    "topics": [
      {
        "name": "AI Breakthroughs",
        "description": "Latest developments in artificial intelligence",
        "summary": "Detailed analysis of AI developments...",
        "sources": ["Guardian", "TechCrunch"],
        "urls": ["https://...", "https://..."],
        "importance": 8.5
      }
    ]
  }
}
```

### Trigger Processing
```
POST /api/trigger_processing
```
Manually triggers the full news processing pipeline.

**Response:**
```json
{
  "message": "News processing pipeline triggered. Data will be updated shortly."
}
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | - | ✅ |
| `NEWSAPI_KEY` | NewsAPI key for news content | - | ✅ |
| `GUARDIAN_API_KEY` | Guardian API key | - | ✅ |
| `WEBZ_API_KEY` | Webz API key | - | ✅ |
| `FLASK_ENV` | Flask environment | `development` | ❌ |
| `FLASK_DEBUG` | Enable debug mode | `True` | ❌ |
| `PORT` | Server port | `5000` | ❌ |

### Market Sectors

The system automatically categorizes news into these sectors:

1. **Technology & Software**
2. **Finance & Economy**
3. **Healthcare & Biotech**
4. **Energy & Materials**
5. **Defense & Geopolitics**
6. **Cryptocurrency & Blockchain**
7. **Artificial Intelligence & Robotics**
8. **Retail & Consumer Goods**
9. **Automotive & Mobility**
10. **Real Estate & Infrastructure**

## 🛠️ Development

### Project Structure

```
backend/
├── app.py                 # Main Flask application
├── const.py              # Configuration constants
├── guardian.py           # Guardian API integration
├── insufficient_apis/    # Additional API integrations
│   ├── newsapi.py       # NewsAPI integration
│   └── webz.py          # Webz API integration
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── README.md            # This file
```

### Key Functions

#### `classify_sector_and_topic()`
- Classifies articles by market sector
- Identifies and groups related topics
- Assigns importance scores (1-10)

#### `summarize_content()`
- Generates AI-powered summaries
- Creates multi-level content analysis
- Handles different summary types

#### `run_full_processing_pipeline()`
- Orchestrates the entire processing workflow
- Manages data flow between components
- Handles error recovery

### Data Flow

1. **News Collection** → `fetch_and_store_news()`
2. **Classification** → `sort_by_sector_and_topic()`
3. **Summarization** → `summarize_sector_topic_map()`
4. **API Delivery** → `/api/summarize_news`

## 🚀 Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-key"
export NEWSAPI_KEY="your-key"
export GUARDIAN_API_KEY="your-key"
export WEBZ_API_KEY="your-key"

# Run the application
python app.py
```

### Production Deployment

#### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
# Build and run
docker build -t theleanbrief-backend .
docker run -p 5000:5000 --env-file .env theleanbrief-backend
```

#### Using Heroku

```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your-key
heroku config:set NEWSAPI_KEY=your-key
heroku config:set GUARDIAN_API_KEY=your-key
heroku config:set WEBZ_API_KEY=your-key
git push heroku main
```

### Environment Setup

#### Production Environment Variables

```bash
# Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=False

# Set API keys
export OPENAI_API_KEY="sk-..."
export NEWSAPI_KEY="..."
export GUARDIAN_API_KEY="..."
export WEBZ_API_KEY="..."
```

## 📊 Monitoring & Logging

### Log Levels

- **INFO**: General application flow
- **WARNING**: Non-critical issues
- **ERROR**: Critical errors requiring attention

### Key Metrics

- Processing time per article
- API response times
- Error rates
- Memory usage

### Health Checks

```bash
# Check API health
curl http://localhost:5000/

# Check data freshness
curl http://localhost:5000/api/summarize_news | jq '.'
```

## 🔒 Security

### Best Practices

1. **Environment Variables**: Never commit API keys to version control
2. **CORS Configuration**: Properly configured for frontend access
3. **Input Validation**: All inputs are validated and sanitized
4. **Rate Limiting**: Implement rate limiting for production

### Security Headers

```python
# Add security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

## 🐛 Troubleshooting

### Common Issues

#### OpenAI API Errors
```bash
# Check API key
echo $OPENAI_API_KEY

# Test API connection
python -c "import openai; openai.api_key='your-key'; print('Valid')"
```

#### Missing Dependencies
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Debug Mode

```bash
# Enable debug mode
export FLASK_DEBUG=True
python app.py
```

## 📈 Performance Optimization

### Caching

```python
# Implement Redis caching
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
```

### Async Processing

```python
# Use Celery for background tasks
from celery import Celery
celery = Celery('tasks', broker='redis://localhost:6379/0')
```

### Database Integration

```python
# Add PostgreSQL for persistent storage
import psycopg2
conn = psycopg2.connect("postgresql://user:pass@localhost/db")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

---

**For more information, see the main [README.md](../README.md)** 