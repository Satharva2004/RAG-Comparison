"""Turn results/summary.json into a substack-style markdown report:
per-vertical comparison tables (accuracy/latency) + an overall decision
framework, mirroring the RAG vs GraphRAG performance-analysis format.
"""
import json

from src.common.config import RESULTS_DIR, VERTICALS

APPROACH_LABEL = {
    "vector": "Vector RAG (Pinecone)",
    "bm25": "Vectorless / BM25",
    "hybrid": "Hybrid (BM25 + Vector, RRF)",
    "graph": "Graph RAG (Neo4j)",
}


def load_summary():
    return json.loads((RESULTS_DIR / "summary.json").read_text(encoding="utf-8"))


def vertical_table(rows: list[dict]) -> str:
    header = "| Approach | Retrieval Hit Rate | Avg Judge Score (1-5) | Avg Retrieval Latency (s) | Avg Generation Latency (s) |\n"
    header += "|---|---|---|---|---|\n"
    lines = [header]
    for r in sorted(rows, key=lambda x: -x["avg_judge_score"]):
        lines.append(
            f"| {APPROACH_LABEL[r['approach']]} | {r['retrieval_hit_rate']:.1%} | "
            f"{r['avg_judge_score']:.2f} | {r['avg_retrieval_latency_s']:.3f} | "
            f"{r['avg_generation_latency_s']:.3f} |\n"
        )
    return "".join(lines)


def best_per_vertical(summary: list[dict]) -> str:
    lines = ["| Vertical | Best Approach (by judge score) | Judge Score | Hit Rate |\n", "|---|---|---|---|\n"]
    for v in VERTICALS:
        rows = [r for r in summary if r["vertical"] == v]
        best = max(rows, key=lambda x: x["avg_judge_score"])
        lines.append(
            f"| {v.capitalize()} | {APPROACH_LABEL[best['approach']]} | "
            f"{best['avg_judge_score']:.2f} | {best['retrieval_hit_rate']:.1%} |\n"
        )
    return "".join(lines)


def main():
    summary = load_summary()
    out = ["# RAG vs GraphRAG vs Vectorless: Enterprise Vertical Performance Analysis\n"]
    out.append(
        "\nComparing four retrieval strategies — **Vector (Pinecone)**, **Vectorless/BM25**, "
        "**Hybrid (RRF fusion)**, and **Graph RAG (Neo4j)** — across four enterprise verticals "
        "(finance, marketing, product, service), using Groq (gpt-oss) for generation and "
        "LLM-as-judge scoring, and `nomic-embed-text-v1` for dense embeddings.\n"
    )

    out.append("\n## Summary: Best Approach per Vertical\n\n")
    out.append(best_per_vertical(summary))

    for v in VERTICALS:
        rows = [r for r in summary if r["vertical"] == v]
        out.append(f"\n## {v.capitalize()}\n\n")
        out.append(vertical_table(rows))

    out.append(
        "\n## Decision Framework\n\n"
        "- **Vector RAG**: best for free-text, semantically fuzzy queries where exact keyword "
        "overlap with the source is unlikely (paraphrased questions).\n"
        "- **Vectorless / BM25**: best for terminology-heavy, exact-match-sensitive queries "
        "(ticket IDs, product SKUs, ticker symbols) and where infra simplicity/cost matters.\n"
        "- **Hybrid**: generally the safest default — recovers cases either single method misses, "
        "at the cost of running both pipelines.\n"
        "- **Graph RAG**: best where the enterprise data has real entity relationships to traverse "
        "(company↔filing, customer↔ticket↔product); highest ingestion cost (LLM entity extraction "
        "per document) and depends heavily on extraction quality.\n"
    )

    report_path = RESULTS_DIR / "reports" / "report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("".join(out), encoding="utf-8")
    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
