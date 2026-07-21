# Supplementary Data S2. AI-Judge Criteria and Prompt

## Purpose

This file documents the automated AI-judge layer used to screen generated RAG answers. The judge was used for reproducible answer-quality scoring, not as a replacement for expert regulatory review.

## Judge model and settings

- Judge model: `models/gemini-flash-lite-latest`
- Temperature: `0.0`
- Input per row: question, system answer, expected answer, answerability label, and retrieved article-level evidence.
- Output per row: JSON with four numeric scores from 0 to 1 and a short rationale.
- Retrieval evidence for judge calls: top five passages reconstructed from saved retrieval and rerank queries where available.
- Main code path: `evaluation/answer_quality.py`

## Scoring criteria

- Faithfulness: every factual claim in the answer is supported by the retrieved evidence.
- Citation correctness: citations are present when an answer is given, point to retrieved evidence, and support the associated claim. Article-level citation labels were accepted even when the support was in a paragraph, item, or subitem inside the cited article.
- Completeness: the answer covers the essential expected information, including material conditions and exceptions.
- Refusal correctness: unanswerable questions should be refused without an unsupported answer; answerable questions should be answered rather than refused.

## Thresholds used for row-level flags

- Scores below 0.8 were flagged for review.
- For answerable questions, the main flags were faithfulness below 0.8, citation correctness below 0.8, completeness below 0.8, and literal refusal.
- For unanswerable or adversarial questions, refusal correctness below 0.8 was flagged.
- Saturated results, including scores of 1.000 across small or development-linked sets, were treated as possible overfitting or insufficient challenge and were not interpreted as proof of perfect reliability.

## Exact judge prompt template

```text
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
```

## Limitations

The AI judge may share assumptions with the answer-generation model and can over-score concise answers or under-score boundary cases. Its scores were therefore used as screening labels, supplemented by per-question error flags and external stress tests. Rows judged after a targeted repair step are development evidence rather than independent validation.
