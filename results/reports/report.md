# RAG vs GraphRAG vs Vectorless: Enterprise Vertical Performance Analysis

Comparing four retrieval strategies — **Vector (Pinecone)**, **Vectorless/BM25**, **Hybrid (RRF fusion)**, and **Graph RAG (Neo4j)** — across four enterprise verticals (finance, marketing, product, service), using Groq (gpt-oss) for generation and LLM-as-judge scoring, and `nomic-embed-text-v1` for dense embeddings.

## Summary: Best Approach per Vertical

| Vertical | Best Approach (by judge score) | Judge Score | Hit Rate |
|---|---|---|---|
| Finance | Hybrid (BM25 + Vector, RRF) | 4.90 | 100.0% |
| Marketing | Vector RAG (Pinecone) | 4.20 | 60.0% |
| Product | Vector RAG (Pinecone) | 2.45 | 40.0% |
| Service | Hybrid (BM25 + Vector, RRF) | 4.25 | 10.0% |

## Finance

| Approach | Retrieval Hit Rate | Avg Judge Score (1-5) | Avg Retrieval Latency (s) | Avg Generation Latency (s) |
|---|---|---|---|---|
| Hybrid (BM25 + Vector, RRF) | 100.0% | 4.90 | 1.353 | 2.620 |
| Vectorless / BM25 | 100.0% | 4.85 | 0.005 | 4.486 |
| Vector RAG (Pinecone) | 100.0% | 4.80 | 1.455 | 2.521 |
| Graph RAG (Neo4j) | 70.0% | 4.10 | 1.677 | 3.350 |

## Marketing

| Approach | Retrieval Hit Rate | Avg Judge Score (1-5) | Avg Retrieval Latency (s) | Avg Generation Latency (s) |
|---|---|---|---|---|
| Vector RAG (Pinecone) | 60.0% | 4.20 | 2.028 | 6.854 |
| Vectorless / BM25 | 30.0% | 3.90 | 0.005 | 7.701 |
| Hybrid (BM25 + Vector, RRF) | 25.0% | 1.95 | 2.441 | 3.972 |
| Graph RAG (Neo4j) | 35.0% | 1.80 | 2.978 | 3.905 |

## Product

| Approach | Retrieval Hit Rate | Avg Judge Score (1-5) | Avg Retrieval Latency (s) | Avg Generation Latency (s) |
|---|---|---|---|---|
| Vector RAG (Pinecone) | 40.0% | 2.45 | 6.582 | 1.171 |
| Hybrid (BM25 + Vector, RRF) | 40.0% | 2.25 | 0.853 | 2.382 |
| Graph RAG (Neo4j) | 35.0% | 2.25 | 2.365 | 3.429 |
| Vectorless / BM25 | 20.0% | 1.80 | 0.027 | 3.192 |

## Service

| Approach | Retrieval Hit Rate | Avg Judge Score (1-5) | Avg Retrieval Latency (s) | Avg Generation Latency (s) |
|---|---|---|---|---|
| Hybrid (BM25 + Vector, RRF) | 10.0% | 4.25 | 1.219 | 3.616 |
| Graph RAG (Neo4j) | 10.0% | 3.70 | 3.244 | 3.529 |
| Vector RAG (Pinecone) | 15.0% | 3.65 | 1.094 | 3.076 |
| Vectorless / BM25 | 10.0% | 3.55 | 0.003 | 4.694 |

## Decision Framework

- **Vector RAG**: best for free-text, semantically fuzzy queries where exact keyword overlap with the source is unlikely (paraphrased questions).
- **Vectorless / BM25**: best for terminology-heavy, exact-match-sensitive queries (ticket IDs, product SKUs, ticker symbols) and where infra simplicity/cost matters.
- **Hybrid**: generally the safest default — recovers cases either single method misses, at the cost of running both pipelines.
- **Graph RAG**: best where the enterprise data has real entity relationships to traverse (company↔filing, customer↔ticket↔product); highest ingestion cost (LLM entity extraction per document) and depends heavily on extraction quality.
