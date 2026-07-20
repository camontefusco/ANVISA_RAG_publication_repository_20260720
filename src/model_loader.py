import os
import re
import time
import unicodedata
from typing import Any

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, RetryError, ServiceUnavailable
from dotenv import load_dotenv
from llama_index.core.llms import (
    CompletionResponse,
    CompletionResponseGen,
    CustomLLM,
    LLMMetadata,
)
from src.config import (
    GEMINI_API_KEY,
    GEMINI_REWRITE_MODEL,
    GEMINI_ANSWER_MODEL,
)

load_dotenv()

# Disable Google Cloud ADC completely
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
os.environ["GOOGLE_CLOUD_PROJECT"] = ""

# Configure client with explicit API key
api_key = GEMINI_API_KEY or os.getenv("GOOGLE_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)


def _require_api_key() -> str:
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found. Add it to your .env file.")
    return api_key


def generate_with_retry(
    model: genai.GenerativeModel,
    prompt: str,
    *,
    generation_config: dict[str, Any],
    max_attempts: int = 8,
    **kwargs: Any,
):
    """Call Gemini with quota-aware backoff for publication-scale evaluation."""
    for attempt in range(1, max_attempts + 1):
        try:
            return model.generate_content(
                prompt,
                generation_config=generation_config,
                **kwargs,
            )
        except (ResourceExhausted, RetryError, ServiceUnavailable):
            if attempt == max_attempts:
                raise
            time.sleep(min(60, 10 * attempt))


def _is_grounding_refusal(text: str) -> bool:
    normalized = "".join(
        character
        for character in unicodedata.normalize("NFKD", text.lower())
        if not unicodedata.combining(character)
    )
    return (
        "documentos recuperados" in normalized
        and "informacao suficiente" in normalized
    ) or (
        "retrieved documents" in normalized
        and ("enough information" in normalized or "sufficient information" in normalized)
    )


def _allows_preamble_only(prompt: str) -> bool:
    match = re.search(r"Question:\s*(.*?)\s*Answer:\s*$", prompt, re.DOTALL)
    if not match:
        return False
    normalized_question = "".join(
        character
        for character in unicodedata.normalize("NFKD", match.group(1).lower())
        if not unicodedata.combining(character)
    )
    return bool(
        re.search(
            r"\b(?:data|date|dated|publicada|publicado|published|publication)\b",
            normalized_question,
        )
    )
class GeminiGenerativeLLM(CustomLLM):
    """LlamaIndex-compatible wrapper around google.generativeai."""

    model_name: str
    temperature: float = 0.2

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=8192,
            num_output=1024,
            model_name=self.model_name,
        )

    def complete(
        self,
        prompt: str,
        formatted: bool = False,
        **kwargs: Any,
    ) -> CompletionResponse:
        generation_config = {"temperature": self.temperature}
        generation_config.update(kwargs.pop("generation_config", {}) or {})
        model = genai.GenerativeModel(self.model_name)
        result = generate_with_retry(
            model,
            prompt,
            generation_config=generation_config,
            **kwargs,
        )
        answer_text = result.text or ""
        requires_article_citation = "Final validation:" in prompt
        if (
            requires_article_citation
            and not _allows_preamble_only(prompt)
            and not _is_grounding_refusal(answer_text)
            and ", Art." not in answer_text
        ):
            revision_prompt = (
                f"{prompt}\n\nInvalid draft:\n{answer_text}\n\n"
                "The draft is invalid because it lacks a retrieved article citation. "
                "Return a corrected grounded answer containing at least one exact "
                "[RDC or IN ..., Art. ...] citation from the context. If no article "
                "supports the answer, return only the Portuguese refusal sentence. "
                "Never attach an article citation to a claim that article does not "
                "directly support; instead, revise the claim to match the article."
            )
            revised = generate_with_retry(
                model,
                revision_prompt,
                generation_config=generation_config,
            )
            answer_text = revised.text or ""
            if not _is_grounding_refusal(answer_text) and ", Art." not in answer_text:
                answer_text = (
                    "Os documentos recuperados nao fornecem informacao suficiente "
                    "para responder."
                )
        return CompletionResponse(
            text=answer_text,
            raw={"model_name": self.model_name},
        )

    def stream_complete(
        self,
        prompt: str,
        formatted: bool = False,
        **kwargs: Any,
    ) -> CompletionResponseGen:
        response = self.complete(prompt, formatted=formatted, **kwargs)
        yield response


# ------------------------------
# TRANSLATION / REWRITE LLM
# ------------------------------
def load_rewrite_llm():
    """Gemini model for query rewriting / translation."""
    _require_api_key()
    return GeminiGenerativeLLM(model_name=GEMINI_REWRITE_MODEL, temperature=0.0)


# ------------------------------
# ANSWER GENERATION LLM
# ------------------------------
def load_answer_llm():
    """Gemini model for the final ANVISA answers."""
    _require_api_key()
    return GeminiGenerativeLLM(model_name=GEMINI_ANSWER_MODEL, temperature=0.2)


# ------------------------------
# TRANSLATOR CLASS (simple)
# ------------------------------
class Translator:
    """Translation plus glossary-controlled English-to-Portuguese query rewriting."""

    REGULATORY_GLOSSARY = {
        "clinical trial": "ensaio clínico",
        "clinical trials": "ensaios clínicos",
        "sponsor": "patrocinador",
        "sponsors": "patrocinadores",
        "applicant company": "empresa solicitante",
        "biological product": "produto biológico",
        "biological products": "produtos biológicos",
        "medical device": "dispositivo médico",
        "medical devices": "dispositivos médicos",
        "stability study": "estudo de estabilidade",
        "stability studies": "estudos de estabilidade",
        "terminated prematurely": "finalizado prematuramente",
        "suspended or terminated prematurely": "finalizado prematuramente ou suspenso",
        "required formats": "formatos exigidos",
        "at the time of filing": "no ato do protocolo",
        "standard operating procedures": "Procedimentos Operacionais Padrão",
        "equivalent documents": "documentos equivalentes",
        "pharmacovigilance activities": "atividades de farmacovigilância",
        "responsibilities": "responsabilidades",
    }
    ENGLISH_QUERY_MARKERS = re.compile(
        r"\b(what|which|when|where|who|why|how|does|do|is|are|under|according|"
        r"must|should|can|clinical|sponsor|biological|medical device|stability study)\b",
        re.IGNORECASE,
    )

    def __init__(self):
        _require_api_key()
        self.client = genai.GenerativeModel(GEMINI_REWRITE_MODEL)

    def translate(self, text: str, target_lang: str) -> str:
        normalized = "".join(
            character
            for character in unicodedata.normalize("NFKD", text.lower())
            if not unicodedata.combining(character)
        )
        if (
            target_lang.lower() == "english"
            and "documentos recuperados" in normalized
            and "informacao suficiente" in normalized
        ):
            return "The retrieved documents do not provide enough information to answer."
        prompt = (
            f"Translate this text into {target_lang}. Preserve regulatory identifiers, "
            "acronyms, article numbers, and every square-bracket citation exactly as "
            f"written. Return only the translation:\n{text}"
        )
        result = generate_with_retry(
            self.client,
            prompt,
            generation_config={"temperature": 0.0},
        )
        return result.text

    def maybe_rewrite_query(self, text: str) -> str:
        """Rewrite an English query with canonical PT/EN regulatory terminology."""
        glossary_lines = "\n".join(
            f"- {english} -> {portuguese}"
            for english, portuguese in self.REGULATORY_GLOSSARY.items()
        )
        prompt = (
            "Rewrite the English user query in Portuguese for retrieval over ANVISA "
            "regulatory documents. Do not answer the question. Preserve every acronym "
            "such as DDCM or DEEC, regulation identifier such as RDC 945/2024 or IN "
            "338/2024, number, and article reference. Use the canonical Portuguese "
            "regulatory terminology in this glossary. Return only one concise Portuguese "
            "retrieval query.\n\nGlossary:\n"
            f"{glossary_lines}\n\nEnglish query:\n{text}"
        )
        result = generate_with_retry(
            self.client,
            prompt,
            generation_config={"temperature": 0.0},
        )
        rewritten = (result.text or text).strip()

        expansions = []
        lowered_original = text.lower()
        # Longest phrases first avoids adding both singular and plural variants.
        for english in sorted(self.REGULATORY_GLOSSARY, key=len, reverse=True):
            if re.search(rf"\b{re.escape(english)}\b", lowered_original):
                if any(english.endswith(suffix) for suffix in (" trials", "sponsors", " products", " devices", " studies")):
                    singular = english.removesuffix("s")
                    if any(item.endswith(f"({singular})") for item in expansions):
                        continue
                portuguese = self.REGULATORY_GLOSSARY[english]
                expansions.append(f"{portuguese} ({english})")
        if expansions:
            rewritten = f"{rewritten} Termos regulatórios: {'; '.join(expansions)}."
        return rewritten

    def is_likely_english(self, text: str) -> bool:
        return bool(self.ENGLISH_QUERY_MARKERS.search(text))

    def rewrite_for_retrieval(self, text: str) -> str:
        """Rewrite English input and leave Portuguese input unchanged."""
        return self.rewrite(text) if self.is_likely_english(text) else text

    def rewrite(self, text: str) -> str:
        """Rewrite a known-English query for bilingual regulatory retrieval."""
        return self.maybe_rewrite_query(text)


class GlossaryQueryRewriter:
    """Offline English query expansion for ANVISA retrieval ablations."""

    REGULATORY_GLOSSARY = {
        **Translator.REGULATORY_GLOSSARY,
        "adverse event": "evento adverso",
        "adverse events": "eventos adversos",
        "amendment": "emenda",
        "amendments": "emendas",
        "anvisa's decisions": "decisões da Anvisa",
        "application": "aplicação",
        "applicant company": "empresa solicitante",
        "applicable regulatory requirements": "exigências regulatórias aplicáveis",
        "biological products": "produtos biológicos",
        "cell banks": "bancos de células",
        "clinical development": "desenvolvimento clínico",
        "clinical investigation": "investigação clínica",
        "clinical investigations": "investigações clínicas",
        "clinical studies": "estudos clínicos",
        "clinical trial data": "dados do ensaio clínico",
        "clinically significant event": "evento clinicamente significativo",
        "complete reports": "relatórios completos",
        "communicated": "divulgadas",
        "communication": "divulgação",
        "consequences": "sanções",
        "custom-made": "sob medida",
        "deadline": "prazo",
        "decisions": "decisões",
        "development discontinuation": "descontinuação do desenvolvimento",
        "documentation formats": "formatos de documentação",
        "documentation submitted manually": "documentação protocolizada manualmente",
        "drug registration": "registro de medicamento",
        "drug safety": "segurança de medicamentos",
        "excluded": "excluídos",
        "filing a registration application for a biological product": "protocolo de pedido de registro de um produto biológico",
        "filing": "protocolização",
        "foreign languages": "idiomas estrangeiros",
        "good clinical practice": "Boas Práticas Clínicas",
        "good clinical practices": "Boas Práticas Clínicas",
        "gcp": "BPC",
        "holder": "detentor",
        "import": "importação",
        "importation": "importação",
        "implementing": "implementação",
        "in vitro diagnostic": "diagnóstico in vitro",
        "investigational product": "produto sob investigação",
        "investigator": "investigador",
        "investigator's obligations": "obrigações do investigador",
        "investigator-sponsor": "investigador-patrocinador",
        "legal consequences": "sanções",
        "manual": "manual",
        "manually": "manual",
        "marketing authorization holder": "detentor de registro de medicamento",
        "marketing authorization holders": "detentores de registro de medicamento",
        "master cell bank": "banco de célula mestre",
        "medical devices": "dispositivos médicos",
        "must submit": "deverá apresentar",
        "non-compliance": "descumprimento",
        "non-clinical and clinical studies": "estudos não-clínicos e clínicos",
        "non-reportable": "não reportáveis",
        "notification": "notificação",
        "optimized analysis": "análise otimizada",
        "optimized analysis procedure": "procedimento de análise otimizada",
        "participants": "participantes",
        "pharmacovigilance": "farmacovigilância",
        "pharmacovigilance activities": "atividades de farmacovigilância",
        "petitions": "petições",
        "physical copy": "cópia física",
        "printed copy": "via impressa",
        "primary sponsor": "patrocinador primário",
        "procedural adequacy": "adequação processual",
        "protocol": "protocolo",
        "required formats": "formatos exigidos",
        "registration application": "pedido de registro",
        "registration protocol": "protocolo de registro",
        "registration": "registro",
        "responsibilities": "responsabilidades",
        "responsibilities of those involved": "responsabilidades dos envolvidos",
        "revalidation": "revalidação",
        "risk assessment": "avaliação de risco",
        "risk classification": "classificação de risco",
        "risk management plan": "plano de gerenciamento de risco",
        "risk minimization": "minimização de risco",
        "risk minimization plan": "plano de minimização de risco",
        "serious adverse event": "evento adverso grave",
        "sops": "POPs",
        "stability": "estabilidade",
        "status": "situação",
        "suspended or terminated prematurely": "finalizado prematuramente ou suspenso",
        "standard operating procedures": "procedimentos operacionais padrão",
        "structural units": "unidades estruturais",
        "substantial amendment": "emenda substancial",
        "substantial amendments": "emendas substanciais",
        "terminated prematurely": "finalizado prematuramente",
        "update of classification rules": "atualização das regras de classificação",
        "working cell bank": "banco de célula de trabalho",
        "at the time of filing": "no ato do protocolo",
        "documentation format": "formato da documentação",
        "filed documentation": "documentação protocolada",
        "filing a registration application": "protocolar a solicitação de registro",
        "same information": "mesmas informações",
        "cd-rom": "CD-ROM",
        "pdf": "PDF",
        "activities must be described": "atividades devem estar descritas",
        "described in sops": "descritas em Procedimentos Operacionais Padrão",
        "equivalent documents": "documentos equivalentes",
        "pharmacovigilance system": "Sistema de Farmacovigilância",
        "operational failures": "falhas operacionais",
        "overlaps": "sobreposições",
        "gaps": "lacunas",
        "avoid operational failures": "evitar falhas operacionais",
    }

    def rewrite(self, text: str) -> str:
        lowered = text.lower()
        identifiers = re.findall(
            r"\b(?:RDC|IN)\s*\d+/?\d*|\bDDCM\b|\bDEEC\b|\bBPC\b|\bGCP\b|Art\.?\s*\d+",
            text,
            flags=re.IGNORECASE,
        )
        expansions = []
        for english in sorted(self.REGULATORY_GLOSSARY, key=len, reverse=True):
            if re.search(rf"\b{re.escape(english)}\b", lowered):
                portuguese = self.REGULATORY_GLOSSARY[english]
                expansions.append(f"{portuguese} ({english})")
        seen = set()
        unique_expansions = [
            item for item in expansions if not (item.lower() in seen or seen.add(item.lower()))
        ]
        parts = ["Consulta regulatória ANVISA."]
        if identifiers:
            parts.append("Identificadores: " + "; ".join(dict.fromkeys(identifiers)) + ".")
        if unique_expansions:
            parts.append("Termos regulatórios: " + "; ".join(unique_expansions) + ".")
        parts.append("Pergunta original em inglês: " + text)
        return " ".join(parts)
