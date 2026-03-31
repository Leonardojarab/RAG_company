![RAG Company Banner](image/rag_company.png)

A production-ready RAG (Retrieval-Augmented Generation) system that lets you chat with your company's knowledge base using natural language. Built with LangChain, ChromaDB, and Gradio.

---

## What it does

- **Chat interface** — ask questions about your company's documents and get accurate, context-aware answers
- **Source transparency** — every answer shows the retrieved document chunks used to generate it
- **Evaluation dashboard** — measure retrieval quality (MRR, nDCG) and answer quality (accuracy, completeness, relevance) using an LLM-as-a-judge

---

## Architecture

```
knowledge-base/          # Source documents (.md files)
├── company/
├── contracts/
├── employees/
└── products/

implementation/
├── ingest.py            # Loads documents → chunks → vector store
└── answer.py            # Retrieves context + calls LLM

evaluation/
├── eval.py              # Retrieval & answer quality metrics
├── test.py              # Test question loader
└── tests.jsonl          # Test dataset

app.py                   # Chat UI (Gradio)
evaluator.py             # Evaluation dashboard (Gradio)
```

**Flow:**
```
User question → Embedding → ChromaDB retrieval → LLM (GPT-4.1-nano) → Answer + Sources
```

---

## Quickstart

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-key-here
```

### 3. Build the vector database

```bash
uv run python -m implementation.ingest
```

### 4. Launch the chat app

```bash
uv run python app.py
```

### 5. (Optional) Launch the evaluation dashboard

```bash
uv run python evaluator.py
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | GPT-4.1-nano (OpenAI) |
| Embeddings | all-MiniLM-L6-v2 (HuggingFace) |
| Vector Store | ChromaDB |
| RAG Framework | LangChain |
| UI | Gradio 6 |
| Evaluation | litellm + LLM-as-a-judge |
| Package Manager | uv |

---

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| MRR | Mean Reciprocal Rank — how high relevant docs rank |
| nDCG | Normalized Discounted Cumulative Gain |
| Coverage | % of expected keywords found in retrieved docs |
| Accuracy | Factual correctness vs reference answer (1–5) |
| Completeness | Coverage of all answer aspects (1–5) |
| Relevance | How directly the answer addresses the question (1–5) |

---

## CI/CD with GitHub Actions

Two automated workflows run on every push:

### CI — Syntax Check
Runs on **every push** to `main`. Verifies that all `.py` files have no syntax errors.
- ✅ Green = code is valid
- ❌ Red = syntax error found, with exact file and line number

### Retrieval Evaluation
Runs automatically when you change `answer.py`, `ingest.py`, `knowledge-base/` or `evaluation/`. Rebuilds the vector database and measures retrieval quality across 150 test questions.

**How to use it:** change a parameter (e.g. `RETRIEVAL_K` in `answer.py`), push, and GitHub tells you if retrieval improved.

**Current benchmark results (RETRIEVAL_K=15):**

| Metric | Value | Status |
|--------|-------|--------|
| Avg MRR | 0.7624 | Acceptable |
| Avg nDCG | 0.7670 | Acceptable |
| Coverage | 93.5% | Good ✅ |

Results are saved as a downloadable artifact (`evaluation/results.json`) in the Actions tab for every run, enabling historical comparison across experiments.

---

## Adding your own knowledge base

1. Place `.md` files inside `knowledge-base/` organized by category (subfolder = `doc_type` metadata)
2. Rebuild the vector store: `uv run python -m implementation.ingest`
3. Run the app: `uv run python app.py`
