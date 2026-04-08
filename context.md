# context.md — Smart Travel Planning Assistant

This file serves as the **source of truth** for the project team.  
It combines the current file structure with all finalized technical decisions and database architecture.  
Place this file at the project root so any team member (or AI assistant) can quickly understand the project state.

---

## 1. Project Overview

The **Smart Travel Planning Assistant** is an Agentic AI system that enables users to plan trips, compare travel options, and receive personalized itineraries through a conversational interface.

It uses a **RAG (Retrieval-Augmented Generation)** approach backed by FAISS to provide context-aware, role-based travel recommendations from internal travel guides, hotel data, and itinerary documents.

The system is agent-driven: the LangChain agent dynamically decides whether to retrieve from the knowledge base or invoke a specialized tool (itinerary generation, budget optimization, destination comparison, or real-time data fetch) based on the user's request.

---

## 2. Technical Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Agent Orchestration | LangChain Agent |
| LLM | OpenAI (via `langchain-openai`) |
| Vector Store | FAISS (`faiss-cpu`) |
| Relational Database | PostgreSQL (`smart_travel_planner` DB) |
| Observability | LangSmith |
| ORM | SQLAlchemy |
| Text Splitting | `langchain-text-splitters` + `tiktoken` |

**Database Host:** `172.25.84.112:5432`  
**Database Name:** `smart_travel_planner`  
**Default Password:** `team123`

---

## 3. File Structure

```
smart_travel_planner/
├── backend/                        # Application & Intelligence Layer
│   ├── agents/                     # LangChain Agent definition
│   │   └── tools/                  # One file per tool
│   │       ├── travel_retrieval.py     # RAG-based travel info fetch
│   │       ├── itinerary_generator.py  # Generate day-by-day plans
│   │       ├── external_travel.py      # Real-time travel API calls
│   │       ├── comparison.py           # Destination comparison logic
│   │       └── budget_optimizer.py     # Plans within budget constraint
│   ├── auth/                       # Authentication & RBAC logic
│   ├── app/
│   │   └── routers/
│   │       └── documents.py        # Document management endpoints
│   ├── services/                   # PDF processing & FAISS vector logic
│   ├── database.py                 # DB engine, session, Base
│   ├── models.py                   # SQLAlchemy ORM models
│   └── main.py                     # FastAPI entry point
├── frontend/                       # Streamlit UI
│   └── app.py                      # Chat interface + itinerary display
├── storage/                        # Local travel document storage
│   └── travel_docs/
│       ├── guides/                 # Destination travel guides
│       ├── hotels/                 # Hotel and accommodation data
│       └── itineraries/            # Sample itinerary documents
├── tests/                          # Unit & Integration tests
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (never commit)
└── context.md                      # Project documentation (this file)
```

---

## 4. Database Architecture

The system uses a **single PostgreSQL instance** (`smart_travel_planner`) with all tables in the default `public` schema.  
Vector data is handled by **FAISS** (stored on disk); PostgreSQL stores only chunk text and FAISS index references.

---

### A. User & Auth Tables

#### `users`
Stores credentials and roles. Roles control tool access and UI behavior.

| Column | Type | Notes |
|---|---|---|
| id | Integer | PK |
| name | String(100) | Required |
| email | String(150) | Unique, required |
| password_hash | Text | Hashed password |
| role | String(50) | `admin`, `travel_agent`, `user` |
| created_at | TIMESTAMP | Auto |

**Role Behavior:**
- `admin` — Full system access
- `travel_agent` — Full planning tools, detailed itinerary generation
- `user` — Simplified travel suggestions only

---

### B. Conversation & Memory Tables

#### `conversations`
Each chat session belongs to one user.

| Column | Type | Notes |
|---|---|---|
| id | Integer | PK |
| user_id | Integer | FK → users.id (CASCADE) |
| title | String(200) | Session label |
| created_at | TIMESTAMP | Auto |

#### `messages`
Each message pair (query + response) in a conversation.

| Column | Type | Notes |
|---|---|---|
| id | Integer | PK |
| conversation_id | Integer | FK → conversations.id (CASCADE) |
| user_query | Text | Required |
| agent_response | Text | Required |
| created_at | TIMESTAMP | Auto |

---

### C. Preference & Trip Tables (Long-Term Memory)

#### `user_preferences`
One-to-one with users. Persists travel preferences for personalization.

| Column | Type | Notes |
|---|---|---|
| id | Integer | PK |
| user_id | Integer | FK → users.id (CASCADE), Unique |
| budget | Integer | In user's currency |
| travel_style | String(100) | e.g., adventure, luxury, budget |
| preferred_location | String(150) | Favorite region/country |
| hotel_type | String(100) | e.g., hostel, resort, boutique |
| preferred_transport | String(100) | e.g., flight, train, road |
| updated_at | TIMESTAMP | Auto |

#### `trips`
Each planned trip for a user.

| Column | Type | Notes |
|---|---|---|
| id | Integer | PK |
| user_id | Integer | FK → users.id (CASCADE) |
| origin | String(150) | Departure location |
| destination | String(150) | Required |
| start_date | Date | Trip start |
| end_date | Date | Trip end |
| budget | Integer | Trip budget |
| created_at | TIMESTAMP | Auto |

#### `itineraries`
Day-by-day plans linked to a trip.

| Column | Type | Notes |
|---|---|---|
| id | Integer | PK |
| trip_id | Integer | FK → trips.id (CASCADE) |
| day | Integer | Day number (1, 2, 3...) |
| plan | Text | Full day plan as text |

---

### D. RAG / Document Tables

#### `documents`
Registry of all ingested travel documents. Source files live on the filesystem; DB stores metadata only.

| Column | Type | Notes |
|---|---|---|
| id | Integer | PK |
| document_name | String(200) | Required |
| document_category | String(100) | e.g., `guide`, `hotel`, `itinerary` |
| source_type | String(100) | e.g., `pdf`, `web`, `manual` |
| uploaded_by | Integer | FK → users.id (SET NULL) |
| faiss_doc_key | String(100) | Unique key linking to FAISS index |
| is_active | String(10) | `TRUE` / `FALSE` |
| created_at | TIMESTAMP | Auto |

#### `document_chunks`
Text fragments produced during document ingestion.

| Column | Type | Notes |
|---|---|---|
| id | Integer | PK |
| document_id | Integer | FK → documents.id (CASCADE) |
| chunk | Text | Raw chunk text, required |
| faiss_vector_id | Integer | Index position in FAISS store |
| metadata_json | JSON | Source page, section, etc. |

---

### E. Access Control Table

#### `role_access_policies`
Defines which roles can access which documents.

| Column | Type | Notes |
|---|---|---|
| id | Integer | PK |
| role_name | String(50) | `admin`, `travel_agent`, `user` |
| document_id | Integer | FK → documents.id (CASCADE) |
| access_type | String(50) | e.g., `read`, `full` |
| created_at | TIMESTAMP | Auto |

---

## 5. Agent Tools Summary

| # | Tool File | Responsibility |
|---|---|---|
| 1 | `travel_retrieval.py` | RAG retrieval from FAISS — fetches relevant travel info from documents |
| 2 | `itinerary_generator.py` | Generates day-by-day travel plans based on trip details |
| 3 | `external_travel.py` | Calls real-time external APIs for live pricing, weather, availability |
| 4 | `comparison.py` | Compares two or more destinations on key attributes |
| 5 | `budget_optimizer.py` | Recommends best travel options within a specified budget |

The LangChain agent decides at runtime which tool(s) to invoke or whether to answer from RAG context alone.

---

## 6. Implementation Notes

- **Source of Truth:** Travel documents (PDFs) are stored under `storage/travel_docs/`. The database only stores metadata and `faiss_doc_key` references — never binary file content.
- **FAISS Integration:** Each document chunk is embedded and stored in the FAISS index. The `faiss_vector_id` in `document_chunks` maps back to the FAISS index position for lookup.
- **Role-Based Retrieval:** Before any RAG query, the system checks `role_access_policies` to filter which `document_id`s the current user's role is allowed to retrieve.
- **Long-Term Memory:** `user_preferences` and `trips` tables persist across sessions to improve personalization over time.
- **ORM Init:** Run `database.py` directly (`python database.py`) to create all tables via `Base.metadata.create_all()`. All models must be imported before this call — they are imported at the bottom of `database.py` via `from models import *`.
- **Environment Variables:** Copy `.env.example` to `.env` and fill in your OpenAI API key and LangSmith credentials. Never commit `.env`.
- **New Tools:** When adding a new agent tool, create a new file in `backend/agents/tools/` and ensure agent actions are observable via LangSmith tracing.

---

## 7. Environment Variables (`.env`)

```env
DATABASE_URL=postgresql://USERNAME:team123@172.25.84.112:5432/smart_travel_planner
OPENAI_API_KEY=your_openai_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=smart-travel-assistant
FAISS_INDEX_PATH=./storage/faiss_index
```

---

## 8. Current Status & Next Steps

| Status | Item |
|---|---|
| DONE | Database models (`models.py`) |
| DONE | DB connection & table init (`database.py`) |
| DONE | FastAPI entry point (`main.py`) |
| DONE | Documents router scaffold (`app/routers/documents.py`) |
| DONE | Requirements defined (`requirements.txt`) |
| IN PROGRESS | Document ingestion service (PDF → chunks → FAISS) |
| IN PROGRESS | Auth endpoints (login, session management) |
| UPCOMING | LangChain agent + tool integration |
| UPCOMING | RAG retrieval pipeline (FAISS search → context injection) |
| UPCOMING | Streamlit chat UI |
| UPCOMING | LangSmith observability wiring |
| UPCOMING | Role-based access enforcement in retrieval |

---

## For Your Team

> **Team Lead Note:** Every member must update their `.env` with the shared PostgreSQL IP (`172.25.84.112`).  
> When adding new agent tools, create a new file in `backend/agents/tools/` and document the tool's behavior.  
> All RAG document ingestion must register entries in both `documents` and `document_chunks` tables and update the FAISS index on disk.  
> The `faiss_doc_key` in `documents` is the bridge between PostgreSQL metadata and the FAISS vector store — treat it as a required field.
