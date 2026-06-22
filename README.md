# Airport Support Agent

Airport handles millions of passengers yearly. Ground staff and customer service teams field the same questions repeatedly — baggage rules, lounge access, transit hotel availability, terminal connections. This project builds a retrieval-augmented agent that answers those questions automatically, grounded strictly in official CAG content.

The Hotels component goes a step further: instead of just retrieving information, the agent can search availability, compare options, and simulate a booking — demonstrating an agentic pattern with structured Tool Use.

---

## Architecture

```
User Query
    ↓
Query Expansion: LLM rewrites the query into multiple variants to improve retrieval coverage
    ↓
Hybrid Retrieval: BM25 (keyword) + Embedding (semantic) search run in parallel and results are merged
    ↓
Reranking: Cross-encoder rescores candidates jointly against the query, filters low-confidence results
    ↓
Intent Routing: LLM determines whether to answer from retrieved context, invoke a tool, or both
    ↓                              ↓
RAG Response                 Hotel Tool Use
Facilities & Services        search_hotels()
Baggage, Lounges,            compare_hotels()
Amenities, Health            book_room()
    ↓                              ↓
                 Final Response
```

---

## Tech Stack

| Layer | Tools |
|---|---|
| Scraping | requests, BeautifulSoup |
| Embedding | sentence-transformers |
| Keyword Search | rank_bm25 |
| Vector Store | FAISS |
| Reranker | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| LLM | Claude via Anthropic API |
| API | FastAPI |
| Containerization | Docker, docker-compose |

---

## Project Structure

```
airport-support-agent/
├── data/
│   ├── raw/               # Scraped HTML/JSON from official website
│   └── processed/         # Cleaned text ready for chunking
├── src/
│   ├── ingestion/         # Scraping and cleaning scripts
│   ├── chunking/          # Semantic chunking with overlap
│   ├── retrieval/         # BM25, embeddings, hybrid merge, reranker
│   ├── pipeline/          # End-to-end query pipeline
│   └── tools/             # Hotel tool implementations (mock endpoints)
├── api/
│   ├── main.py            # FastAPI entry point
│   └── routes/            # /chat and /hotels endpoints
├── evaluation/
│   ├── test_cases.json    # Query and ground truth answer pairs
│   └── metrics.py         # MRR, nDCG, LLM-as-Judge scoring
├── configs/
│   └── config.yaml        # Chunk size, top-k, model names
├── notebooks/             # Exploratory work and pipeline traces
├── .env.example           # Environment variable template
├── docker-compose.yml
└── requirements.txt

```

---

## Getting Started

```bash
# Clone
git clone https://github.com/MiZhyn/airport-support-agent.git
cd airport-support-agent

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Open .env and add your ANTHROPIC_API_KEY

# Scrape and build the knowledge base
python src/ingestion/scraper.py

# Start the API
uvicorn api.main:app --reload
```

To run the full stack with Docker:

```bash
docker-compose up
```

---

## Evaluation

Ground truth question-answer pairs are generated across both knowledge domains. Three metrics are reported:

- **MRR** — measures whether the correct document appears near the top of retrieved results
- **nDCG** — measures the overall quality of the ranking, not just the top result
- **LLM-as-Judge** — Claude compares the agent's response against the ground truth answer and returns a score with reasoning

Results are logged per query so failure cases can be inspected directly.

---

## Knowledge Base

All content is sourced from the official Changi Airport website:

- **Facilities & Services** — Baggage, Lounges, Amenities, Health & Wellness, Digital Services
- **Hotels** — Crowne Plaza Changi Airport, Transit Hotels, YOTEL AIR Singapore
