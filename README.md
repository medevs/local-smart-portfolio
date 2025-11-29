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

- **Docker** and **Docker Compose** (recommended)
- OR **Python 3.11+**, **Node.js 18+**, and **Ollama** for local development

---

## 🐳 Docker Deployment (Recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd portfolio
```

### Step 2: Configure Environment Variables

Create a `backend/.env` file:

```bash
cd backend
cp .env.example .env  # If .env.example exists
# OR create .env manually
```

Edit `backend/.env`:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:3b

# ChromaDB Configuration
CHROMA_PERSIST_DIR=./data/chroma_db
CHROMA_COLLECTION_NAME=portfolio_docs

# Security (REQUIRED - Generate a secure key)
ADMIN_API_KEY=your-secure-api-key-here

# CORS Settings (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Optional: Other settings
DEBUG=false
```

**Generate a secure API key:**

```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OR using OpenSSL
openssl rand -base64 32
```

### Step 3: Configure Frontend

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ADMIN_API_KEY=your-admin-api-key-here
```

### Step 4: Start Services

```bash
# Build and start all services
docker compose up -d

# Check service status
docker compose ps
```

### Step 5: Initialize Ollama Model

```bash
# Download the LLM model (this may take 5-15 minutes, ~2GB)
docker compose exec ollama ollama pull llama3.2:3b
```

### Step 6: Access the Application

- **Portfolio**: http://localhost:3000
- **Admin Dashboard**: http://localhost:3000/admin
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 💻 Local Development (Without Docker)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (see Docker section above)
# Then start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
pnpm install
# OR
npm install

# Create .env.local file (see Docker section above)
# Then start the development server
pnpm dev
# OR
npm run dev
```

### Start Ollama

```bash
# Install Ollama from https://ollama.ai
# Then start the service
ollama serve

# Download the model
ollama pull llama3.2:3b
```

---

## 📁 Project Structure

```
portfolio/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── routers/      # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── models/       # Pydantic models
│   │   └── utils/        # Utilities
│   ├── data/             # ChromaDB and document storage
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/             # Next.js frontend
│   ├── app/              # Next.js app router pages
│   ├── components/       # React components
│   ├── data/             # Static data files (customize these!)
│   ├── lib/              # Utilities & API client
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml     # Docker configuration
├── docker-compose.prod.yml # Production overrides
└── README.md
```

---

## 🎯 Customization

### Update Personal Information

Edit `frontend/data/personal.ts` with your information:
- Personal details (name, email, location, bio)
- Work experience
- Education
- Skills
- Social media links

### Update Portfolio Content

- **Projects**: `frontend/data/projects.ts`
- **Timeline**: `frontend/data/timeline.ts`
- **Skills**: `frontend/data/skills.tsx`
- **Page Content**: `frontend/data/pageContent.ts`
- **About Section**: `frontend/data/about.tsx`

### Customize Styling

The portfolio uses an amber/gold color scheme. To customize:

1. **Global Styles**: Edit `frontend/app/globals.css`
2. **Color Variables**: Update CSS custom properties
3. **Components**: Modify Tailwind classes in component files
4. **Theme**: Adjust colors in `frontend/components/layout/ClientLayout.tsx`

### Change AI Model

To use a different Ollama model:

1. Update `OLLAMA_MODEL` in `backend/.env`
2. Pull the new model: `docker compose exec ollama ollama pull <model-name>`
3. Restart the backend: `docker compose restart backend`

---

## 🔧 Docker Commands

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f backend
docker compose logs -f frontend

# Restart a service
docker compose restart backend

# Rebuild and restart
docker compose up -d --build

# Check service status
docker compose ps

# Execute commands in containers
docker compose exec backend bash
docker compose exec frontend sh
```

---

## 🚀 Production Deployment

For production, use the production override:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

The production configuration:
- Removes port mappings (use a reverse proxy)
- Sets resource limits
- Disables debug mode
- Includes Nginx reverse proxy (optional)

### Using a Reverse Proxy

Recommended reverse proxies:
- **Nginx**
- **Traefik**
- **Caddy**

Example Nginx configuration is available in `infra/nginx/`.

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

### Document Upload (RAG)
```http
POST /ingest
Content-Type: multipart/form-data
X-Admin-Key: <your-api-key>

file: <document-file>
```

### Admin Operations

**Get Statistics:**
```http
GET /admin/stats
X-Admin-Key: <your-api-key>
```

**List Documents:**
```http
GET /documents
X-Admin-Key: <your-api-key>
```

**Delete Document:**
```http
DELETE /documents/{id}
X-Admin-Key: <your-api-key>
```

---

## 🔒 Security Notes

1. **API Key**: Always use a strong, randomly generated API key
2. **Environment Variables**: Never commit `.env` files to version control
3. **CORS**: Configure `CORS_ORIGINS` properly for production
4. **Reverse Proxy**: Use HTTPS in production with a reverse proxy
5. **Firewall**: Restrict access to admin endpoints

---

## 🐛 Troubleshooting

### Services won't start

```bash
# Check logs
docker compose logs

# Check if ports are in use
netstat -tulpn | grep -E ':(3000|8000|11434)'

# Rebuild containers
docker compose up -d --build
```

### Ollama model not loading

```bash
# Check Ollama logs
docker compose logs ollama

# Manually pull the model
docker compose exec ollama ollama pull llama3.2:3b

# List available models
docker compose exec ollama ollama list
```

### Frontend can't connect to backend

1. Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
2. Verify backend is running: `docker compose ps`
3. Check CORS settings in `backend/.env`
4. Check browser console for errors

### ChromaDB issues

```bash
# Reset ChromaDB (WARNING: Deletes all data)
docker compose down
docker volume rm portfolio_chroma_data
docker compose up -d
```

---

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Ollama Documentation](https://ollama.ai/docs)
- [ChromaDB Documentation](https://docs.trychroma.com)

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
