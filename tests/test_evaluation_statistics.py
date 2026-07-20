from __future__ import annotations

import unittest

from evaluation.evaluation_statistics import (
    agreement_rate,
    binary_relevance,
    clustered_bootstrap_mean_ci,
    cohen_kappa,
    ndcg_at_k,
    paired_language_difference_ci,
    precision_at_k,
    recall_at_k,
    reciprocal_rank_at_k,
)


class RetrievalMetricTests(unittest.TestCase):
    def test_article_metrics_credit_each_gold_article_once(self) -> None:
        gold = ["RDC 9/2015, Art. 51", "RDC 9/2015, Art. 52"]
        retrieved = [
            "RDC 9/2015, Art. 51",
            "RDC 9/2015, Art. 51",
            "RDC 9/2015, Art. 52",
        ]
        self.assertEqual(binary_relevance(gold, retrieved), [1, 0, 1])
        self.assertEqual(recall_at_k(gold, retrieved, 2), 0.5)
        self.assertEqual(recall_at_k(gold, retrieved, 3), 1.0)
        self.assertAlmostEqual(precision_at_k(gold, retrieved, 3), 2 / 3)
        self.assertEqual(reciprocal_rank_at_k(gold, retrieved, 3), 1.0)
        self.assertGreater(ndcg_at_k(gold, retrieved, 3), 0.9)

    def test_article_matching_is_case_accent_and_whitespace_robust(self) -> None:
        self.assertEqual(
            recall_at_k(["IN 338/2024, Art. 7"], ["  in 338/2024,  ART. 7 "], 1),
            1.0,
        )


class UncertaintyAndAgreementTests(unittest.TestCase):
    def test_clustered_bootstrap_counts_pairs_not_rows(self) -> None:
        rows = [
            {"pair_id": "A", "score": 1},
            {"pair_id": "A", "score": 1},
            {"pair_id": "B", "score": 0},
            {"pair_id": "B", "score": 0},
        ]
        estimate, lower, upper, clusters = clustered_bootstrap_mean_ci(
            rows, "score", resamples=200
        )
        self.assertEqual(estimate, 0.5)
        self.assertEqual(clusters, 2)
        self.assertLessEqual(lower, estimate)
        self.assertGreaterEqual(upper, estimate)

    def test_kappa_and_agreement(self) -> None:
        first = ["1", "1", "0", "0"]
        second = ["1", "1", "0", "0"]
        self.assertEqual(agreement_rate(first, second), 1.0)
        self.assertEqual(cohen_kappa(first, second), 1.0)

    def test_kappa_is_undefined_without_category_variation(self) -> None:
        self.assertEqual(agreement_rate(["1", "1"], ["1", "1"]), 1.0)
        self.assertIsNone(cohen_kappa(["1", "1"], ["1", "1"]))

    def test_paired_language_difference(self) -> None:
        rows = [
            {"pair_id": "A", "language": "pt", "score": 1},
            {"pair_id": "A", "language": "en", "score": 0},
            {"pair_id": "B", "language": "pt", "score": 0.5},
            {"pair_id": "B", "language": "en", "score": 0.5},
        ]
        estimate, lower, upper, pairs = paired_language_difference_ci(
            rows, "score", resamples=200
        )
        self.assertEqual(estimate, 0.5)
        self.assertEqual(pairs, 2)
        self.assertLessEqual(lower, estimate)
        self.assertGreaterEqual(upper, estimate)


if __name__ == "__main__":
    unittest.main()
