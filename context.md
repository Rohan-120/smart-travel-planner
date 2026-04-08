# Smart Travel Planning Assistant

This file is the project source of truth. It summarizes the current architecture, database design, storage layout, and implementation status so any teammate can quickly understand what is already built and what is still pending.

---

## 1. Project Overview

The Smart Travel Planning Assistant is an agentic AI travel-planning system that helps users:

- plan trips through a conversational interface
- compare destinations and travel options
- receive personalized itineraries
- use saved preferences and travel history for better recommendations

The intended design uses a Retrieval-Augmented Generation (RAG) pipeline backed by FAISS. The assistant should retrieve relevant destination, hotel, and itinerary information from local travel documents and combine that with tool-based planning logic.

The long-term goal is a LangChain-driven agent that decides whether to:

- answer from retrieved travel knowledge
- generate an itinerary
- compare destinations
- optimize for budget
- call external travel data sources when needed

---

## 2. Technical Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Agent Orchestration | LangChain Agent |
| LLM | OpenAI via `langchain-openai` |
| Vector Store | FAISS (`faiss-cpu`) |
| Relational Database | PostgreSQL (`smart_travel_planner`) |
| Observability | LangSmith |
| ORM | SQLAlchemy |
| Text Splitting | `langchain-text-splitters` + `tiktoken` |

Database host currently documented for the team:

- Host: `172.25.84.112:5432`
- Database: `smart_travel_planner`

---

## 3. Current Repository Structure

```text
smart_travel_planner/
|-- backend/
|   |-- agents/
|   |   `-- tools/
|   |       |-- travel_retrieval.py
|   |       |-- itinerary_generator.py
|   |       |-- external_travel.py
|   |       |-- comparison.py
|   |       `-- budget_optimizer.py
|   |-- app/
|   |   `-- routers/
|   |       `-- documents.py
|   |-- auth/
|   |   `-- auth.py
|   |-- services/
|   |   `-- document_service.py
|   |-- database.py
|   |-- models.py
|   `-- main.py
|-- frontend/
|   `-- app.py
|-- storage/
|   |-- travel_docs/
|   |   |-- guides/
|   |   |-- hotels/
|   |   `-- itineraries/
|   `-- policies/
|       |-- admin/
|       |-- travel_agent/
|       `-- user/
|-- tests/
|-- .env.example
|-- requirements.txt
`-- context.md
```

### Storage Notes

`storage/travel_docs/` now contains seeded local RAG documents:

- `guides/`: 5 destination guide PDFs
- `hotels/`: 5 hotel-focused PDFs
- `itineraries/`: 5 itinerary-focused PDFs

Current seeded destinations:

- Mumbai
- Manali
- Jaipur
- Goa
- Delhi

`storage/policies/` contains role-specific policy PDFs for:

- admin
- travel_agent
- user

These policy PDFs are documentation assets. They are not part of the travel RAG pipeline unless explicitly ingested later.

---

## 4. Database Architecture

The system uses PostgreSQL for relational data and FAISS for vector storage.

- PostgreSQL stores users, trips, conversations, document metadata, and access policies.
- FAISS is intended to store embedded travel-document chunks on disk.

### A. User and Auth Tables

#### `users`

Stores login identity and role.

| Column | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| name | String(100) | Required |
| email | String(150) | Unique, required |
| password_hash | Text | Hashed password |
| role | String(50) | `admin`, `travel_agent`, `user` |
| created_at | TIMESTAMP | Auto timestamp |

### B. Conversation and Memory Tables

#### `conversations`

Stores each user chat session.

| Column | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | FK -> `users.id` |
| title | String(200) | Session label |
| created_at | TIMESTAMP | Auto timestamp |

#### `messages`

Stores message pairs inside a conversation.

| Column | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| conversation_id | Integer | FK -> `conversations.id` |
| user_query | Text | Required |
| agent_response | Text | Required |
| created_at | TIMESTAMP | Auto timestamp |

#### `user_memory`

Stores additional long-term memory records per user.

| Column | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | FK -> `users.id` |
| memory_type | String(100) | Memory classification |
| content | Text | Required |
| created_at | TIMESTAMP | Auto timestamp |

### C. Preference and Trip Tables

#### `user_preferences`

Stores long-term travel preferences for personalization.

| Column | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | FK -> `users.id`, unique |
| budget | Integer | Optional |
| travel_style | String(100) | Example: adventure, luxury, budget |
| preferred_location | String(150) | Favorite region or destination |
| hotel_type | String(100) | Example: hostel, resort, boutique |
| preferred_transport | String(100) | Example: flight, train, road |
| updated_at | TIMESTAMP | Auto timestamp |

#### `trips`

Stores trip records for each user.

| Column | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | FK -> `users.id` |
| origin | String(150) | Optional |
| destination | String(150) | Required |
| start_date | Date | Optional |
| end_date | Date | Optional |
| budget | Integer | Optional |
| created_at | TIMESTAMP | Auto timestamp |

#### `itineraries`

Stores day-by-day plan rows linked to a trip.

| Column | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| trip_id | Integer | FK -> `trips.id` |
| day | Integer | Day number |
| plan | Text | Day plan text |

### D. RAG and Document Tables

#### `documents`

Stores metadata for ingested files.

| Column | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| document_name | String(200) | Required |
| document_category | String(100) | Example: `guide`, `hotel`, `itinerary` |
| source_type | String(100) | Example: `pdf`, `web`, `manual` |
| uploaded_by | Integer | FK -> `users.id`, nullable |
| faiss_doc_key | String(100) | Unique FAISS linkage key |
| is_active | String(10) | `TRUE` or `FALSE` |
| created_at | TIMESTAMP | Auto timestamp |

#### `document_chunks`

Stores text chunks for vector retrieval.

| Column | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| document_id | Integer | FK -> `documents.id` |
| chunk | Text | Required |
| faiss_vector_id | Integer | FAISS vector position |
| metadata_json | JSON | Page or section metadata |

### E. Access Control Table

#### `role_access_policies`

Controls which roles can access which documents.

| Column | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| role_name | String(50) | `admin`, `travel_agent`, `user` |
| document_id | Integer | FK -> `documents.id` |
| access_type | String(50) | Example: `read`, `full` |
| created_at | TIMESTAMP | Auto timestamp |

---

## 5. Agent Tools Planned

The repo already contains tool files for the intended agent workflow:

| Tool File | Intended Responsibility | Current State |
|---|---|---|
| `travel_retrieval.py` | Retrieve travel info from FAISS | Stub |
| `itinerary_generator.py` | Generate day-by-day travel plans | Stub |
| `external_travel.py` | Real-time travel or pricing data | Stub |
| `comparison.py` | Compare destinations | Stub |
| `budget_optimizer.py` | Recommend options within budget | Stub |

Important note:

- Tool files exist, but the actual LangChain agent orchestration layer is not implemented yet.

---

## 6. Implementation Notes

- Travel PDFs belong under `storage/travel_docs/`.
- Destination-wide knowledge belongs in `guides/`.
- Accommodation-focused documents belong in `hotels/`.
- Day-by-day plans belong in `itineraries/`.
- PostgreSQL should store only metadata and chunks, not binary PDF content.
- FAISS should be the bridge between chunk embeddings and retrieval.
- Role-based retrieval should use `role_access_policies` before returning document context.
- Long-term personalization should come from `user_preferences`, `user_memory`, and `trips`.
- `.env.example` should be copied to `.env` locally and never committed with secrets.

Current implementation caveats:

- `document_service.py` is still a stub.
- `/documents/upload` is still a stub.
- auth endpoints are still stubs.
- frontend login and chat are scaffolded but not connected to backend APIs.
- only the documents router is currently mounted in the FastAPI app.
- tests are not implemented yet.

---

## 7. Environment Variables

```env
DATABASE_URL=postgresql://USERNAME:team123@172.25.84.112:5432/smart_travel_planner
OPENAI_API_KEY=your_openai_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=smart-travel-assistant
FAISS_INDEX_PATH=./storage/faiss_index
```

---

## 8. Current Status

| Status | Item |
|---|---|
| DONE | Database models are defined in `backend/models.py` |
| DONE | Database engine and table init scaffold exist in `backend/database.py` |
| DONE | FastAPI app entrypoint exists in `backend/main.py` |
| DONE | Documents router scaffold exists in `backend/app/routers/documents.py` |
| DONE | Requirements are defined in `requirements.txt` |
| DONE | Local RAG source PDFs have been added to `storage/travel_docs/guides` |
| DONE | Local hotel PDFs have been added to `storage/travel_docs/hotels` |
| DONE | Local itinerary PDFs have been added to `storage/travel_docs/itineraries` |
| DONE | Role-specific policy PDFs have been added to `storage/policies` |
| IN PROGRESS | Streamlit frontend scaffold exists, but backend integration is pending |
| IN PROGRESS | Auth module scaffold exists, but login/logout are not implemented |
| IN PROGRESS | Document ingestion and FAISS search are planned in code, but not implemented |
| UPCOMING | Agent executor and LangChain tool orchestration |
| UPCOMING | RAG retrieval pipeline with FAISS plus access filtering |
| UPCOMING | LangSmith tracing and observability wiring |
| UPCOMING | API endpoints for chat and planning |
| UPCOMING | Automated tests |

---

## 9. Recommended Next Steps

1. Implement `backend/services/document_service.py` for PDF reading, chunking, embedding, and FAISS persistence.
2. Complete `/documents/upload` so new PDFs can be registered in PostgreSQL and indexed.
3. Implement auth and mount the auth router in the FastAPI app.
4. Build an agent endpoint that can call retrieval and planning tools.
5. Connect the Streamlit UI to login and chat endpoints.
6. Add LangSmith tracing.
7. Add unit and integration tests.

---

## 10. Team Notes

- Keep all travel knowledge documents inside the correct subfolder under `storage/travel_docs/`.
- When adding new destinations, try to maintain the same three-category structure: `guides`, `hotels`, `itineraries`.
- When adding new tools, create a dedicated file under `backend/agents/tools/` and document the purpose clearly.
- If policy documents should ever become searchable by the assistant, create a policy ingestion path explicitly instead of mixing them into travel documents by default.
