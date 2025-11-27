I'll analyze your PRD and project structure to create a comprehensive implementation plan. Let me first explore the entire project folder structure and existing files.

[22 tools called]

Now I have a complete picture of your project. Let me create a comprehensive implementation plan.

---

# 📋 COMPLETE IMPLEMENTATION PLAN
## AI-Powered Portfolio Website & Personal Homelab Assistant

---

## 📊 PROJECT ANALYSIS SUMMARY

### Current State Assessment

| Component | Status | Notes |
|-----------|--------|-------|
| **Frontend** | ⚠️ Scaffolded | Next.js 15.5.5 initialized, basic template, has axios/swr/zustand |
| **Backend** | ❌ Empty | Folder structure exists, venv created, no code |
| **RAG System** | ❌ Not started | No ChromaDB, embeddings, or Ollama integration |
| **Admin Dashboard** | ❌ Not started | No upload/management UI |
| **Docker** | ❌ Not configured | No docker-compose.dev.yml |
| **Environment** | ❌ Missing | No .env files or configuration |

### Missing from PRD (Gaps Identified)

1. **No `requirements.txt`** - Python dependencies not defined
2. **No error handling strategy** - How to handle RAG failures, Ollama timeouts
3. **No CORS configuration** - Frontend/Backend communication
4. **No rate limiting spec** - Protecting the chat endpoint
5. **No session management details** - How chat history is stored
6. **No document storage path** - Where uploaded files go
7. **No shadcn/ui installed** - Listed in PRD but not set up
8. **No specific Ollama model** - phi3/llama3/mistral - which to default to?

---

## 🏗️ HIGH-LEVEL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           LOCAL DEVELOPMENT                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────┐     ┌─────────────────────────────────────────┐ │
│  │   Next.js Frontend │     │              FastAPI Backend            │ │
│  │    localhost:3000  │────▶│             localhost:8000              │ │
│  │                    │     │                                         │ │
│  │  • Portfolio Pages │     │  ┌─────────────────────────────────┐   │ │
│  │  • Chat Interface  │     │  │         RAG Pipeline            │   │ │
│  │  • Admin Dashboard │     │  │  • Embeddings (sentence-trans)  │   │ │
│  └────────────────────┘     │  │  • Chunking (langchain)         │   │ │
│                             │  │  • Retrieval                    │   │ │
│                             │  └─────────────────────────────────┘   │ │
│                             │                                         │ │
│                             │  ┌─────────────┐  ┌─────────────────┐  │ │
│                             │  │  ChromaDB   │  │     Ollama      │  │ │
│                             │  │ (embedded)  │  │ localhost:11434 │  │ │
│                             │  │ ./chroma_db │  │  (phi3/llama3)  │  │ │
│                             │  └─────────────┘  └─────────────────┘  │ │
│                             └─────────────────────────────────────────┘ │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                      File Storage                                   │ │
│  │  ./data/documents/  - Uploaded PDFs, Markdown, etc.                │ │
│  │  ./data/chroma_db/  - Vector database persistence                  │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔗 DEPENDENCY DIAGRAM

```
                    ┌──────────────────────┐
                    │   1. Environment     │
                    │   Setup & Config     │
                    └──────────┬───────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
            ▼                  ▼                  ▼
   ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
   │ 2A. Backend    │ │ 2B. Frontend   │ │ 2C. Ollama     │
   │ Foundation     │ │ Foundation     │ │ Local Setup    │
   │ (FastAPI)      │ │ (Next.js)      │ │                │
   └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
           │                  │                  │
           ▼                  │                  │
   ┌────────────────┐         │                  │
   │ 3. RAG System  │◀────────┘                  │
   │ (ChromaDB +    │◀──────────────────────────┘
   │  Embeddings)   │
   └───────┬────────┘
           │
           ▼
   ┌────────────────┐
   │ 4. Chat API    │
   │ (Streaming)    │
   └───────┬────────┘
           │
           ▼
   ┌────────────────┐
   │ 5. Chat UI     │
   │ (Frontend)     │
   └───────┬────────┘
           │
           ▼
   ┌────────────────┐
   │ 6. Document    │
   │ Ingestion API  │
   └───────┬────────┘
           │
           ▼
   ┌────────────────┐
   │ 7. Admin       │
   │ Dashboard      │
   └───────┬────────┘
           │
           ▼
   ┌────────────────┐
   │ 8. Portfolio   │
   │ Pages          │
   └───────┬────────┘
           │
           ▼
   ┌────────────────┐
   │ 9. Docker      │
   │ Local Compose  │
   └────────────────┘
```

---

## 📁 COMPLETE FILE STRUCTURE PLAN

### Backend Files to Create

```
backend/
├── app/
│   ├── __init__.py              ✅ (exists, needs update)
│   ├── main.py                  ✅ (exists, needs full implementation)
│   ├── config.py                🆕 CREATE - Environment configuration
│   ├── models/
│   │   ├── __init__.py          🆕 CREATE
│   │   ├── chat.py              🆕 CREATE - Chat request/response models
│   │   ├── document.py          🆕 CREATE - Document models
│   │   └── response.py          🆕 CREATE - API response models
│   ├── routers/
│   │   ├── __init__.py          🆕 CREATE
│   │   ├── chat.py              🆕 CREATE - Chat endpoint
│   │   ├── ingest.py            🆕 CREATE - Document ingestion
│   │   ├── admin.py             🆕 CREATE - Admin operations
│   │   └── health.py            🆕 CREATE - Health check
│   ├── services/
│   │   ├── __init__.py          🆕 CREATE
│   │   ├── rag.py               🆕 CREATE - RAG pipeline
│   │   ├── embeddings.py        🆕 CREATE - Embedding service
│   │   ├── ollama_client.py     🆕 CREATE - Ollama integration
│   │   ├── chroma_client.py     🆕 CREATE - ChromaDB operations
│   │   └── document_loader.py   🆕 CREATE - File processing
│   └── utils/
│       ├── __init__.py          🆕 CREATE
│       ├── chunking.py          🆕 CREATE - Text chunking
│       └── logger.py            🆕 CREATE - Logging setup
├── requirements.txt             🆕 CREATE - Python dependencies
├── .env.example                 🆕 CREATE - Environment template
└── data/
    ├── documents/               🆕 CREATE - Document storage
    └── chroma_db/               🆕 CREATE - Vector DB persistence
```

### Frontend Files to Create/Modify

```
frontend/
├── app/
│   ├── layout.tsx               ✅ (modify - add providers, theme)
│   ├── page.tsx                 ✅ (modify - landing page)
│   ├── globals.css              ✅ (modify - custom styles)
│   ├── providers.tsx            🆕 CREATE - Client providers
│   ├── (portfolio)/             🆕 CREATE - Route group
│   │   ├── page.tsx             🆕 CREATE - Home/landing
│   │   ├── projects/
│   │   │   ├── page.tsx         🆕 CREATE - Projects list
│   │   │   └── [slug]/
│   │   │       └── page.tsx     🆕 CREATE - Project detail
│   │   ├── about/
│   │   │   └── page.tsx         🆕 CREATE - About page
│   │   └── contact/
│   │       └── page.tsx         🆕 CREATE - Contact page
│   ├── chat/
│   │   └── page.tsx             🆕 CREATE - Full chat page
│   └── admin/
│       ├── layout.tsx           🆕 CREATE - Admin layout
│       ├── page.tsx             🆕 CREATE - Admin dashboard
│       ├── upload/
│       │   └── page.tsx         🆕 CREATE - Upload documents
│       └── documents/
│           └── page.tsx         🆕 CREATE - Manage documents
├── components/
│   ├── ui/                      🆕 CREATE - shadcn components
│   ├── layout/
│   │   ├── Header.tsx           🆕 CREATE - Navigation header
│   │   ├── Footer.tsx           🆕 CREATE - Site footer
│   │   └── Sidebar.tsx          🆕 CREATE - Sidebar navigation
│   ├── chat/
│   │   ├── ChatWindow.tsx       🆕 CREATE - Main chat container
│   │   ├── ChatInput.tsx        🆕 CREATE - Message input
│   │   ├── MessageBubble.tsx    🆕 CREATE - Chat message
│   │   ├── ChatHistory.tsx      🆕 CREATE - Message list
│   │   └── TypingIndicator.tsx  🆕 CREATE - Loading indicator
│   ├── portfolio/
│   │   ├── Hero.tsx             🆕 CREATE - Hero section
│   │   ├── ProjectCard.tsx      🆕 CREATE - Project card
│   │   ├── SkillBadge.tsx       🆕 CREATE - Skill display
│   │   └── ContactForm.tsx      🆕 CREATE - Contact form
│   └── admin/
│       ├── FileUpload.tsx       🆕 CREATE - Upload component
│       ├── DocumentList.tsx     🆕 CREATE - Document table
│       └── StatusBadge.tsx      🆕 CREATE - Status indicator
├── lib/
│   ├── api/
│   │   ├── client.ts            🆕 CREATE - API client
│   │   ├── chat.ts              🆕 CREATE - Chat API functions
│   │   └── documents.ts         🆕 CREATE - Document API
│   ├── hooks/
│   │   ├── useChat.ts           🆕 CREATE - Chat hook
│   │   └── useDocuments.ts      🆕 CREATE - Documents hook
│   ├── store/
│   │   └── chatStore.ts         🆕 CREATE - Zustand store
│   └── utils/
│       └── cn.ts                🆕 CREATE - Classname utility
├── types/
│   └── index.ts                 🆕 CREATE - TypeScript types
├── .env.local.example           🆕 CREATE - Environment template
└── components.json              🆕 CREATE - shadcn config
```

### Root Project Files

```
portfolio/
├── docker-compose.dev.yml       🆕 CREATE - Local development
├── .gitignore                   🆕 CREATE - Git ignore
├── README.md                    🆕 CREATE - Project documentation
└── .env.example                 🆕 CREATE - Root env template
```

---

## 🗓️ IMPLEMENTATION ROADMAP (MILESTONES)

### **PHASE 1: Environment & Foundation** (Day 1)
> Goal: Get both frontend and backend running locally with health checks

| Task | Files | Verification |
|------|-------|--------------|
| 1.1 Create backend requirements.txt | `backend/requirements.txt` | File exists |
| 1.2 Create backend config | `backend/app/config.py` | Import works |
| 1.3 Create logger utility | `backend/app/utils/logger.py` | Logs print |
| 1.4 Implement main.py with CORS | `backend/app/main.py` | Server starts |
| 1.5 Create health router | `backend/app/routers/health.py` | GET /health returns 200 |
| 1.6 Create .env files | `.env`, `backend/.env`, `frontend/.env.local` | Configs load |
| 1.7 Install shadcn/ui | `frontend/components.json`, `frontend/components/ui/*` | Components available |
| 1.8 Create cn utility | `frontend/lib/utils/cn.ts` | Import works |

**Verification Step:**
```bash
# Terminal 1 - Backend
cd backend && source venv/Scripts/activate && pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Visit: http://localhost:8000/health → {"status": "healthy"}

# Terminal 2 - Frontend
cd frontend && pnpm dev
# Visit: http://localhost:3000 → Page loads
```

---

### **PHASE 2: Backend Models & Base Services** (Day 1-2)
> Goal: Define data models and create service scaffolding

| Task | Files | Verification |
|------|-------|--------------|
| 2.1 Create Pydantic models | `backend/app/models/*.py` | Import without errors |
| 2.2 Create Ollama client service | `backend/app/services/ollama_client.py` | Connection test passes |
| 2.3 Create ChromaDB client | `backend/app/services/chroma_client.py` | DB initializes |
| 2.4 Create embeddings service | `backend/app/services/embeddings.py` | Embeddings generate |
| 2.5 Create document loader | `backend/app/services/document_loader.py` | Files parse |
| 2.6 Create chunking utility | `backend/app/utils/chunking.py` | Text chunks correctly |

**Verification Step:**
```bash
# Test Ollama is running
curl http://localhost:11434/api/tags
# Should list available models

# Test embedding
python -c "from app.services.embeddings import get_embedding; print(get_embedding('test')[:5])"
```

---

### **PHASE 3: RAG Pipeline** (Day 2-3)
> Goal: Complete RAG system - ingest, embed, store, retrieve

| Task | Files | Verification |
|------|-------|--------------|
| 3.1 Implement full RAG service | `backend/app/services/rag.py` | Query returns context |
| 3.2 Create ingest router | `backend/app/routers/ingest.py` | POST /ingest works |
| 3.3 Create admin router | `backend/app/routers/admin.py` | GET /documents works |
| 3.4 Wire all routers in main | `backend/app/main.py` | All endpoints accessible |
| 3.5 Test with sample document | Manual test | Upload → Query returns relevant text |

**Verification Step:**
```bash
# Upload a test document
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@docs/PRD.md"
# → {"status": "success", "chunks": 25}

# List documents
curl http://localhost:8000/documents
# → [{"id": "...", "name": "PRD.md", "chunks": 25}]
```

---

### **PHASE 4: Chat API with Streaming** (Day 3-4)
> Goal: Working chat endpoint with streaming responses

| Task | Files | Verification |
|------|-------|--------------|
| 4.1 Create chat router with SSE | `backend/app/routers/chat.py` | POST /chat streams |
| 4.2 Integrate RAG in chat | `backend/app/services/rag.py` | Context retrieved |
| 4.3 Format prompt for Ollama | `backend/app/services/ollama_client.py` | Good responses |
| 4.4 Add chat history support | `backend/app/routers/chat.py` | Multi-turn works |

**Verification Step:**
```bash
# Test chat with streaming
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is this portfolio about?"}' \
  --no-buffer
# → Streaming response about the portfolio
```

---

### **PHASE 5: Frontend Foundation** (Day 4-5)
> Goal: Portfolio pages and navigation structure

| Task | Files | Verification |
|------|-------|--------------|
| 5.1 Create layout with providers | `frontend/app/layout.tsx`, `providers.tsx` | Theme works |
| 5.2 Create Header component | `frontend/components/layout/Header.tsx` | Navigation renders |
| 5.3 Create Footer component | `frontend/components/layout/Footer.tsx` | Footer renders |
| 5.4 Create landing page | `frontend/app/page.tsx` | Hero displays |
| 5.5 Create About page | `frontend/app/(portfolio)/about/page.tsx` | Content displays |
| 5.6 Create Projects page | `frontend/app/(portfolio)/projects/page.tsx` | Cards display |
| 5.7 Create API client | `frontend/lib/api/client.ts` | Requests work |
| 5.8 Create TypeScript types | `frontend/types/index.ts` | Types available |

**Verification Step:**
```bash
pnpm dev
# Visit: http://localhost:3000 → Beautiful landing page
# Navigate to /about → About page loads
# Navigate to /projects → Projects display
```

---

### **PHASE 6: Chat UI** (Day 5-6)
> Goal: Fully functional chat interface with streaming

| Task | Files | Verification |
|------|-------|--------------|
| 6.1 Create Zustand chat store | `frontend/lib/store/chatStore.ts` | State manages |
| 6.2 Create chat API functions | `frontend/lib/api/chat.ts` | API calls work |
| 6.3 Create useChat hook | `frontend/lib/hooks/useChat.ts` | Hook functional |
| 6.4 Create ChatWindow component | `frontend/components/chat/ChatWindow.tsx` | Container renders |
| 6.5 Create MessageBubble | `frontend/components/chat/MessageBubble.tsx` | Messages display |
| 6.6 Create ChatInput | `frontend/components/chat/ChatInput.tsx` | Input works |
| 6.7 Create TypingIndicator | `frontend/components/chat/TypingIndicator.tsx` | Loading shows |
| 6.8 Create chat page | `frontend/app/chat/page.tsx` | Full chat works |
| 6.9 Add floating chat widget | `frontend/components/chat/ChatWidget.tsx` | Widget on all pages |

**Verification Step:**
```bash
pnpm dev
# Visit: http://localhost:3000/chat
# Type: "What is this portfolio about?"
# → Streaming response appears
# → Chat history persists in session
```

---

### **PHASE 7: Admin Dashboard** (Day 6-7)
> Goal: Upload documents, view status, manage knowledge base

| Task | Files | Verification |
|------|-------|--------------|
| 7.1 Create admin layout | `frontend/app/admin/layout.tsx` | Admin shell renders |
| 7.2 Create admin dashboard | `frontend/app/admin/page.tsx` | Stats display |
| 7.3 Create FileUpload component | `frontend/components/admin/FileUpload.tsx` | Upload works |
| 7.4 Create DocumentList component | `frontend/components/admin/DocumentList.tsx` | Docs list |
| 7.5 Create upload page | `frontend/app/admin/upload/page.tsx` | Full upload flow |
| 7.6 Create documents page | `frontend/app/admin/documents/page.tsx` | Management works |
| 7.7 Create useDocuments hook | `frontend/lib/hooks/useDocuments.ts` | Data fetches |
| 7.8 Implement delete functionality | Backend + Frontend | Delete works |

**Verification Step:**
```bash
# Visit: http://localhost:3000/admin
# → Dashboard with stats
# Visit: http://localhost:3000/admin/upload
# → Upload a PDF → Success message
# Visit: http://localhost:3000/admin/documents
# → See uploaded document → Delete works
```

---

### **PHASE 8: Polish & Integration** (Day 7-8)
> Goal: Responsive design, error handling, final testing

| Task | Files | Verification |
|------|-------|--------------|
| 8.1 Add error boundaries | Various components | Errors handled gracefully |
| 8.2 Add loading states | Various components | Loading indicators show |
| 8.3 Mobile responsiveness | All components | Works on mobile |
| 8.4 Add toast notifications | Install sonner + integrate | Toasts display |
| 8.5 Final styling pass | `globals.css`, components | Looks polished |
| 8.6 Test all user flows | Manual testing | Everything works |

---

### **PHASE 9: Docker Local Environment** (Day 8)
> Goal: Single command to start entire stack

| Task | Files | Verification |
|------|-------|--------------|
| 9.1 Create backend Dockerfile | `backend/Dockerfile.dev` | Image builds |
| 9.2 Create frontend Dockerfile | `frontend/Dockerfile.dev` | Image builds |
| 9.3 Create docker-compose.dev.yml | `docker-compose.dev.yml` | Stack starts |
| 9.4 Add volume mounts for dev | `docker-compose.dev.yml` | Hot reload works |
| 9.5 Test full stack in Docker | Run compose | All services up |

**Verification Step:**
```bash
docker-compose -f docker-compose.dev.yml up
# → Backend: http://localhost:8000
# → Frontend: http://localhost:3000
# → All features work
```

---

## 📦 PYTHON DEPENDENCIES (requirements.txt)

```txt
# Core
fastapi==0.115.0
uvicorn[standard]==0.32.0
python-multipart==0.0.12
python-dotenv==1.0.1

# RAG & AI
chromadb==0.5.23
langchain==0.3.7
langchain-community==0.3.5
langchain-text-splitters==0.3.2
sentence-transformers==3.3.0
httpx==0.28.0

# Document Processing
pypdf==5.1.0
python-docx==1.1.2
markdown==3.7

# Utilities
pydantic==2.9.2
pydantic-settings==2.6.1
loguru==0.7.2

# Development
watchfiles==0.24.0
```

---

## 🎯 PRIORITIZED CODE GENERATION ORDER

Based on dependencies and critical path:

### **Priority 1 - Must Generate First**
1. `backend/requirements.txt`
2. `backend/app/config.py`
3. `backend/app/utils/logger.py`
4. `backend/app/main.py` (with CORS)
5. `backend/app/routers/health.py`
6. `backend/app/models/__init__.py` + `chat.py` + `document.py`

### **Priority 2 - Core Services**
7. `backend/app/services/embeddings.py`
8. `backend/app/services/chroma_client.py`
9. `backend/app/services/ollama_client.py`
10. `backend/app/utils/chunking.py`
11. `backend/app/services/document_loader.py`
12. `backend/app/services/rag.py`

### **Priority 3 - Backend APIs**
13. `backend/app/routers/ingest.py`
14. `backend/app/routers/chat.py`
15. `backend/app/routers/admin.py`

### **Priority 4 - Frontend Foundation**
16. `frontend/lib/utils/cn.ts`
17. `frontend/types/index.ts`
18. `frontend/lib/api/client.ts`
19. `frontend/app/providers.tsx`
20. `frontend/app/layout.tsx` (updated)
21. `frontend/components/layout/Header.tsx`
22. `frontend/components/layout/Footer.tsx`

### **Priority 5 - Chat System**
23. `frontend/lib/store/chatStore.ts`
24. `frontend/lib/api/chat.ts`
25. `frontend/lib/hooks/useChat.ts`
26. `frontend/components/chat/*`
27. `frontend/app/chat/page.tsx`

### **Priority 6 - Portfolio Pages**
28. `frontend/app/page.tsx` (landing)
29. `frontend/app/(portfolio)/about/page.tsx`
30. `frontend/app/(portfolio)/projects/page.tsx`
31. `frontend/components/portfolio/*`

### **Priority 7 - Admin Dashboard**
32. `frontend/lib/hooks/useDocuments.ts`
33. `frontend/components/admin/*`
34. `frontend/app/admin/*`

### **Priority 8 - Docker**
35. `docker-compose.dev.yml`
36. `backend/Dockerfile.dev`
37. `frontend/Dockerfile.dev`

---

## 🔧 RECOMMENDED PRD IMPROVEMENTS

1. **Add Default Ollama Model**: Specify `phi3:mini` as default (fastest for local)
2. **Add Session Storage**: Use localStorage for chat history (client-side)
3. **Add Rate Limiting**: 10 requests/minute per IP for chat endpoint
4. **Add Document Size Limits**: Max 10MB per file, 50MB total
5. **Add Supported File Types**: `.md`, `.txt`, `.pdf`, `.docx`
6. **Add Error Messages**: Define user-friendly error messages
7. **Add Loading States**: Define skeleton UIs for each section
8. **Add Admin Authentication**: Simple API key check for admin routes
9. **Add Chunk Size Config**: 500 tokens with 50 token overlap (configurable)
10. **Add Context Window**: Max 3 retrieved chunks per query

---

## 🚀 IMMEDIATE NEXT STEP

**We should start with Phase 1, Task 1.1: Creating the backend foundation.**

This means:
1. Create `backend/requirements.txt` with all Python dependencies
2. Create `backend/app/config.py` for environment configuration
3. Create `backend/app/utils/logger.py` for structured logging
4. Update `backend/app/main.py` with FastAPI app, CORS, and router setup
5. Create `backend/app/routers/health.py` for health check endpoint
6. Create environment files (`.env.example`, `backend/.env`)

**Would you like me to start generating the code for Phase 1?** I'll create all the foundation files needed to get the backend server running with a health check endpoint, then we can verify it works before moving to Phase 2.