# 🌍 ReliefLink AI
### Real-Time Crisis Awareness & Trusted Donation Platform

> An AI-powered, full-stack humanitarian platform built with **FastAPI**, **Streamlit**, **LangGraph**, **LangChain RAG**, **FAISS**, and **OpenAI GPT**.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│   FRONTEND  —  Streamlit UI                                 │
│   Crisis Feed • Donor Hub • Physical Aid • Help Center      │
│   Crisis Blog • AI Chat Assistant (sidebar)                 │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP (REST)
┌────────────────────▼────────────────────────────────────────┐
│   BACKEND  —  FastAPI  (port 8000)                          │
│   /api/crisis  •  /api/rag  •  /api/help  •  /api/chat     │
└──────┬─────────────┬───────────────────────────────────────┘
       │ LangGraph   │ RAG Chain (LCEL)
┌──────▼──────┐  ┌───▼───────────────────────────────────────┐
│  LangGraph  │  │  LangChain + FAISS + OpenAI Embeddings    │
│  Workflow   │  │  Retrieve → Augment → Generate            │
│  6 nodes    │  └───────────────────────────────────────────┘
└──────┬──────┘
       │ GPT-3.5-turbo / Embeddings
┌──────▼──────────────────────────────────────────────────────┐
│   OpenAI API  +  NewsAPI  +  LangSmith (observability)     │
└─────────────────────────────────────────────────────────────┘
```

## 🧠 LangGraph Workflow (6 Nodes)

```
fetch_news → analyze → classify_urgency → extract_needs → embed_store → generate_output → END
```

| Node | Purpose |
|------|---------|
| `fetch_news` | NewsAPI real-time headlines (fallback: rich sample data) |
| `analyze` | GPT extracts crisis type, region, needs, summary as JSON |
| `classify_urgency` | Normalises urgency (High/Medium/Low) + colour coding |
| `extract_needs` | Maps needs to controlled vocabulary taxonomy |
| `embed_store` | OpenAI embeddings → FAISS vector store |
| `generate_output` | Formats final feed, persists to in-memory cache |

---

## 📁 Project Structure

```
ReliefAI/
├── backend/
│   ├── config.py                  # Env var loading
│   ├── main.py                    # FastAPI app + CORS
│   ├── data/
│   │   ├── sample_data.py         # 8 crises, donation orgs, help requests
│   │   └── faiss_store.py         # FAISS vector store wrapper
│   ├── workflow/
│   │   ├── langgraph_pipeline.py  # 6-node LangGraph workflow
│   │   └── rag_pipeline.py        # LCEL RAG chain + blog + trust score
│   └── routes/
│       ├── crisis.py              # /api/crisis endpoints
│       ├── rag.py                 # /api/rag endpoints
│       ├── help.py                # /api/help endpoints
│       └── chat.py                # /api/chat endpoints
├── frontend/
│   └── app.py                     # Streamlit UI (5 pages + AI chat)
├── .streamlit/config.toml         # Dark theme config
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & Setup Environment

```bash
cd d:\ReliefAI
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
copy .env.example .env
# Edit .env and add your keys:
#   OPENAI_API_KEY=sk-...          ← Required
#   NEWS_API_KEY=...               ← Optional (get free at newsapi.org)
#   LANGCHAIN_API_KEY=...          ← Optional (LangSmith tracing)
```

### 3. Start the Backend

```bash
# In terminal 1 (from ReliefAI directory)
uvicorn backend.main:app --reload --port 8000
```

Visit http://localhost:8000/docs for interactive API docs.

### 4. Start the Frontend

```bash
# In terminal 2 (from ReliefAI directory)
streamlit run frontend/app.py
```

Visit http://localhost:8501 to use the app.

---

## 🖥️ UI Pages

| Page | Description |
|------|-------------|
| 🌐 **Crisis Feed** | Live carousel of AI-analyzed crisis reports with urgency badges and needs chips. Click "Refresh" to trigger the full LangGraph pipeline. |
| 💰 **Donor Hub** | Select a region → get AI analysis (RAG-grounded) + verified donation orgs with direct links + urgent needs breakdown |
| 🏥 **Physical Aid** | Find physical donation collection centres by country, with accepted items guide |
| 🆘 **Help Center** | Submit a help request (AI trust scoring) + browse the public help feed |
| 📰 **Crisis Blog** | Generate a full RAG-grounded awareness blog post for any crisis region |
| 🤖 **AI Chat** | Always-on sidebar chat assistant, context-aware and backed by FAISS RAG |

---

## ⚙️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/crisis/process` | Run full LangGraph pipeline |
| `GET`  | `/api/crisis/feed` | Get current crisis feed |
| `GET`  | `/api/crisis/regions` | List available regions |
| `POST` | `/api/rag/query` | RAG query against FAISS |
| `POST` | `/api/rag/analyze` | Region analysis for donors |
| `POST` | `/api/rag/blog` | Generate awareness blog |
| `POST` | `/api/help/submit` | Submit help request |
| `GET`  | `/api/help/feed` | Get public help feed |
| `POST` | `/api/chat/message` | AI chat message |
| `GET`  | `/health` | Health check + FAISS status |
| `GET`  | `/docs` | Interactive Swagger docs |

---

## 🔑 API Keys

| Key | Required | Purpose | Get It |
|-----|----------|---------|--------|
| `OPENAI_API_KEY` | ✅ Yes | GPT analysis, embeddings, RAG | [platform.openai.com](https://platform.openai.com) |
| `NEWS_API_KEY` | ⬜ Optional | Real-time headlines | [newsapi.org](https://newsapi.org/register) (free tier) |
| `LANGCHAIN_API_KEY` | ⬜ Optional | LangSmith tracing | [smith.langchain.com](https://smith.langchain.com) (free) |

> **Without `OPENAI_API_KEY`**: App runs with rich pre-loaded sample data. AI features return informative fallback messages.
>
> **Without `NEWS_API_KEY`**: Uses 8 built-in crisis scenarios (still fully demonstrates the workflow).

---

## 🧪 Testing Without API Keys

The app works **fully without any API keys** using built-in sample data:
- 8 crisis scenarios across Sudan, Gaza, Ukraine, Haiti, Yemen, Somalia, Ethiopia, Syria
- 5 realistic help requests with trust scores
- Donation organizations for every region
- Physical collection centres in 7 countries

---

## 📊 Trust Scoring System

Help requests are scored using a transparent rule-based system:

| Signal | Points |
|--------|--------|
| Supporting documents uploaded | +30 |
| Contact email provided | +12 |
| Donation link provided | +8 |
| Bank details provided | +5 |
| Detailed description (>300 chars) | +5 |
| Base score | 40 |

| Score | Level | Badge |
|-------|-------|-------|
| 80–100 | High | ✅ AI Verified |
| 60–79 | Medium | ⚠️ Partially Verified |
| 0–59 | Low | 🔍 Under Review |

---

## ⚠️ Disclaimers

- This platform does **not** process real payments
- Verification is **simulated** for demonstration purposes
- For real emergencies, always contact emergency services (911 / 999 / 112)
- AI-generated content may contain inaccuracies — always verify with official sources

---

*Built with ❤️ for humanitarian awareness. ReliefLink AI — connecting compassion with action.*
