# AI-Powered Personal Finance Chatbot 🤖💰

A comprehensive financial management application that combines the power of IBM Granite 3.0-1B AI model with Groq's Llama-3-8B for intelligent financial advice, analysis, and professional report generation.

## ✨ Features

- **🧠 Advanced AI Integration**: IBM Granite 3.0-1B model for specialized financial analysis
- **💬 Intelligent Chat Interface**: Real-time financial conversations with adaptive tone
- **📊 Professional Reports**: Generate downloadable Word documents with comprehensive analysis
- **🗄️ Session Management**: SQLite database for persistent user sessions
- **🌍 Multi-language Support**: Available in 9 Indian languages
- **🎨 Modern UI**: Card-based responsive design with professional styling
- **⚡ Smart Fallback System**: 3-tier reliability (Granite → Groq → Structured reporting)
- **🔒 Financial Focus**: Keyword filtering ensures finance-only conversations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key ([Get one here](https://console.groq.com/keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nithyasri2007/Finance_Bot.git
   cd Finance_Bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn streamlit sqlite3 requests transformers torch python-docx groq python-dotenv
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Groq API key
   ```

5. **Initialize database**
   ```bash
   cd database
   python setup.py
   cd ..
   ```

### 🏃‍♂️ Running the Application

1. **Start the IBM Granite AI Service** (Terminal 1)
   ```bash
   cd backend
   python app1.py
   # Runs on http://localhost:8002
   ```

2. **Start the FastAPI Backend** (Terminal 2)
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   # Runs on http://localhost:8000
   ```

3. **Start the Streamlit Frontend** (Terminal 3)
   ```bash
   cd frontend
   streamlit run app.py --server.port 8502
   # Runs on http://localhost:8502
   ```

4. **Access the Application**
   Open your browser and navigate to `http://localhost:8502`

## 🏗️ Architecture

```
├── backend/
│   ├── main.py           # FastAPI server with financial analysis
│   ├── app1.py           # IBM Granite 3.0-1B AI service
│   └── modal_model.py    # Model configuration (deprecated)
├── frontend/
│   └── app.py            # Streamlit UI with modern card design
├── database/
│   └── setup.py          # SQLite database initialization
├── .env.example          # Environment variables template
└── reports/              # Generated Word documents (auto-created)
```

## 🛠️ API Endpoints

### FastAPI Backend (Port 8000)
- `POST /chat` - AI-powered financial conversations
- `POST /generate-report` - Generate comprehensive financial reports
- `POST /create-word-report` - Create downloadable Word documents
- `GET /sessions/{user_id}` - Retrieve user session data
- `POST /save-session` - Save user session data

### IBM Granite Service (Port 8002)
- `POST /generate` - Specialized AI financial analysis using IBM Granite 3.0-1B

## 🎯 Core Technologies

- **Backend**: FastAPI, SQLite, IBM Granite 3.0-1B, Groq API
- **Frontend**: Streamlit with custom CSS styling
- **AI Models**: IBM Granite 3.0-1B, Llama-3-8B (via Groq)
- **Database**: SQLite for session management
- **Document Generation**: python-docx for professional Word reports

## 🔧 Configuration

### Environment Variables (.env)
```env
GROQ_API_KEY=your-groq-api-key-here
```

### Model Configuration
- **IBM Granite**: Ultra-optimized with 256 tokens, temperature 0.5
- **Groq Llama-3**: Fallback system with comprehensive error handling
- **Timeout Handling**: 90-second Granite timeout with instant fallback

## 📝 Usage Examples

1. **Financial Chat**: Ask questions about budgeting, investments, savings
2. **Report Generation**: Create professional financial analysis documents
3. **Multi-language**: Switch between 9 Indian languages for localized advice
4. **Session Persistence**: Resume conversations across browser sessions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- IBM for the Granite 3.0-1B model
- Groq for the Llama-3-8B API access
- Streamlit for the amazing web framework
- FastAPI for the robust backend framework

---

**Made with ❤️ for better financial management**
