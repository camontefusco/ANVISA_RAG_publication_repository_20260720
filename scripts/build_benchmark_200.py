from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import google.generativeai as genai

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import DATA_PATH, GEMINI_REWRITE_MODEL
from src.model_loader import generate_with_retry
from src.regulatory_documents import DOCUMENT_CATALOG, load_regulatory_documents


OUTPUT_PATH = ROOT / "evaluation" / "publication_benchmark_200.jsonl"
MANIFEST_PATH = ROOT / "evaluation" / "benchmark_200_manifest.json"
REVIEW_PATH = ROOT / "evaluation" / "benchmark_200_review.csv"

DIRECT_ALLOCATION = {
    "rdc09_2015.txt": 12,
    "RDC_55_2010_Registro_de_Produtos_Biológicos.txt": 12,
    "RDC_751_2022_Regras_de_classificação_de_risco.txt": 12,
    "RDC_406_2020_Estudos_de_Estabilidade.txt": 12,
    "IN_338_2024.txt": 10,
    "RDC_945_2024.txt": 12,
}

INFORMATION_MARKERS = (
    "deve",
    "devera",
    "prazo",
    "objetivo",
    "responsabilidade",
    "submeter",
    "notificar",
    "classifica",
    "registro",
    "proibido",
    "permitido",
    "aplica",
    "dispens",
    "cancel",
    "suspens",
    "relatorio",
)
EXCEPTION_MARKERS = (
    "exceto",
    "salvo",
    "desde que",
    "quando",
    "caso",
    "sem prejuizo",
    "dispens",
    "podera",
    "paragrafo",
    "§",
)


@dataclass
class GoldItem:
    id: str
    pair_id: str
    question: str
    language: str
    category: str
    difficulty: str
    answerable: bool
    gold_sources: list[str]
    gold_articles: list[str]
    gold_citations: list[str]
    gold_evidence: list[str]
    gold_terms: list[str]
    expected_answer: str
    provenance: str
    validation_status: str
    notes: str


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def lexical_normalize(text: str) -> str:
    import unicodedata

    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", ascii_text.lower()).strip()


def evidence_grounded_terms(requested: list[Any], evidence: list[str]) -> list[str]:
    combined = " ".join(evidence)
    lexical_evidence = lexical_normalize(combined)
    terms: list[str] = []
    for term in requested:
        candidate = normalize(str(term))
        if candidate and lexical_normalize(candidate) in lexical_evidence and candidate not in terms:
            terms.append(candidate)

    if len(terms) >= 5:
        return terms[:7]

    stopwords = {
        "artigo", "anvisa", "devera", "disposto", "mediante", "podera",
        "quando", "resolucao", "segundo", "serao", "somente", "todos",
    }
    for token in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]{6,}", combined):
        if len(terms) >= 5:
            break
        normalized_token = lexical_normalize(token)
        if normalized_token in stopwords or token in terms:
            continue
        terms.append(token)
    return terms[:7]


def parse_json_response(text: str) -> Any:
    cleaned = (text or "").strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def article_number(article: str) -> int:
    match = re.search(r"\d+", article)
    return int(match.group()) if match else -1


def information_score(document: Any) -> tuple[int, int, int]:
    text = normalize(document.text).lower()
    marker_score = sum(marker in text for marker in INFORMATION_MARKERS)
    useful_length = min(len(text), 1800)
    definition_penalty = 1 if len(text) > 5000 else 0
    return marker_score - definition_penalty, useful_length, -article_number(document.metadata["article"])


def select_direct_articles(
    by_source: dict[str, list[Any]],
    unique_citations: set[str],
) -> list[Any]:
    selected: list[Any] = []
    for source, count in DIRECT_ALLOCATION.items():
        candidates = [
            document
            for document in by_source[source]
            if document.metadata["article"] != "Preamble"
            and document.metadata["citation_label"] in unique_citations
            and 120 <= len(normalize(document.text)) <= 5000
        ]
        ranked = sorted(candidates, key=information_score, reverse=True)
        if len(ranked) < count:
            raise ValueError(f"Not enough usable articles in {source}: {len(ranked)}")
        chosen: list[Any] = []
        used_numbers: set[int] = set()
        for candidate in ranked:
            number = article_number(candidate.metadata["article"])
            if any(abs(number - existing) <= 1 for existing in used_numbers):
                continue
            chosen.append(candidate)
            used_numbers.add(number)
            if len(chosen) == count:
                break
        for candidate in ranked:
            if len(chosen) == count:
                break
            if candidate not in chosen:
                chosen.append(candidate)
        selected.extend(chosen)
    if len(selected) != 70:
        raise AssertionError(f"Expected 70 direct concepts, got {len(selected)}")
    return selected


def select_complex_specs(
    by_source: dict[str, list[Any]],
    unique_citations: set[str],
) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    sources = list(DIRECT_ALLOCATION)

    for source in sources:
        candidates = []
        for document in by_source[source]:
            text = normalize(document.text).lower()
            score = sum(marker in text for marker in EXCEPTION_MARKERS)
            if (
                document.metadata["article"] != "Preamble"
                and document.metadata["citation_label"] in unique_citations
                and score
            ):
                candidates.append((score, min(len(text), 2500), document))
        candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
        if candidates:
            specs.append({"category": "exception", "documents": [candidates[0][2]]})

    for source in sources[:4]:
        articles = sorted(
            [
                d
                for d in by_source[source]
                if d.metadata["article"] != "Preamble"
                and d.metadata["citation_label"] in unique_citations
            ],
            key=lambda document: article_number(document.metadata["article"]),
        )
        best_pair = max(
            zip(articles, articles[1:]),
            key=lambda pair: information_score(pair[0])[0] + information_score(pair[1])[0],
        )
        specs.append({"category": "multi_article", "documents": list(best_pair)})

    if len(specs) != 10:
        raise AssertionError(f"Expected 10 complex concepts, got {len(specs)}")
    return specs


def compact_source(document: Any) -> dict[str, str]:
    return {
        "source_document": document.metadata["source_document"],
        "regulation_id": document.metadata["regulation_id"],
        "article": document.metadata["article"],
        "citation_label": document.metadata["citation_label"],
        "chapter": document.metadata.get("chapter", ""),
        "section": document.metadata.get("section", ""),
        "text": normalize(document.text)[:4500],
    }


def generation_prompt(records: list[dict[str, Any]], mode: str) -> str:
    if mode == "direct":
        task = (
            "For each record, write one natural Portuguese question and its English semantic "
            "equivalent. Both must be answerable only from that article. Avoid asking merely "
            "'what does Article X say'; ask about the regulatory substance."
        )
    else:
        task = (
            "For each record, write one natural Portuguese question and its English semantic "
            "equivalent. For exception records, test the condition, exception, or limitation. "
            "For multi_article records, require information from every supplied article."
        )
    return f"""
You are constructing a bilingual ANVISA regulatory benchmark. {task}

Rules:
- Use only the supplied source text; do not add external legal knowledge.
- Produce concise expected answers in Portuguese and English.
- Preserve regulation identifiers, acronyms, numbers, deadlines, and legal conditions.
- Each expected answer must include every material condition needed for correctness.
- Provide 3 to 7 gold_terms in Portuguese that occur verbatim in the supplied text.
- Do not include citations in the question or answer; citations are added deterministically.
- Return exactly one output object per input key and no additional objects.

Return only a JSON array with fields:
key, question_pt, answer_pt, question_en, answer_en, gold_terms

Inputs:
{json.dumps(records, ensure_ascii=False, indent=2)}
""".strip()


def generate_concepts(
    model: genai.GenerativeModel,
    specs: list[dict[str, Any]],
    mode: str,
) -> list[dict[str, Any]]:
    inputs = []
    for index, spec in enumerate(specs, start=1):
        inputs.append(
            {
                "key": f"{mode}_{index:02d}",
                "category": spec.get("category", "direct_article"),
                "sources": [compact_source(document) for document in spec["documents"]],
            }
        )
    generated: list[dict[str, Any]] = []
    for start in range(0, len(inputs), 6):
        batch = inputs[start : start + 6]
        response = generate_with_retry(
            model,
            generation_prompt(batch, mode),
            generation_config={"temperature": 0.0},
        )
        parsed = parse_json_response(response.text)
        if not isinstance(parsed, list):
            raise ValueError("Generator did not return a JSON array")
        generated.extend(parsed)
    by_key = {record["key"]: record for record in generated}
    missing = [record["key"] for record in inputs if record["key"] not in by_key]
    if missing:
        raise ValueError(f"Generator omitted records: {missing}")
    return [by_key[record["key"]] for record in inputs]


def build_answerable_items(
    specs: list[dict[str, Any]],
    generated: list[dict[str, Any]],
    prefix: str,
) -> list[GoldItem]:
    items: list[GoldItem] = []
    for index, (spec, content) in enumerate(zip(specs, generated), start=1):
        documents = spec["documents"]
        category = spec.get("category", "direct_article")
        pair_id = f"{prefix}_{index:02d}"
        common = {
            "pair_id": pair_id,
            "category": category,
            "difficulty": "medium" if category == "direct_article" else "hard",
            "answerable": True,
            "gold_sources": [d.metadata["source_document"] for d in documents],
            "gold_articles": [d.metadata["article"] for d in documents],
            "gold_citations": [d.metadata["citation_label"] for d in documents],
            "gold_evidence": [normalize(d.text) for d in documents],
            "gold_terms": evidence_grounded_terms(
                content["gold_terms"],
                [normalize(d.text) for d in documents],
            ),
            "provenance": "article_text_machine_drafted",
            "validation_status": "pending_human_review",
            "notes": "Bilingual pair generated from the listed gold article evidence.",
        }
        items.append(
            GoldItem(
                id=f"{pair_id}_PT",
                question=normalize(content["question_pt"]),
                language="pt",
                expected_answer=normalize(content["answer_pt"]),
                **common,
            )
        )
        items.append(
            GoldItem(
                id=f"{pair_id}_EN",
                question=normalize(content["question_en"]),
                language="en",
                expected_answer=normalize(content["answer_en"]),
                **common,
            )
        )
    return items


UNANSWERABLE_CONCEPTS = [
    ("market_price", "Qual é o preço atual de mercado de um medicamento específico no Brasil?", "What is the current market price of a specific medicine in Brazil?"),
    ("medical_advice", "Qual tratamento devo escolher para uma doença autoimune?", "Which treatment should I choose for an autoimmune disease?"),
    ("individual_dose", "Qual dose individual de um produto biológico devo usar?", "What individual dose of a biological product should I use?"),
    ("reimbursement", "Qual valor o sistema de saúde reembolsa por este medicamento?", "How much does the health system reimburse for this medicine?"),
    ("patent", "Quando expira a patente comercial de um produto biológico específico?", "When does the commercial patent for a specific biological product expire?"),
    ("tax", "Qual imposto incide sobre a venda de um dispositivo médico?", "Which tax applies to the sale of a medical device?"),
    ("company_status", "Qual é a situação atual do pedido regulatório da empresa X?", "What is the current status of company X's regulatory submission?"),
    ("future_approval", "A Anvisa aprovará um ensaio clínico apresentado no próximo ano?", "Will Anvisa approve a clinical trial submitted next year?"),
    ("nonexistent_article", "O que determina o Art. 999 da RDC 945/2024?", "What does Article 999 of RDC 945/2024 establish?"),
    ("nonexistent_regulation", "Quais são os requisitos da RDC 1234/2030 para ensaios clínicos?", "What are the requirements of RDC 1234/2030 for clinical trials?"),
    ("fabricated_deadline", "A RDC 751/2022 exige aprovação de dispositivos em exatamente cinco dias?", "Does RDC 751/2022 require device approval in exactly five days?"),
    ("foreign_law", "Quais requisitos da FDA substituem automaticamente as normas da Anvisa?", "Which FDA requirements automatically replace Anvisa regulations?"),
    ("legal_opinion", "Esta empresa deve processar a Anvisa por atrasar uma análise?", "Should this company sue Anvisa for delaying a review?"),
    ("ethics_decision", "O comitê de ética aprovará este protocolo clínico específico?", "Will the ethics committee approve this specific clinical protocol?"),
    ("product_comparison", "Qual marca de medicamento biológico é clinicamente superior?", "Which brand of biological medicine is clinically superior?"),
    ("contact_details", "Qual é o telefone pessoal do servidor responsável por uma submissão?", "What is the personal telephone number of the official responsible for a submission?"),
    ("historical_reason", "Por que um diretor específico votou a favor da RDC 945/2024?", "Why did a specific director vote in favor of RDC 945/2024?"),
    ("guaranteed_outcome", "Seguir a RDC 406/2020 garante que nunca ocorrerá evento adverso?", "Does following RDC 406/2020 guarantee that no adverse event will ever occur?"),
    ("missing_contract", "Quais obrigações constam no contrato privado entre o patrocinador e o centro?", "What obligations are in the private contract between the sponsor and the site?"),
    ("post_corpus_update", "Que alteração regulatória entrou em vigor depois dos documentos deste corpus?", "Which regulatory amendment took effect after the documents in this corpus?"),
]


def build_unanswerable_items() -> list[GoldItem]:
    items: list[GoldItem] = []
    refusal_pt = "Os documentos recuperados nao fornecem informacao suficiente para responder."
    refusal_en = "The retrieved documents do not provide enough information to answer."
    for index, (category, question_pt, question_en) in enumerate(UNANSWERABLE_CONCEPTS, start=1):
        pair_id = f"UNANS_{index:02d}"
        common = {
            "pair_id": pair_id,
            "category": f"unanswerable_{category}",
            "difficulty": "hard",
            "answerable": False,
            "gold_sources": [],
            "gold_articles": [],
            "gold_citations": [],
            "gold_evidence": [],
            "gold_terms": [],
            "provenance": "manually_curated_adversarial_template",
            "validation_status": "pending_human_review",
            "notes": "Must refuse; the requested information is absent, fabricated, predictive, or individualized.",
        }
        items.append(
            GoldItem(
                id=f"{pair_id}_PT",
                question=question_pt,
                language="pt",
                expected_answer=refusal_pt,
                **common,
            )
        )
        items.append(
            GoldItem(
                id=f"{pair_id}_EN",
                question=question_en,
                language="en",
                expected_answer=refusal_en,
                **common,
            )
        )
    return items


def validate_items(items: list[GoldItem], valid_citations: set[str]) -> dict[str, Any]:
    errors: list[str] = []
    ids = [item.id for item in items]
    questions = [item.question.casefold() for item in items]
    counts = Counter(
        "direct_pt" if item.answerable and item.category == "direct_article" and item.language == "pt"
        else "direct_en" if item.answerable and item.category == "direct_article" and item.language == "en"
        else "complex" if item.answerable
        else "unanswerable"
        for item in items
    )
    expected_counts = {"direct_pt": 70, "direct_en": 70, "complex": 20, "unanswerable": 40}
    if len(items) != 200:
        errors.append(f"Expected 200 rows, got {len(items)}")
    if len(ids) != len(set(ids)):
        errors.append("Duplicate IDs found")
    if len(questions) != len(set(questions)):
        errors.append("Duplicate questions found")
    if counts != Counter(expected_counts):
        errors.append(f"Unexpected concept counts: {dict(counts)}")
    for item in items:
        if item.answerable:
            if not item.gold_citations or not item.gold_evidence:
                errors.append(f"{item.id}: answerable item lacks gold evidence")
            invalid = set(item.gold_citations) - valid_citations
            if invalid:
                errors.append(f"{item.id}: unknown citations {sorted(invalid)}")
        elif item.gold_citations or item.gold_evidence:
            errors.append(f"{item.id}: unanswerable item has gold evidence")
    return {"errors": errors, "counts": dict(counts)}


def final_validate(items: list[GoldItem], valid_citations: set[str]) -> dict[str, Any]:
    errors: list[str] = []
    category_counts = Counter(
        "pt_answerable" if item.answerable and item.category == "direct_article" and item.language == "pt"
        else "en_answerable" if item.answerable and item.category == "direct_article" and item.language == "en"
        else "complex" if item.answerable
        else "unanswerable"
        for item in items
    )
    expected = {"pt_answerable": 70, "en_answerable": 70, "complex": 20, "unanswerable": 40}
    if len(items) != 200:
        errors.append(f"Expected 200 rows, got {len(items)}")
    if category_counts != Counter(expected):
        errors.append(f"Expected {expected}, got {dict(category_counts)}")
    ids = [item.id for item in items]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate IDs found")
    for item in items:
        if item.answerable and set(item.gold_citations) - valid_citations:
            errors.append(f"{item.id}: citation not found in corpus")
        if not item.question or not item.expected_answer:
            errors.append(f"{item.id}: blank question or answer")
    return {"errors": errors, "counts": dict(category_counts)}


def write_outputs(items: list[GoldItem], audit: dict[str, Any]) -> None:
    OUTPUT_PATH.write_text(
        "".join(json.dumps(asdict(item), ensure_ascii=False) + "\n" for item in items),
        encoding="utf-8",
    )
    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "benchmark": str(OUTPUT_PATH),
        "total_items": len(items),
        "counts": audit["counts"],
        "validation_errors": audit["errors"],
        "status": "structurally_valid_pending_human_review" if not audit["errors"] else "invalid",
        "corpus_documents": list(DOCUMENT_CATALOG),
        "generator_model": GEMINI_REWRITE_MODEL,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    fields = [
        "id",
        "pair_id",
        "language",
        "category",
        "question",
        "expected_answer",
        "gold_citations",
        "gold_evidence",
        "human_question_clear_0_1",
        "human_answer_supported_0_1",
        "human_citations_exact_0_1",
        "human_pair_equivalent_0_1",
        "human_keep_revise_drop",
        "human_comments",
    ]
    with REVIEW_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in items:
            writer.writerow(
                {
                    "id": item.id,
                    "pair_id": item.pair_id,
                    "language": item.language,
                    "category": item.category,
                    "question": item.question,
                    "expected_answer": item.expected_answer,
                    "gold_citations": "; ".join(item.gold_citations),
                    "gold_evidence": " | ".join(item.gold_evidence),
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the 200-question bilingual gold benchmark.")
    parser.parse_args()

    documents = load_regulatory_documents(DATA_PATH)
    by_source: dict[str, list[Any]] = defaultdict(list)
    for document in documents:
        by_source[document.metadata["source_document"]].append(document)

    citation_counts = Counter(
        document.metadata["citation_label"] for document in documents
    )
    unique_citations = {
        citation for citation, count in citation_counts.items() if count == 1
    }
    direct_documents = select_direct_articles(by_source, unique_citations)
    direct_specs = [{"category": "direct_article", "documents": [document]} for document in direct_documents]
    complex_specs = select_complex_specs(by_source, unique_citations)

    model = genai.GenerativeModel(GEMINI_REWRITE_MODEL)
    direct_generated = generate_concepts(model, direct_specs, "direct")
    complex_generated = generate_concepts(model, complex_specs, "complex")

    core_items = (
        build_answerable_items(direct_specs, direct_generated, "DIRECT")
        + build_answerable_items(complex_specs, complex_generated, "COMPLEX")
        + build_unanswerable_items()
    )
    valid_citations = {document.metadata["citation_label"] for document in documents}
    core_audit = validate_items(core_items, valid_citations)
    if core_audit["errors"]:
        raise ValueError("; ".join(core_audit["errors"]))

    items = core_items
    audit = final_validate(items, valid_citations)
    write_outputs(items, audit)
    if audit["errors"]:
        raise ValueError("; ".join(audit["errors"]))
    print(f"Wrote {len(items)} items to {OUTPUT_PATH}")
    print(f"Manifest: {MANIFEST_PATH}")
    print(f"Solo review sheet: {REVIEW_PATH}")
    print(f"Counts: {audit['counts']}")


if __name__ == "__main__":
    main()
