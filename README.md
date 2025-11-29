# 🚀 AI-Powered Portfolio Website

A modern, self-hosted portfolio website with an AI assistant powered by local LLMs and RAG technology.

<div align="center">

![Next.js](https://img.shields.io/badge/Next.js-15.5.5-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green?style=for-the-badge&logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=for-the-badge&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)

*Showcase your work with a beautiful portfolio and intelligent AI assistant*

</div>

---

## ✨ Features

- **🎨 Modern Portfolio**: Beautiful, responsive design showcasing projects, skills, and experience
- **🤖 AI Assistant**: Local LLM-powered chatbot with RAG for intelligent responses
- **🔒 Privacy-First**: All AI processing happens locally - no data leaves your server
- **📊 Real-time Metrics**: Display live system status and LLM performance benchmarks
- **🏠 Homelab Integration**: Showcase your homelab journey and infrastructure
- **📱 Fully Responsive**: Mobile-first design that works on all devices

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15.5.5 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS 4.0
- **UI Components**: shadcn/ui + Radix UI
- **Animations**: Framer Motion
- **Icons**: Lucide React + React Icons

### Backend
- **Framework**: FastAPI 0.115.0
- **Language**: Python 3.11+
- **Vector DB**: ChromaDB
- **LLM**: Ollama (local models)
- **Embeddings**: sentence-transformers

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ with pip
- Node.js 18+ with pnpm
- Ollama installed and running
- Git

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd portfolio

# Backend setup
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
pnpm install
```

### Configuration

Create environment files:

**Backend** (`backend/.env`):
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
CHROMA_PERSIST_DIR=./data/chroma_db
ADMIN_API_KEY=your-secure-api-key-here
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Run Development Servers

```bash
# Terminal 1: Start Ollama
ollama serve
ollama pull llama3.2:3b

# Terminal 2: Backend
cd backend
source venv/Scripts/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3: Frontend
cd frontend
pnpm dev
```

Access the application:
- **Portfolio**: http://localhost:3000
- **Admin Dashboard**: http://localhost:3000/admin
- **API Docs**: http://localhost:8000/docs

---

## 🐳 Docker Deployment

```bash
# Start all services
docker compose up -d

# Initialize Ollama model
docker compose exec ollama ollama pull llama3.2:3b

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

---

## 📁 Project Structure

```
portfolio/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── routers/      # API endpoints
│   │   ├── services/     # Business logic
│   │   └── models/       # Pydantic models
│   └── requirements.txt
│
├── frontend/             # Next.js frontend
│   ├── app/              # Next.js app router pages
│   ├── components/       # React components
│   ├── data/             # Static data files
│   └── lib/              # Utilities & API client
│
└── docker-compose.yml    # Docker configuration
```

---

## 🎯 Customization

### Update Personal Information

Edit `frontend/data/personal.ts` with your information:
- Personal details (name, email, location)
- Work experience
- Education
- Skills
- Projects

### Update Portfolio Content

- **Projects**: `frontend/data/projects.ts`
- **Timeline**: `frontend/data/timeline.ts`
- **Skills**: `frontend/data/skills.tsx`
- **Page Content**: `frontend/data/pageContent.ts`
- **Homelab**: `frontend/data/homelab.tsx`

### Styling

The portfolio uses an amber/gold color scheme. To customize:
- Edit `frontend/app/globals.css` for global styles
- Modify Tailwind classes in components
- Update color variables in CSS

---

## 🔧 API Endpoints

### Health Check
```http
GET /health
```

### Chat (Streaming)
```http
POST /chat/stream
Content-Type: application/json

{
  "message": "Tell me about your projects",
  "history": []
}
```

### Document Upload
```http
POST /ingest
Content-Type: multipart/form-data

file: <document-file>
```

### Admin Operations
```http
GET /admin/stats
X-Admin-Key: <your-api-key>

DELETE /documents/{id}
X-Admin-Key: <your-api-key>
```

---

## 🤝 Contributing

This is an open-source portfolio template. Feel free to:

1. Fork the repository
2. Customize it for your own use
3. Submit improvements via Pull Requests

---

## 📄 License

MIT License - feel free to use this for your own portfolio!

---

## 🙏 Acknowledgments

- **Ollama** for local LLM inference
- **ChromaDB** for vector database
- **shadcn/ui** for beautiful components
- **Next.js** and **FastAPI** teams

---

<div align="center">

**Built with ❤️ using modern web technologies and AI**

</div>
