# 📋 Portfolio Update & Enhancement Plan

## Executive Summary

This plan outlines the comprehensive update of Ahmed's portfolio with:
1. **Real personal and professional data** (extracted from homelab journey documentation)
2. **Live homelab system metrics** (integrated from Prometheus/Grafana)
3. **Real LLM performance benchmarks** (from homelab Ollama instances)
4. **Separate data file structure** for maintainability
5. **Accurate homelab journey representation** based on actual documented experience

**Important Note:** This portfolio IS Ahmed's actual website. The previous research contained incorrect information about medevs.xyz and work experience. This plan is based solely on the documented homelab journey.

---

## 🔍 Phase 1: Research & Data Collection

### 1.1 Personal Information Research
**Status:** ✅ Research Complete (Based on Homelab Journey Document)

**Accurate Findings:**
- **Name:** Ahmed Oublihi
- **Username/Homelab Name:** medevs
- **Professional Focus:** DevOps, MLOps, and LLM Deployment Specialist
- **Current Website:** This portfolio (portfolio.medevs.local) - **THIS IS THE ACTUAL WEBSITE**
- **Professional Goals:**
  - Specialize in **DevOps**, **MLOps**, and **LLM deployment**
  - Learn local AI and on-premises systems
  - Prepare for future where local LLMs and self-hosted AI are standard
  - Learn by doing, not just theory
- **Current Focus:** 
  - Local AI deployment
  - LLM infrastructure
  - RAG systems
  - Homelab automation
  - Self-hosted AI systems

### 1.2 Homelab Infrastructure Analysis
**Status:** ✅ Fully Documented (From Homelab Journey)

**Actual Homelab Stack (Verified from Journey Document):**
- **Server:** Ubuntu Server 22.04 LTS
  - **Hostname:** medevs
  - **IP Addresses:** 
    - Wi-Fi: 192.168.178.23 (primary)
    - Ethernet: 192.168.178.24 (fallback)
  - **SSH Port:** 2222 (hardened)
  - **Username:** medevs
- **Hardware:**
  - CPU: Intel Core i5 (4th Gen)
  - RAM: 16GB DDR3
  - Storage: 1× SSD
  - GPU: None
  - Networking: RJ45 Ethernet + TP-Link USB Wi-Fi adapter (RTL8192EU)
- **Security:**
  - SSH key-only authentication (ED25519)
  - Password authentication disabled
  - UFW firewall configured
  - Fail2ban active
  - Unattended upgrades enabled
  - Root login disabled
- **Monitoring Stack:**
  - Prometheus (port 9090)
  - Grafana (port 3000) - accessible via grafana.local
  - cAdvisor (port 8082)
- **Services Running:**
  - Nginx Proxy Manager (ports 80/81/443)
  - Portainer (container management)
  - Dashy (homelab dashboard, port 8081)
  - Ollama (LLM server, port 11434)
  - Watchtower (auto-updates containers)
  - Portfolio App (port 3100, accessible via portfolio.medevs.local)
- **Domains Configured:**
  - portfolio.medevs.local (HTTPS with self-signed SAN certificate)
  - portfolio-api.medevs.local (HTTPS)
  - grafana.local
  - Various other .local domains
- **CI/CD:**
  - GitHub Actions workflow (.github/workflows/deploy.yml)
  - GitHub Container Registry (GHCR)
  - Automatic deployments via Watchtower
  - Images: ghcr.io/medevs/portfolio-frontend:latest, ghcr.io/medevs/portfolio-backend:latest

**Data Sources Available:**
1. **Prometheus Metrics:** 
   - System CPU, RAM, disk, network metrics
   - Container metrics via cAdvisor
   - PromQL queries already tested and working:
     - CPU: `100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)`
     - RAM: `100 * (1 - ((node_memory_MemAvailable_bytes) / (node_memory_MemTotal_bytes)))`
     - Disk: `100 - ((node_filesystem_avail_bytes{mountpoint="/",fstype!="tmpfs"} / node_filesystem_size_bytes{mountpoint="/",fstype!="tmpfs"}) * 100)`
2. **Grafana Dashboards:** Pre-configured with working queries
3. **Ollama API:** Model performance, token generation speed, memory usage (port 11434)
4. **cAdvisor:** Container resource usage (port 8082)
5. **System Metrics:** Uptime, network stats, container health

---

## 📁 Phase 2: Data Structure & File Organization

### 2.1 Create Separate Data File
**File:** `frontend/data/personal.ts`

**Structure:**
```typescript
export interface PersonalInfo {
  name: string;
  title: string;
  bio: string;
  location?: string;
  email?: string;
  website?: string;
  github?: string;
  linkedin?: string;
  twitter?: string;
}

export interface Experience {
  company: string;
  role: string;
  period: string;
  description: string;
  technologies: string[];
  achievements?: string[];
}

export interface Education {
  institution: string;
  degree: string;
  period: string;
  description?: string;
}

export interface Publication {
  title: string;
  authors: string[];
  journal?: string;
  year: string;
  link?: string;
  description?: string;
}

export interface Certification {
  name: string;
  issuer: string;
  date: string;
  credentialId?: string;
  link?: string;
}
```

### 2.2 Update Existing Data Files
- **`frontend/data/projects.ts`** - Update with real project data
- **`frontend/data/timeline.ts`** - Update with actual career timeline
- **`frontend/data/skills.tsx`** - Update with verified skill levels
- **`frontend/data/metrics.tsx`** - Convert to API-fetched data (remove static data)

---

## 🔌 Phase 3: Backend API Enhancements

### 3.1 Create Homelab Metrics Endpoint
**New File:** `backend/app/routers/metrics.py`

**Endpoint:** `GET /api/metrics/system`

**Functionality:**
- Fetch system metrics from Prometheus API
- Aggregate data: CPU, RAM, Disk, Network, Uptime
- Calculate trends (compare with previous values)
- Return formatted response

**Response Format:**
```json
{
  "timestamp": "2025-01-27T10:30:00Z",
  "metrics": {
    "cpu": {
      "usage_percent": 32.5,
      "cores": 8,
      "load_avg": [1.2, 1.5, 1.8]
    },
    "memory": {
      "used_gb": 8.2,
      "total_gb": 32,
      "usage_percent": 25.6
    },
    "disk": {
      "used_gb": 120,
      "total_gb": 500,
      "usage_percent": 24
    },
    "network": {
      "rx_mbps": 10.5,
      "tx_mbps": 2.3
    },
    "uptime": {
      "days": 45,
      "hours": 12,
      "uptime_percent": 99.8
    }
  },
  "trends": {
    "cpu": "+2%",
    "memory": "-1%",
    "disk": "+0.5%"
  }
}
```

**Implementation Options:**
1. **Direct Prometheus Query** (Recommended)
   - Use `prometheus-client` Python library
   - Query Prometheus REST API: `http://prometheus:9090/api/v1/query` (or `http://192.168.178.23:9090/api/v1/query` from host)
   - PromQL queries (already tested and working in Grafana - from Day 8):
     - CPU: `100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)`
     - Memory: `100 * (1 - ((node_memory_MemAvailable_bytes) / (node_memory_MemTotal_bytes)))`
     - Disk: `100 - ((node_filesystem_avail_bytes{mountpoint="/",fstype!="tmpfs"} / node_filesystem_size_bytes{mountpoint="/",fstype!="tmpfs"}) * 100)`

2. **Grafana API** (Alternative)
   - Use Grafana's HTTP API
   - Fetch pre-configured dashboard data
   - Less flexible but easier

3. **cAdvisor API** (For Container Metrics)
   - Direct container metrics
   - `http://cadvisor:8082/api/v1.3/containers/`

### 3.2 Create LLM Benchmarks Endpoint
**New File:** `backend/app/routers/benchmarks.py`

**Endpoint:** `GET /api/metrics/benchmarks`

**Functionality:**
- Query Ollama API for model information
- Run benchmark tests (optional) or fetch cached results
- Calculate performance metrics: tokens/sec, latency, memory usage
- Return benchmark data for all available models

**Response Format:**
```json
{
  "timestamp": "2025-01-27T10:30:00Z",
  "models": [
    {
      "name": "llama3.2:3b",
      "speed_tokens_per_sec": 42,
      "latency_ms": 45,
      "memory_gb": 8.5,
      "quality_score": 92,
      "last_tested": "2025-01-27T09:00:00Z"
    },
    {
      "name": "mistral:7b",
      "speed_tokens_per_sec": 58,
      "latency_ms": 32,
      "memory_gb": 7.2,
      "quality_score": 88,
      "last_tested": "2025-01-27T09:00:00Z"
    },
    {
      "name": "phi3.5:mini",
      "speed_tokens_per_sec": 75,
      "latency_ms": 25,
      "memory_gb": 4.8,
      "quality_score": 85,
      "last_tested": "2025-01-27T09:00:00Z"
    }
  ]
}
```

**Implementation:**
- Use existing `OllamaClient` service
- Query: `GET http://ollama:11434/api/tags` (list models)
- For each model, run a test prompt and measure:
  - Time to first token
  - Tokens per second
  - Memory usage (from system metrics)
- Cache results (update every 1 hour)

### 3.3 Configuration Updates
**File:** `backend/app/config.py`

**New Settings:**
```python
# Prometheus Settings
prometheus_url: str = Field(default="http://prometheus:9090")
prometheus_enabled: bool = Field(default=True)

# Metrics Cache Settings
metrics_cache_ttl: int = Field(default=60)  # seconds
benchmarks_cache_ttl: int = Field(default=3600)  # 1 hour
```

---

## 🎨 Phase 4: Frontend Integration

### 4.1 Update SystemMetricsCard Component
**File:** `frontend/components/sections/SystemMetricsCard.tsx`

**Changes:**
- Remove static import from `@/data/metrics`
- Add API call to fetch live metrics
- Add loading state
- Add error handling with fallback to cached data
- Auto-refresh every 30 seconds

**Implementation:**
```typescript
"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";

export function SystemMetricsCard() {
  const [metrics, setMetrics] = useState<SystemMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await api.getSystemMetrics();
        setMetrics(data);
        setError(null);
      } catch (err) {
        setError("Failed to load metrics");
        // Fallback to cached/static data
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  // ... rest of component
}
```

### 4.2 Update BenchmarksCard Component
**File:** `frontend/components/sections/BenchmarksCard.tsx`

**Changes:**
- Similar to SystemMetricsCard
- Fetch from `/api/metrics/benchmarks`
- Auto-refresh every hour (benchmarks change less frequently)

### 4.3 Update API Client
**File:** `frontend/lib/api.ts`

**New Methods:**
```typescript
interface SystemMetricsResponse {
  timestamp: string;
  metrics: {
    cpu: { usage_percent: number; ... };
    memory: { used_gb: number; ... };
    disk: { used_gb: number; ... };
    network: { rx_mbps: number; ... };
    uptime: { days: number; uptime_percent: number; ... };
  };
  trends: { cpu: string; memory: string; ... };
}

interface BenchmarksResponse {
  timestamp: string;
  models: Array<{
    name: string;
    speed_tokens_per_sec: number;
    latency_ms: number;
    memory_gb: number;
    quality_score: number;
  }>;
}

async getSystemMetrics(): Promise<SystemMetricsResponse> {
  const response = await fetch(`${this.baseUrl}/api/metrics/system`);
  if (!response.ok) throw new Error("Failed to get system metrics");
  return response.json();
}

async getBenchmarks(): Promise<BenchmarksResponse> {
  const response = await fetch(`${this.baseUrl}/api/metrics/benchmarks`);
  if (!response.ok) throw new Error("Failed to get benchmarks");
  return response.json();
}
```

### 4.4 Update Personal Data Components
**Files to Update:**
- `frontend/components/sections/Hero.tsx` - Use personal data
- `frontend/components/sections/AboutCard.tsx` - Use personal data
- `frontend/components/sections/Timeline.tsx` - Use timeline data
- `frontend/app/about/page.tsx` - Use personal data

**Implementation:**
- Import from `@/data/personal`
- Replace hardcoded values with data from personal.ts

---

## 📊 Phase 5: Data Population

### 5.1 Personal Data File
**File:** `frontend/data/personal.ts`

**Content to Include (Based on Homelab Journey):**
- **Name:** Ahmed Oublihi
- **Title:** DevOps & MLOps Engineer | LLM Deployment Specialist
- **Bio:** 
  - Software engineer specializing in DevOps, MLOps, and LLM deployment
  - Building local AI infrastructure and self-hosted systems
  - Passionate about learning by doing and understanding systems deeply
  - Running a production-grade homelab for experimentation and learning
- **Professional Goals:**
  - Specialize in DevOps, MLOps, and LLM deployment
  - Master local AI and on-premises systems
  - Prepare for future where local LLMs are standard
- **Homelab Journey:**
  - Built complete homelab infrastructure from scratch
  - Deployed monitoring stack (Prometheus, Grafana, cAdvisor)
  - Implemented CI/CD pipeline with GitHub Actions
  - Configured reverse proxy with SSL
  - Automated deployments with Watchtower
- **Skills (From Journey):**
  - Docker & Docker Compose
  - Linux system administration (Ubuntu Server)
  - Network configuration (Netplan, NetworkManager)
  - Security hardening (SSH, UFW, Fail2ban)
  - Monitoring (Prometheus, Grafana)
  - Reverse proxy (Nginx Proxy Manager)
  - SSL/TLS certificates
  - CI/CD (GitHub Actions, GHCR)
  - Local LLM deployment (Ollama)
  - RAG systems
  - Vector databases (ChromaDB)
- **Contact Information:** (To be confirmed with user)
- **Social Links:** (To be confirmed with user - GitHub, LinkedIn, etc.)

### 5.2 Projects Data
**File:** `frontend/data/projects.ts`

**Update with Real Projects (Based on Portfolio & Homelab Journey):**
- **AI-Powered Portfolio** (THIS PROJECT)
  - Description: Self-hosted portfolio website with AI assistant powered by local LLMs and RAG
  - Technologies: Next.js, FastAPI, Ollama, ChromaDB, Docker
  - Features: RAG system, document ingestion, streaming chat, admin dashboard
  - Deployment: Fully deployed on homelab with CI/CD
  - Live: https://portfolio.medevs.local (local network)
  - GitHub: (To be confirmed)
  
- **Homelab Infrastructure**
  - Description: Production-grade homelab with monitoring, CI/CD, and automated deployments
  - Technologies: Ubuntu Server, Docker, Prometheus, Grafana, Nginx Proxy Manager, Watchtower
  - Features: Complete monitoring stack, automated container updates, SSL certificates, reverse proxy
  - Status: Fully operational with 11+ days of documented journey
  
- **TalkTheDoc** (RAG system)
  - Description: Real-time RAG system for document chat with streaming responses
  - Technologies: RAG, LangChain, FastAPI, ChromaDB
  - Status: (Update with actual status)
  
- **Docspresso** (AI documentation)
  - Description: AI-powered documentation generator using local LLMs
  - Technologies: LLM, Python, Next.js, Ollama
  - Status: (Update with actual status)
  
- **AI Agent Playground**
  - Description: Interactive platform for testing document summarization and code explanation agents
  - Technologies: LangChain, React, FastAPI, WebSocket
  - Status: (Update with actual status)

### 5.3 Timeline Data
**File:** `frontend/data/timeline.ts`

**Update with Real Timeline (Based on Homelab Journey):**
- **2024-2025 (Current):**
  - **DevOps & MLOps Focus**
  - Building production-grade homelab infrastructure
  - Deploying local LLM systems and RAG architectures
  - Implementing CI/CD pipelines
  - Setting up monitoring and observability stacks
  
- **2024:**
  - **Homelab Journey Begins**
  - Day 1-3: Ubuntu Server installation, Docker setup, first containerized app
  - Day 4-7: Security hardening (SSH, firewall, Fail2ban)
  - Day 8: Complete monitoring stack (Prometheus, Grafana, cAdvisor)
  - Day 9: Wi-Fi migration and network configuration
  - Day 10: Full portfolio deployment with SSL
  - Day 11: CI/CD automation with GitHub Actions
  
- **2024:**
  - **AI/LLM Specialist**
  - Building local LLM infrastructure
  - Developing RAG systems
  - Working with Ollama, ChromaDB, vector embeddings
  
- **2023-2024:**
  - **Full Stack + DevOps**
  - Learning containerization and orchestration
  - Deploying scalable applications
  - Infrastructure automation

**Note:** Timeline should reflect the homelab journey progression. Education and earlier professional experience to be confirmed with user.

---

## 🔧 Phase 6: Implementation Details

### 6.1 Backend Dependencies
**File:** `backend/requirements.txt`

**Add:**
```
prometheus-client>=0.20.0  # For Prometheus queries
httpx>=0.27.0  # For async HTTP requests (if not already present)
```

### 6.2 Error Handling & Fallbacks
- If Prometheus is unavailable → return cached data or static fallback
- If Ollama is unavailable → return last known benchmarks
- Add retry logic with exponential backoff
- Log errors for debugging

### 6.3 Caching Strategy
- **System Metrics:** Cache for 60 seconds (update frequently)
- **Benchmarks:** Cache for 1 hour (update less frequently)
- Use in-memory cache (Python dict with TTL)
- Consider Redis for production (optional)

### 6.4 Security Considerations
- Metrics endpoints should be public (no auth needed for read-only data)
- Consider rate limiting to prevent abuse
- Sanitize all Prometheus/Ollama responses
- Validate data before returning to frontend

---

## 📝 Phase 7: Testing & Validation

### 7.1 Unit Tests
- Test Prometheus query parsing
- Test Ollama benchmark calculation
- Test data transformation functions

### 7.2 Integration Tests
- Test metrics endpoint with mock Prometheus
- Test benchmarks endpoint with mock Ollama
- Test frontend components with mock API responses

### 7.3 Manual Testing Checklist
- [ ] System metrics display correctly
- [ ] Benchmarks display correctly
- [ ] Auto-refresh works
- [ ] Fallback to cached data works
- [ ] Error states display properly
- [ ] Personal data displays correctly
- [ ] All links work
- [ ] Mobile responsive

---

## 🚀 Phase 8: Deployment

### 8.1 Environment Variables
**Backend `.env`:**
```env
# Prometheus Settings (if Prometheus is in same Docker network)
PROMETHEUS_URL=http://prometheus:9090
# OR if accessing from host network
# PROMETHEUS_URL=http://192.168.178.23:9090
PROMETHEUS_ENABLED=true
METRICS_CACHE_TTL=60
BENCHMARKS_CACHE_TTL=3600

# Ollama is already configured in existing .env
# OLLAMA_BASE_URL=http://ollama:11434
```

### 8.2 Docker Compose Updates
**File:** `docker-compose.yml` or `docker-compose.homelab.yml`

**Network Considerations:**
- **Current Setup:** Portfolio containers are likely on a separate Docker network
- **Prometheus Access:** 
  - Option 1: If Prometheus is in same network → use `http://prometheus:9090`
  - Option 2: If Prometheus is on host network → use `http://192.168.178.23:9090`
  - Option 3: Add Prometheus to portfolio network or use host network mode
- **Ollama:** Already configured and working (`http://ollama:11434`)
- **Note:** Based on homelab journey, monitoring stack runs separately. May need to configure network access or use host IP.

### 8.3 Deployment Steps
1. Update code with all changes
2. Build new Docker images
3. Deploy to homelab
4. Verify Prometheus connectivity
5. Verify Ollama connectivity
6. Test endpoints
7. Monitor for errors

---

## 📋 Implementation Checklist

### Backend
- [ ] Create `backend/app/routers/metrics.py`
- [ ] Create `backend/app/routers/benchmarks.py`
- [ ] Add Prometheus client dependency (`prometheus-client` or `httpx` for REST API)
- [ ] Update `backend/app/config.py` with new settings
- [ ] Add caching logic (in-memory with TTL)
- [ ] Add error handling and fallbacks
- [ ] **Verify Prometheus network access** (same Docker network or host IP)
- [ ] Test endpoints locally
- [ ] Test with real Prometheus connection
- [ ] Update API documentation

### Frontend
- [ ] Create `frontend/data/personal.ts`
- [ ] Update `frontend/data/projects.ts` with real data
- [ ] Update `frontend/data/timeline.ts` with real data
- [ ] Update `frontend/data/skills.tsx` with verified levels
- [ ] Update `frontend/lib/api.ts` with new methods
- [ ] Update `SystemMetricsCard.tsx` to fetch live data
- [ ] Update `BenchmarksCard.tsx` to fetch live data
- [ ] Update `Hero.tsx` with personal data
- [ ] Update `AboutCard.tsx` with personal data
- [ ] Update `Timeline.tsx` with real timeline
- [ ] Add loading states
- [ ] Add error handling
- [ ] Test all components

### Data Population
- [x] Extract accurate information from homelab journey document
- [ ] Populate `personal.ts` with verified data (name, goals, skills from journey)
- [ ] Update projects with real status and links
- [ ] Update timeline with homelab journey milestones (Day 1-11)
- [ ] Add homelab infrastructure details
- [ ] Confirm social links (GitHub, LinkedIn) with user
- [ ] Add contact information (if user wants to include)

### Testing & Deployment
- [ ] Test locally with mock data
- [ ] **Verify Prometheus network connectivity** (check if same Docker network or need host IP)
- [ ] Test with real Prometheus connection (use working PromQL queries from Grafana)
- [ ] Test with real Ollama connection (already working)
- [ ] **Note:** Portfolio is already deployed and working on homelab
- [ ] Deploy updated code (will auto-deploy via Watchtower if CI/CD is set up)
- [ ] Verify all metrics display correctly
- [ ] Test auto-refresh functionality
- [ ] Monitor for 24 hours
- [ ] Fix any issues

---

## 🎯 Success Criteria

1. ✅ All personal data is accurate and reflects actual homelab journey
2. ✅ System metrics display real-time data from Prometheus/Grafana
3. ✅ LLM benchmarks display real data from Ollama
4. ✅ Data is stored in separate, maintainable files
5. ✅ Auto-refresh works correctly (30s for metrics, 1h for benchmarks)
6. ✅ Fallback mechanisms work when services are unavailable
7. ✅ All components are responsive and error-free
8. ✅ Portfolio continues to work on homelab (already deployed)
9. ✅ Metrics integration doesn't break existing functionality
10. ✅ Homelab journey is accurately represented in timeline/projects

---

## 📅 Estimated Timeline

- **Phase 1 (Research):** ✅ Complete
- **Phase 2 (Data Structure):** 1-2 hours
- **Phase 3 (Backend API):** 4-6 hours
- **Phase 4 (Frontend Integration):** 3-4 hours
- **Phase 5 (Data Population):** 2-3 hours
- **Phase 6 (Implementation Details):** 2-3 hours
- **Phase 7 (Testing):** 2-3 hours
- **Phase 8 (Deployment):** 1-2 hours

**Total Estimated Time:** 15-23 hours

---

## 🔄 Next Steps

1. **Review this updated plan** based on your actual homelab journey
2. **Confirm/Clarify:**
   - **Prometheus Network Access:** Is Prometheus accessible from portfolio backend container?
     - Same Docker network? → Use `http://prometheus:9090`
     - Separate network? → Use `http://192.168.178.23:9090` (host IP)
   - **Social Links:** GitHub, LinkedIn, Twitter, etc. (if you want to include)
   - **Contact Information:** Email, etc. (if you want to include)
   - **Education/Background:** Any additional professional/educational background to include?
   - **Projects:** Confirm status of TalkTheDoc, Docspresso, AI Agent Playground
3. **Approve plan** to begin implementation

---

## 📝 Important Notes

- **This portfolio IS your actual website** - no separate medevs.xyz
- **Deployment is already complete** - portfolio is running on homelab
- **CI/CD is set up** - changes will auto-deploy via Watchtower
- **Monitoring stack is operational** - Prometheus/Grafana queries are tested and working
- **Focus is on accuracy** - all data should reflect your actual homelab journey

---

**Document Version:** 2.0  
**Last Updated:** 2025-01-27  
**Status:** Updated with Accurate Homelab Journey Data - Awaiting Approval

