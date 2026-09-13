# Query Agent

A backend project that answers questions using your own data (RAG), and has a separate user registration + email verification system. Built with FastAPI, PostgreSQL, LangChain, and Groq.

---

## 1. What It Does

You give it a question → it finds the most relevant piece of stored text → gives that text to an LLM → LLM answers based on that text (not just its own memory).

Separately, it also handles: signing up a new user, verifying them by email code, and basic account management (get/update/delete).

---

## 2. Architecture — How It Actually Works

### High-level flow (RAG)

```
User Question
     |
     v
FastAPI (/ask endpoint)
     |
     v
Convert question → embedding (sentence-transformers)
     |
     v
Search PostgreSQL (pgvector) for closest matching stored text
     |
     v
Retrieved context + original question
     |
     v
Sent to Groq LLM (via LangChain)
     |
     v
LLM generates answer grounded in that context
     |
     v
Answer returned to user
```

### High-level flow (User system)

```
POST /api/users/register
     |
     v
Check email doesn't already exist
     |
     v
Hash password (bcrypt) + generate 8-char code
     |
     v
Save user (isactive = False) + email the code (SMTP)

POST /api/users/verify
     |
     v
Match submitted code to stored code
     |
     v
isactive = True
```

### Component breakdown

| Component | File(s) | Job |
|---|---|---|
| API layer | `app/main.py`, `app/routers/users.py` | Defines endpoints, routes requests |
| Embeddings | `app/embeddings.py` | Turns text into vectors (local model, no API cost) |
| Vector storage | `app/database/models.py` (`Document` table), PostgreSQL + pgvector | Stores text + its vector, enables similarity search |
| Retrieval | `app/retrieve.py` | Runs the similarity search query |
| LLM chain | `app/rag_chain.py` | Combines retrieved context + question, sends to Groq, returns answer |
| Ingestion | `app/ingest.py`, `app/ingest_web.py` | Loads data (sample text / website) into the vector store |
| User auth | `app/database/models.py` (`User` table), `app/utils/security.py`, `app/utils/email_utils.py` | Password hashing, verification codes, email sending |
| DB connection | `app/database/connection.py` | SQLAlchemy engine/session setup |

### Why Postgres + pgvector (instead of a separate vector database)

One database does both jobs — normal relational data (users) and vector search (documents) — so there's no need to run/manage a second database system just for embeddings.

---

## 3. What Problem This Solves

Plain LLMs only know what they were trained on and can confidently make things up. This project grounds answers in real stored data instead, so the LLM is answering from actual retrieved text, not guessing.

The user system solves the standard "is this a real person with a real email" problem most apps need before trusting an account.

---

## 4. Is It a Real-World Solution Yet?

The architecture matches what real products use (internal knowledge-base bots, support assistants). But right now:
- `/ask` isn't locked behind login — the two modules aren't connected yet.
- The knowledge base has only test data in it, not a real, maintained dataset.

So: **the pattern is real, the build is a working prototype, not a finished product.**

---

## 5. Known Flaws

- No auth check on `/ask` — anyone can call it.
- Verification codes never expire.
- No rate limiting on register/ask endpoints.
- Re-running ingestion creates duplicate rows (no de-duplication).
- No stored source/citation info for retrieved chunks.
- No automated tests, no deployment config (Docker etc.).

---

## 6. MVP Status

Not quite an MVP yet. The hard technical parts (vector search, LLM grounding, working auth flow) are done and tested. What's missing before it's a real MVP:
- Connect the two modules (require login to use `/ask`)
- Code expiry + resend-code option
- A real, ongoing knowledge base instead of test sentences
- Basic rate limiting

---

## 7. Tech Stack

FastAPI · PostgreSQL 18 · pgvector · SQLAlchemy · sentence-transformers · LangChain · Groq API · bcrypt · SMTP