# AI-Customer-Support-ChatBot
# 🤖 AI Customer Support Chatbot

A fully-featured AI-powered customer support chatbot built with Flask, Groq API, and a beautiful modern UI. This project simulates intelligent customer support interactions with FAQ handling, conversation memory, escalation scenarios, and voice input capabilities.

## ✨ Features

### Core Functionality
- **🤖 AI-Powered Responses** - Uses Groq API (Llama 3.3) for intelligent, context-aware responses
- **📚 FAQ Integration** - 40+ pre-configured FAQs across multiple categories
- **💬 Conversation Memory** - Maintains context throughout the conversation
- **🚨 Smart Escalation** - Automatically escalates complex queries to human agents
- **📊 Session Tracking** - SQLite database stores all conversations
- **📝 Conversation Summarization** - AI-generated summaries of chat sessions
- **💡 Suggested Actions** - Context-aware next-step suggestions

### User Interface
- **🎨 Modern, Professional Design** - Gradient purple theme with smooth animations
- **🍔 Burger Menu Navigation** - Clean side menu for all actions
- **🎤 Voice Input** - Speech-to-text functionality for hands-free messaging
- **📜 Chat History** - View and load previous conversations
- **⏱️ Message Timestamps** - Track when messages were sent
- **👤 User Labels** - Clear identification of user vs support agent messages
- **📱 Responsive Design** - Works on desktop and mobile devices

### Technical Features
- **🔧 REST API Backend** - Clean Flask API with CORS support
- **💾 Database Persistence** - SQLite for conversation storage
- **🔄 Real-time Updates** - Dynamic conversation loading
- **🎯 Action Buttons** - Interactive suggested actions
- **📋 FAQ Page** - Dedicated, searchable FAQ interface with collapsible categories

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Groq API Key (free at [console.groq.com](https://console.groq.com/))
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-customer-support-bot.git
cd ai-customer-support-bot
```

2. **Create and activate virtual environment**
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Create .env file
touch .env

# Add your Groq API key
echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
echo "DATABASE_PATH=./database.db" >> .env
```

5. **Run the application**

**Terminal 1 - Backend Server:**
```bash
python3 backend/app.py
```

**Terminal 2 - Frontend Server:**
```bash
cd frontend
python3 -m http.server 8000
```

6. **Access the application**
```
Open your browser and go to: http://localhost:8000
```

## 📁 Project Structure
```
ai-customer-support-bot/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration management
│   ├── database.py         # Database operations
│   ├── llm_service.py      # Groq API integration
│   └── models.py           # Data models
├── data/
│   └── faqs.json           # FAQ dataset (40+ questions)
├── frontend/
│   ├── index.html          # Main chat interface
│   ├── faqs.html           # FAQ page
│   └── faqs.json           # FAQ data (copy)
├── .env                    # Environment variables (not in repo)
├── .gitignore             # Git ignore file
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── database.db            # SQLite database (created automatically)
```

## 🔧 API Endpoints

### Chat Endpoint
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What are your business hours?",
  "session_id": "optional-session-id"
}

Response:
{
  "session_id": "unique-session-id",
  "response": "AI response text",
  "escalated": false,
  "suggested_actions": ["View FAQs", "Contact support"]
}
```

### Get Conversation
```http
GET /api/conversation/<session_id>

Response:
{
  "session_id": "session-id",
  "messages": [...],
  "escalated": false
}
```

### Get Conversation Summary
```http
GET /api/conversation/<session_id>/summary

Response:
{
  "session_id": "session-id",
  "summary": "AI-generated summary",
  "message_count": 10
}
```

### List All Conversations
```http
GET /api/conversations

Response:
{
  "conversations": [...],
  "count": 5
}
```

### Health Check
```http
GET /api/health

Response:
{
  "status": "healthy"
}
```

## 🎨 Customization

### Adding New FAQs
Edit `data/faqs.json`:
```json
{
  "faqs": [
    {
      "id": 41,
      "question": "Your question here?",
      "answer": "Your answer here.",
      "category": "category_name"
    }
  ]
}
```

### Changing AI Model
Edit `backend/llm_service.py`:
```python
model="llama-3.3-70b-versatile"  # Change to any Groq model
```

### Customizing Themes
Edit CSS in `frontend/index.html` - look for color gradients:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 🧪 Testing

### Test Backend API
```bash
# Health check
curl http://127.0.0.1:5000/api/health

# Send a message
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your business hours?"}'
```

### Test Voice Recording
1. Open chat interface
2. Click microphone button (🎤)
3. Allow microphone access
4. Speak your message
5. Recording converts to text automatically

## 📊 Technologies Used

### Backend
- **Flask** - Web framework
- **Groq API** - LLM provider (Llama 3.3)
- **SQLite** - Database
- **Python-dotenv** - Environment management

### Frontend
- **Vanilla JavaScript** - No frameworks needed
- **HTML5/CSS3** - Modern responsive design
- **Web Speech API** - Voice recording
- **Fetch API** - Async requests

## 🛠️ Troubleshooting

### Voice Recording Not Working
- **Chrome/Edge Only**: Speech recognition works best in Chrome or Edge
- **HTTPS Required**: For production, voice recording requires HTTPS
- **Permissions**: Make sure to allow microphone access

### Backend Not Starting
```bash
# Check if port 5000 is already in use
lsof -i :5000

# Use a different port
python3 backend/app.py --port 5001
```

### Frontend Not Loading FAQs
```bash
# Make sure faqs.json is in frontend folder
cp data/faqs.json frontend/faqs.json
```

### Database Issues
```bash
# Delete and recreate database
rm database.db
python3 backend/app.py
```

## 🚀 Deployment

### Deploy Backend (Heroku/Railway/Render)
1. Add `Procfile`:
```
web: python backend/app.py
```

2. Update `requirements.txt` with gunicorn:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

3. Update `backend/app.py` for production:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

### Deploy Frontend (Netlify/Vercel)
1. Update API URLs in `frontend/index.html`
2. Deploy frontend folder
3. Configure CORS in backend for production URL

## 📝 Environment Variables
```bash
# Required
GROQ_API_KEY=your_groq_api_key

# Optional
DATABASE_PATH=./database.db
```


## 🙏 Acknowledgments

- Groq for providing free, fast LLM API
- Flask community for excellent documentation
- UI inspiration from modern chat applications

## 📸 Screenshots

### Main Chat Interface
![Chat Interface](screenshots/chat.png)

### FAQ Page
![FAQ Page](screenshots/faqs.png)

### Burger Menu
![Menu](screenshots/menu.png)

---

**Made with ❤️ for better customer support**
