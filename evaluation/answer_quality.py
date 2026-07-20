from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

import google.generativeai as genai

from src.model_loader import generate_with_retry


CITATION_RE = re.compile(
    r"^(?:RDC|IN)\s+\d+/\d{4}(?:,\s*Art\.\s*\d+)?$",
    re.IGNORECASE,
)
BRACKET_RE = re.compile(r"\[([^\[\]]+)\]")
LOOSE_ARTICLE_CITATION_RE = re.compile(
    r"((?:RDC|IN)\s+\d+/\d{4},\s*Art\.\s*\d+)",
    re.IGNORECASE,
)


def extract_citations(answer: str) -> list[str]:
    return [
        bracket.strip()
        for bracket in BRACKET_RE.findall(answer)
        if CITATION_RE.fullmatch(bracket.strip())
    ]


def normalize_citation(citation: str) -> str:
    return re.sub(r"\s+", " ", citation).strip().lower()


def citation_validity(answer: str, retrieved_citations: list[str]) -> tuple[bool, float]:
    cited = extract_citations(answer)
    citation_like_brackets = [
        bracket.strip()
        for bracket in BRACKET_RE.findall(answer)
        if re.search(r"\b(?:RDC|IN)\s+\d+/\d{4}", bracket, re.IGNORECASE)
    ]
    if not cited and not citation_like_brackets:
        return False, 0.0
    retrieved = {normalize_citation(citation) for citation in retrieved_citations}
    valid = sum(normalize_citation(citation) in retrieved for citation in cited)
    denominator = max(len(citation_like_brackets), len(cited))
    return bool(cited), valid / denominator


def sanitize_answer_citations(answer: str, retrieved_citations: list[str]) -> str:
    """Collapse paragraph/item citation suffixes to retrieved article labels."""
    retrieved = {normalize_citation(citation): citation for citation in retrieved_citations}

    def replace(match: re.Match[str]) -> str:
        bracket = match.group(1).strip()
        if CITATION_RE.fullmatch(bracket):
            return f"[{bracket}]"
        loose = LOOSE_ARTICLE_CITATION_RE.search(bracket)
        if not loose:
            return f"[{bracket}]"
        base = re.sub(r"\s+", " ", loose.group(1)).strip()
        retrieved_label = retrieved.get(normalize_citation(base))
        return f"[{retrieved_label}]" if retrieved_label else f"[{bracket}]"

    return re.sub(r"\[([^\[\]]+)\]", replace, answer)


@dataclass
class JudgeResult:
    faithfulness: float
    citation_correctness: float
    completeness: float
    refusal_correctness: float
    rationale: str


class AnswerQualityJudge:
    def __init__(self, model_name: str) -> None:
        self.model = genai.GenerativeModel(model_name)

    def evaluate(
        self,
        question: str,
        answer: str,
        expected_answer: str,
        answerable: bool,
        contexts: list[tuple[str, str]],
    ) -> JudgeResult:
        evidence = "\n\n".join(
            f"[{citation}]\n{text}" for citation, text in contexts
        )
        prompt = f"""
Evaluate a regulatory RAG answer. Return only JSON with numeric scores from 0 to 1
and a short rationale.

Scoring:
- faithfulness: every factual claim is supported by retrieved evidence.
- citation_correctness: citations exist when an answer is given, refer to retrieved
  evidence, and support the associated claim.
  The system uses article-level citation labels only. If the supporting sentence
  is in a paragraph, item, or subitem inside a retrieved cited article, the
  article-level citation is correct; do not penalize the answer for omitting
  paragraph, item, section, page, or line suffixes.
- completeness: the answer covers the expected answer's essential information,
  including material conditions or exceptions.
- refusal_correctness: score 1 when an unanswerable question is refused without an
  unsupported answer, or when an answerable question is answered rather than refused.

Question answerable from corpus: {answerable}
Question: {question}
Expected answer: {expected_answer}
System answer: {answer}

Retrieved evidence:
{evidence}

JSON fields: faithfulness, citation_correctness, completeness,
refusal_correctness, rationale
""".strip()
        response = generate_with_retry(
            self.model,
            prompt,
            generation_config={"temperature": 0.0},
        )
        response_text = (response.text or "").strip()
        if response_text.startswith("```"):
            response_text = re.sub(r"^```(?:json)?\s*", "", response_text)
            response_text = re.sub(r"\s*```$", "", response_text)
        raw: dict[str, Any] = json.loads(response_text)

        def score(key: str) -> float:
            return min(1.0, max(0.0, float(raw.get(key, 0.0))))

        return JudgeResult(
            faithfulness=score("faithfulness"),
            citation_correctness=score("citation_correctness"),
            completeness=score("completeness"),
            refusal_correctness=score("refusal_correctness"),
            rationale=str(raw.get("rationale", "")),
        )
