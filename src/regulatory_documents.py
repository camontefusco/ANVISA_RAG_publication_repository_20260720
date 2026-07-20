from __future__ import annotations

import re
from pathlib import Path

from llama_index.core import Document


DOCUMENT_CATALOG = {
    "rdc09_2015.txt": {
        "regulation_id": "RDC 9/2015",
        "document_aliases": "RDC 9/2015; RDC 09/2015",
        "document_type": "RDC",
        "document_number": "9",
        "document_year": "2015",
        "document_title": "Regulamento para ensaios clinicos com medicamentos no Brasil",
        "topics": "ensaios clinicos; clinical trials; medicamentos; medicines; DDCM",
    },
    "RDC_55_2010_Registro_de_Produtos_Biológicos.txt": {
        "regulation_id": "RDC 55/2010",
        "document_aliases": "RDC 55/2010",
        "document_type": "RDC",
        "document_number": "55",
        "document_year": "2010",
        "document_title": "Registro de produtos biologicos",
        "topics": "produtos biologicos; biological products; registro; registration; qualidade; seguranca; eficacia",
    },
    "RDC_751_2022_Regras_de_classificação_de_risco.txt": {
        "regulation_id": "RDC 751/2022",
        "document_aliases": "RDC 751/2022",
        "document_type": "RDC",
        "document_number": "751",
        "document_year": "2022",
        "document_title": "Classificacao de risco, notificacao e registro de dispositivos medicos",
        "topics": "dispositivos medicos; medical devices; classificacao de risco; risk classification; notificacao; registro; rotulagem",
    },
    "RDC_406_2020_Estudos_de_Estabilidade.txt": {
        "regulation_id": "RDC 406/2020",
        "document_aliases": "RDC 406/2020",
        "document_type": "RDC",
        "document_number": "406",
        "document_year": "2020",
        "document_title": "Boas Praticas de Farmacovigilancia para Detentores de Registro de Medicamento",
        "topics": "farmacovigilancia; pharmacovigilance; seguranca de medicamentos; drug safety; detentor de registro",
    },
    "IN_338_2024.txt": {
        "regulation_id": "IN 338/2024",
        "document_aliases": "IN 338/2024",
        "document_type": "IN",
        "document_number": "338",
        "document_year": "2024",
        "document_title": "Procedimento otimizado de analise de ensaios clinicos",
        "topics": "ensaios clinicos; clinical trials; reliance; DDCM; DEEC; risco; complexidade; optimized review",
    },
    "RDC_945_2024.txt": {
        "regulation_id": "RDC 945/2024",
        "document_aliases": "RDC 945/2024",
        "document_type": "RDC",
        "document_number": "945",
        "document_year": "2024",
        "document_title": "Ensaios clinicos com medicamentos de uso humano",
        "topics": "ensaios clinicos; clinical trials; DDCM; DEEC; seguranca; safety; medicamentos",
    },
}

ARTICLE_RE = re.compile(r"^Art\.\s*(\d+)\s*[oº°.]?", re.IGNORECASE)
CHAPTER_RE = re.compile(r"^CAP[IÍ]TULO\s+([IVXLCDM]+|\d+)", re.IGNORECASE)
SECTION_RE = re.compile(r"^SE[CÇ][AÃ]O\s+([IVXLCDM]+|\d+)", re.IGNORECASE)


def _heading_with_subtitle(lines: list[str], index: int) -> str:
    heading = lines[index].strip()
    if index + 1 >= len(lines):
        return heading
    subtitle = lines[index + 1].strip()
    if subtitle and not ARTICLE_RE.match(subtitle) and len(subtitle) <= 140:
        return f"{heading} - {subtitle}"
    return heading


def _make_document(
    text: str,
    source_path: Path,
    catalog_entry: dict[str, str],
    article: str,
    chapter: str,
    section: str,
) -> Document:
    citation_parts = [catalog_entry["regulation_id"]]
    if article != "Preamble":
        citation_parts.append(article)
    citation_label = ", ".join(citation_parts)
    metadata = {
        "file_name": source_path.name,
        "file_path": str(source_path),
        "source_document": source_path.name,
        **catalog_entry,
        "article": article,
        "chapter": chapter,
        "section": section,
        "language": "pt",
        "citation_label": citation_label,
        "source_quality": "cleaned",
    }
    return Document(
        text=text.strip(),
        metadata=metadata,
        excluded_embed_metadata_keys=list(metadata),
    )


def parse_regulatory_document(source_path: Path) -> list[Document]:
    """Split one regulation into article-level documents with citation metadata."""
    catalog_entry = DOCUMENT_CATALOG.get(source_path.name)
    if catalog_entry is None:
        raise ValueError(f"No document metadata configured for {source_path.name}")

    lines = source_path.read_text(encoding="utf-8").splitlines()
    documents: list[Document] = []
    current_lines: list[str] = []
    current_article = "Preamble"
    current_chapter = ""
    current_section = ""
    pending_chapter: str | None = None
    pending_section: str | None = None
    skipped_subtitle_indexes: set[int] = set()

    def flush() -> None:
        nonlocal current_lines
        text = "\n".join(current_lines).strip()
        if text:
            documents.append(
                _make_document(
                    text,
                    source_path,
                    catalog_entry,
                    current_article,
                    current_chapter,
                    current_section,
                )
            )
        current_lines = []

    for index, raw_line in enumerate(lines):
        if index in skipped_subtitle_indexes:
            continue
        line = raw_line.strip()
        if not line:
            continue

        chapter_match = CHAPTER_RE.match(line)
        section_match = SECTION_RE.match(line)
        article_match = ARTICLE_RE.match(line)

        if chapter_match:
            pending_chapter = _heading_with_subtitle(lines, index)
            pending_section = ""
            if " - " in pending_chapter:
                skipped_subtitle_indexes.add(index + 1)
            continue
        elif section_match:
            pending_section = _heading_with_subtitle(lines, index)
            if " - " in pending_section:
                skipped_subtitle_indexes.add(index + 1)
            continue

        if article_match:
            flush()
            if pending_chapter is not None:
                current_chapter = pending_chapter
                pending_chapter = None
            if pending_section is not None:
                current_section = pending_section
                pending_section = None
            current_article = f"Art. {article_match.group(1)}"

        current_lines.append(line)

    flush()
    return documents


def load_regulatory_documents(data_path: Path) -> list[Document]:
    """Load every configured regulation and fail loudly on corpus drift."""
    source_paths = sorted(data_path.glob("*.txt"))
    source_names = {path.name for path in source_paths}
    configured_names = set(DOCUMENT_CATALOG)
    missing_metadata = source_names - configured_names
    missing_files = configured_names - source_names
    if missing_metadata or missing_files:
        raise ValueError(
            "Regulatory corpus and metadata catalog differ. "
            f"Missing metadata: {sorted(missing_metadata)}; "
            f"missing files: {sorted(missing_files)}"
        )

    documents: list[Document] = []
    for source_path in source_paths:
        documents.extend(parse_regulatory_document(source_path))
    return documents
