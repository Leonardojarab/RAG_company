"""
Run retrieval evaluation and save results to JSON.
Used by GitHub Actions CI workflow.
"""
import json
from datetime import datetime
from pathlib import Path

from evaluation.eval import evaluate_all_retrieval


def main():
    results = []
    total_mrr = 0.0
    total_ndcg = 0.0
    total_coverage = 0.0
    count = 0

    print("Running retrieval evaluation...")
    for test, result, progress in evaluate_all_retrieval():
        count += 1
        total_mrr += result.mrr
        total_ndcg += result.ndcg
        total_coverage += result.keyword_coverage
        print(f"  [{count}] {test.question[:60]}... MRR={result.mrr:.3f}")

    avg_mrr = total_mrr / count
    avg_ndcg = total_ndcg / count
    avg_coverage = total_coverage / count

    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_tests": count,
        "avg_mrr": round(avg_mrr, 4),
        "avg_ndcg": round(avg_ndcg, 4),
        "avg_coverage": round(avg_coverage, 2),
    }

    print("\n=== RESULTS ===")
    print(f"Tests run:  {count}")
    print(f"Avg MRR:    {avg_mrr:.4f}")
    print(f"Avg nDCG:   {avg_ndcg:.4f}")
    print(f"Coverage:   {avg_coverage:.1f}%")

    output_path = Path("evaluation/results.json")
    output_path.write_text(json.dumps(summary, indent=2))
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
