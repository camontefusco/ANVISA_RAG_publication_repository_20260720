from __future__ import annotations

import math
import random
import re
import unicodedata
from collections import Counter, defaultdict
from statistics import mean
from typing import Any, Iterable, Sequence


def normalize_label(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    ascii_text = "".join(
        character for character in decomposed if not unicodedata.combining(character)
    )
    return re.sub(r"\s+", " ", ascii_text).strip().lower()


def binary_relevance(gold: Sequence[str], retrieved: Sequence[str]) -> list[int]:
    """Return one relevance grade per result, crediting each gold item once."""
    remaining = Counter(normalize_label(item) for item in gold if item)
    grades: list[int] = []
    for item in retrieved:
        normalized = normalize_label(item)
        is_relevant = bool(normalized and remaining[normalized] > 0)
        grades.append(int(is_relevant))
        if is_relevant:
            remaining[normalized] -= 1
    return grades


def recall_at_k(gold: Sequence[str], retrieved: Sequence[str], k: int) -> float | None:
    if not gold:
        return None
    return sum(binary_relevance(gold, retrieved[:k])) / len(gold)


def precision_at_k(gold: Sequence[str], retrieved: Sequence[str], k: int) -> float | None:
    if not gold or k <= 0:
        return None
    return sum(binary_relevance(gold, retrieved[:k])) / k


def reciprocal_rank_at_k(
    gold: Sequence[str], retrieved: Sequence[str], k: int
) -> float | None:
    if not gold:
        return None
    for rank, relevance in enumerate(binary_relevance(gold, retrieved[:k]), start=1):
        if relevance:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(gold: Sequence[str], retrieved: Sequence[str], k: int) -> float | None:
    if not gold:
        return None
    grades = binary_relevance(gold, retrieved[:k])
    dcg = sum(grade / math.log2(rank + 1) for rank, grade in enumerate(grades, 1))
    ideal_relevant = min(len(gold), k)
    ideal = sum(1.0 / math.log2(rank + 1) for rank in range(1, ideal_relevant + 1))
    return dcg / ideal if ideal else 0.0


def percentile(values: Sequence[float], probability: float) -> float:
    if not values:
        raise ValueError("Cannot compute a percentile of an empty sequence.")
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def clustered_bootstrap_mean_ci(
    rows: Sequence[dict[str, Any]],
    key: str,
    cluster_key: str = "pair_id",
    confidence: float = 0.95,
    resamples: int = 2000,
    seed: int = 20260619,
) -> tuple[float | None, float | None, float | None, int]:
    """Bootstrap a mean while resampling bilingual question pairs as clusters."""
    grouped: dict[str, list[float]] = defaultdict(list)
    for index, row in enumerate(rows):
        value = row.get(key)
        if isinstance(value, bool):
            value = float(value)
        if not isinstance(value, (int, float)) or value is None:
            continue
        cluster = str(row.get(cluster_key) or row.get("id") or index)
        grouped[cluster].append(float(value))

    if not grouped:
        return None, None, None, 0

    cluster_values = [values for values in grouped.values()]
    observed = mean(value for values in cluster_values for value in values)
    rng = random.Random(seed)
    estimates: list[float] = []
    for _ in range(resamples):
        sampled = [rng.choice(cluster_values) for _ in cluster_values]
        estimates.append(mean(value for values in sampled for value in values))

    alpha = (1 - confidence) / 2
    return (
        observed,
        percentile(estimates, alpha),
        percentile(estimates, 1 - alpha),
        len(grouped),
    )


def paired_language_difference_ci(
    rows: Sequence[dict[str, Any]],
    key: str,
    confidence: float = 0.95,
    resamples: int = 2000,
    seed: int = 20260619,
) -> tuple[float | None, float | None, float | None, int]:
    """Estimate the paired Portuguese-minus-English metric difference."""
    paired: dict[str, dict[str, float]] = defaultdict(dict)
    for row in rows:
        value = row.get(key)
        if isinstance(value, bool):
            value = float(value)
        language = str(row.get("language", ""))
        pair_id = str(row.get("pair_id", ""))
        if isinstance(value, (int, float)) and language in {"pt", "en"} and pair_id:
            paired[pair_id][language] = float(value)
    differences = [
        values["pt"] - values["en"]
        for values in paired.values()
        if set(values) == {"pt", "en"}
    ]
    if not differences:
        return None, None, None, 0
    observed = mean(differences)
    rng = random.Random(seed)
    estimates = [
        mean(rng.choice(differences) for _ in differences) for _ in range(resamples)
    ]
    alpha = (1 - confidence) / 2
    return (
        observed,
        percentile(estimates, alpha),
        percentile(estimates, 1 - alpha),
        len(differences),
    )


def cohen_kappa(labels_a: Iterable[str], labels_b: Iterable[str]) -> float | None:
    pairs = [
        (str(a).strip(), str(b).strip())
        for a, b in zip(labels_a, labels_b)
        if str(a).strip() and str(b).strip()
    ]
    if not pairs:
        return None
    categories = sorted({label for pair in pairs for label in pair})
    observed = sum(a == b for a, b in pairs) / len(pairs)
    proportions_a = Counter(a for a, _ in pairs)
    proportions_b = Counter(b for _, b in pairs)
    expected = sum(
        proportions_a[category] / len(pairs) * proportions_b[category] / len(pairs)
        for category in categories
    )
    if expected == 1:
        return None
    return (observed - expected) / (1 - expected)


def agreement_rate(labels_a: Iterable[str], labels_b: Iterable[str]) -> float | None:
    pairs = [
        (str(a).strip(), str(b).strip())
        for a, b in zip(labels_a, labels_b)
        if str(a).strip() and str(b).strip()
    ]
    return sum(a == b for a, b in pairs) / len(pairs) if pairs else None


def bootstrap_agreement_ci(
    labels_a: Sequence[str],
    labels_b: Sequence[str],
    statistic: str = "kappa",
    confidence: float = 0.95,
    resamples: int = 2000,
    seed: int = 20260619,
) -> tuple[float | None, float | None, float | None, int]:
    pairs = [
        (str(a).strip(), str(b).strip())
        for a, b in zip(labels_a, labels_b)
        if str(a).strip() and str(b).strip()
    ]
    if not pairs:
        return None, None, None, 0
    metric = cohen_kappa if statistic == "kappa" else agreement_rate
    observed = metric([a for a, _ in pairs], [b for _, b in pairs])
    rng = random.Random(seed)
    estimates: list[float] = []
    for _ in range(resamples):
        sample = [rng.choice(pairs) for _ in pairs]
        estimate = metric([a for a, _ in sample], [b for _, b in sample])
        if estimate is not None:
            estimates.append(estimate)
    if observed is None or not estimates:
        return observed, None, None, len(pairs)
    alpha = (1 - confidence) / 2
    return (
        observed,
        percentile(estimates, alpha),
        percentile(estimates, 1 - alpha),
        len(pairs),
    )
