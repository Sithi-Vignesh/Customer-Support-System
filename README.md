# ABC Technologies - AI-Powered Customer Support System

An intelligent customer support automation system built with LangGraph, featuring multi-agent routing, RAG pipeline, SQLite memory, and human-in-the-loop approval for high-risk requests.

## Architecture

The system uses a LangGraph state machine with the following flow:

```
Customer Query → Intent Classification → RAG Retrieval → Specialized Agent → HITL Approval → Supervisor Validation → Final Response
```

### Agents
- **Sales Agent** — Handles pricing, plans, and product information
- **Technical Agent** — Handles errors, crashes, and configuration issues
- **Billing Agent** — Handles invoices, payments, and refund requests
- **Account Agent** — Handles password resets and account management

### Key Features
- **Intent Classification** — LLM-based query categorization into 5 categories (Sales, Technical, Billing, Account, Memory)
- **RAG Pipeline** — ChromaDB + SentenceTransformers retrieval from 4 company knowledge base documents
- **SQLite Memory** — Persistent conversation history per customer
- **Human-in-the-Loop** — Manual approval required for refunds, cancellations, account closures, compensation, and escalations
- **Supervisor Agent** — Validates and improves all agent responses before delivery

## Project Structure

```
customer_support/
├── agents/
│   ├── sales_agent.py
│   ├── technical_agent.py
│   ├── billing_agent.py
│   └── account_agent.py
├── docs/
│   ├── company_policy.txt
│   ├── pricing_guide.txt
│   ├── technical_manual.txt
│   └── faq.txt
├── graph/
│   ├── state.py
│   ├── nodes.py
│   └── router.py
├── hitl/
│   └── approval.py
├── memory/
│   └── memory_manager.py
├── rag/
│   └── retriever.py
├── main.py
└── requirements.txt
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Groq API Key

### Installation

1. Clone the repository
```bash
git clone https://github.com/Sithi-Vignesh/Customer-Support-System
cd Customer-Support-System
```

2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file in root directory
```
GROQ_API_KEY=your_groq_api_key_here
```

5. Run the system
```bash
python main.py
```

## Demo Queries

The system demonstrates 5 sample queries on startup:

| # | Query | Route | Notes |
|---|-------|-------|-------|
| 1 | What are the pricing plans available? | Sales | RAG retrieves pricing guide |
| 2 | I forgot my account password | Account | RAG retrieves FAQ |
| 3 | My application crashes when uploading a file | Technical | RAG retrieves technical manual |
| 4 | I need a refund for my annual subscription | Billing | Triggers HITL approval |
| 5 | What was my previous support issue? | Memory | SQLite recall, no routing |

## Human-in-the-Loop

The following request types require manual supervisor approval before a response is sent:

- Refund requests
- Subscription cancellation
- Account closure
- Compensation requests
- Escalation to management

When triggered, the system pauses and prompts the human supervisor to approve or reject via terminal input.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Graph Framework | LangGraph |
| LLM | Groq (LLaMA 3.3 70B) |
| RAG | ChromaDB + SentenceTransformers |
| Memory | SQLite |
| LLM Orchestration | LangChain |
| Environment | python-dotenv |

## SQLite Memory Schema

```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL,
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |