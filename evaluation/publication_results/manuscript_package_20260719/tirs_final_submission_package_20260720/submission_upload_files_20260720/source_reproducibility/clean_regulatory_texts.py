from __future__ import annotations

import argparse
import csv
import email
import html
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT_DIR = PROJECT_ROOT / "data"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "cleaned_data"
DEFAULT_REPORT_PATH = PROJECT_ROOT / "reports" / "cleaned_data_audit.csv"

BLOCK_TAGS = {
    "address",
    "article",
    "br",
    "caption",
    "dd",
    "div",
    "dt",
    "figcaption",
    "footer",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "li",
    "main",
    "p",
    "section",
    "td",
    "th",
    "tr",
}


class LegalHTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "svg", "noscript"}:
            self.skip_depth += 1
            return
        if tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "svg", "noscript"}:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        cleaned = data.strip()
        if cleaned:
            self.parts.append(cleaned)
            self.parts.append(" ")

    def get_text(self) -> str:
        return "".join(self.parts)


def normalize_for_matching(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return ascii_text.lower()


def extract_html_from_mhtml(raw: bytes) -> str | None:
    message = email.message_from_bytes(raw)
    if not message.is_multipart():
        return None

    for part in message.walk():
        content_type = part.get_content_type()
        if content_type != "text/html":
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            continue
        charset = part.get_content_charset() or "utf-8"
        for candidate in [charset, "utf-8", "windows-1252", "latin-1"]:
            try:
                return payload.decode(candidate)
            except UnicodeDecodeError:
                continue
        return payload.decode("utf-8", errors="replace")
    return None


def html_to_text(markup: str) -> str:
    parser = LegalHTMLTextExtractor()
    parser.feed(markup)
    parser.close()
    return parser.get_text()


def decode_text(raw: bytes) -> str:
    for encoding in ["utf-8", "windows-1252", "latin-1"]:
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def repair_pdf_letter_lines(text: str) -> str:
    """Repair words split into one-character-per-line runs."""
    lines = text.splitlines()
    repaired: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if len(line) == 1 and line.isalpha():
            chars = [line]
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if len(next_line) == 1 and next_line.isalpha():
                    chars.append(next_line)
                    j += 1
                    continue
                break
            if len(chars) >= 3:
                repaired.append("".join(chars))
                i = j
                continue
        repaired.append(lines[i])
        i += 1
    return "\n".join(repaired)


def repair_rdc09_ocr(text: str) -> str:
    """Apply high-confidence repairs to the known RDC 9/2015 PDF extraction."""
    title_pattern = re.compile(
        r"(FEVEREIRO DE 2015\s+).*?(?=A Diretoria Colegiada)",
        re.DOTALL | re.IGNORECASE,
    )
    text = title_pattern.sub(
        r"\1Dispõe sobre o Regulamento para a realização de ensaios clínicos "
        r"com medicamentos no Brasil.\n",
        text,
        count=1,
    )
    repairs = {
        "Vigilânc ia": "Vigilância",
        "d o Dossiê": "do Dossiê",
        "medicament os": "medicamentos",
        "forma farmacêutic a": "forma farmacêutica",
        "primá rio": "primário",
        "va cinas": "vacinas",
        "Notificaç ão": "Notificação",
        "i mportação": "importação",
        "Espec ífico": "Específico",
        "p agamento": "pagamento",
        "Sanitár ia": "Sanitária",
        "ens aio": "ensaio",
        "Organiza tion": "Organization",
        "Commi ttee": "Committee",
        "cl ínico": "clínico",
        "R esolução": "Resolução",
        "seg uir": "seguir",
        "ana lisados": "analisados",
        "exigênci as": "exigências",
        "planejamen to": "planejamento",
        "instituiçã o": "instituição",
        "documen tação": "documentação",
        "Ag ência": "Agência",
        "a gosto": "agosto",
        "é ticas": "éticas",
        "um a das": "uma das",
        "estud o clínico": "estudo clínico",
        "pel o DDCM": "pelo DDCM",
        "poss uir": "possuir",
        "disponí vel": "disponível",
    }
    for damaged, repaired in repairs.items():
        text = text.replace(damaged, repaired)
    return text


def remove_obvious_noise_lines(lines: list[str]) -> list[str]:
    noise_patterns = [
        r"^from: <saved by blink>",
        r"^snapshot-content-location:",
        r"^subject:",
        r"^date:",
        r"^mime-version:",
        r"^content-type:",
        r"^content-transfer-encoding:",
        r"^content-location:",
        r"multipartboundary",
        r"stylesheet",
        r"font-family",
        r"background(-color)?\s*:",
        r"border(-radius|-color|-style|-width)?\s*:",
        r"padding\s*:",
        r"margin\s*:",
        r"line-height\s*:",
        r"rgba?\(",
        r"^\.[a-z0-9_-]+\s*\{",
        r"^\}",
        r"^@media",
        r"javascript",
        r"bootstrap",
        r"fontawesome",
        r"apple-touch-icon",
        r"manifest\.json",
        r"favicon",
        r"cid:",
        r"data:image",
        r"amphtml",
    ]
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in noise_patterns]
    cleaned: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        normalized = normalize_for_matching(stripped)
        if any(pattern.search(normalized) for pattern in compiled):
            continue
        if len(stripped) > 180 and stripped.count(";") > 8:
            continue
        cleaned.append(stripped)
    return cleaned


def crop_to_legal_text(lines: list[str]) -> list[str]:
    """Drop website navigation before the official regulation text."""
    priority_groups = [
        [
            r"^minist[eé]rio da sa[uú]de$",
            r"^ag[eê]ncia nacional de vigil[aâ]ncia sanit[aá]ria$",
            r"^advert[eê]ncia$",
        ],
        [
            r"^resolu[cç][aã]o\s+-?\s+rdc",
            r"^instru[cç][aã]o normativa",
        ],
        [
            r"^resolu[cç][aã]o da diretoria colegiada",
        ],
    ]
    for patterns in priority_groups:
        compiled = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for index, line in enumerate(lines):
            normalized = normalize_for_matching(line)
            if any(pattern.search(normalized) for pattern in compiled):
                return lines[index:]
    return lines


def normalize_legal_text(text: str, source_name: str = "") -> str:
    text = html.unescape(text)
    text = repair_pdf_letter_lines(text)
    if source_name.lower() == "rdc09_2015.txt":
        text = repair_rdc09_ocr(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"=\r?\n", "", text)
    text = re.sub(r"(?<!\n)\s*(Art\.\s*\d+)", r"\n\1", text)
    text = re.sub(r"(?<!\n)\s*(CAP[IÍ]TULO\s+[IVXLCDM]+)", r"\n\1", text, flags=re.IGNORECASE)
    text = re.sub(r"(?<!\n)\s*(Se[cç][aã]o\s+[IVXLCDM]+)", r"\n\1", text, flags=re.IGNORECASE)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = crop_to_legal_text(remove_obvious_noise_lines(text.splitlines()))

    # Remove exact consecutive duplicates introduced by saved-page artifacts.
    deduped: list[str] = []
    previous = ""
    for line in lines:
        if line == previous:
            continue
        deduped.append(line)
        previous = line

    return "\n".join(deduped).strip() + "\n"


def clean_file(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    html_part = extract_html_from_mhtml(raw)
    if html_part is not None:
        extracted = html_to_text(html_part)
        mode = "mhtml_html"
    else:
        decoded = decode_text(raw)
        if "<html" in decoded.lower() or "<p" in decoded.lower():
            extracted = html_to_text(decoded)
            mode = "html"
        else:
            extracted = decoded
            mode = "plain_text"
    return normalize_legal_text(extracted, source_name=path.name), mode


def build_report_row(source_path: Path, output_path: Path, mode: str, cleaned_text: str) -> dict[str, str | int]:
    raw_text = decode_text(source_path.read_bytes())
    return {
        "file_name": source_path.name,
        "mode": mode,
        "raw_chars": len(raw_text),
        "cleaned_chars": len(cleaned_text),
        "raw_lines": raw_text.count("\n") + 1,
        "cleaned_lines": cleaned_text.count("\n") + 1,
        "output_path": str(output_path),
    }


def clean_directory(input_dir: Path, output_dir: Path, report_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str | int]] = []
    for source_path in sorted(input_dir.glob("*.txt")):
        cleaned_text, mode = clean_file(source_path)
        output_path = output_dir / source_path.name
        output_path.write_text(cleaned_text, encoding="utf-8")
        rows.append(build_report_row(source_path, output_path, mode, cleaned_text))
        print(
            f"{source_path.name}: {mode}, "
            f"{rows[-1]['raw_lines']} raw lines -> {rows[-1]['cleaned_lines']} cleaned lines"
        )

    with report_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "file_name",
                "mode",
                "raw_chars",
                "cleaned_chars",
                "raw_lines",
                "cleaned_lines",
                "output_path",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Cleaned files written to: {output_dir}")
    print(f"Audit report written to: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean ANVISA regulatory source texts.")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--report-path", type=Path, default=DEFAULT_REPORT_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    clean_directory(args.input_dir, args.output_dir, args.report_path)


if __name__ == "__main__":
    main()
