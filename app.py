# app.py
import streamlit as st
from src.engine import get_chat_engine
from src.model_loader import Translator, load_answer_llm
from src.config import DEFAULT_LANGUAGE_PREF, DEBUG_MODE_DEFAULT

st.set_page_config(page_title="ANVISA Navigator", layout="wide")

# -----------------------------
# Load everything once
# -----------------------------
@st.cache_resource(show_spinner=True)
def load_all():
    translator = Translator()
    answer_llm = load_answer_llm()
    query_engine = get_chat_engine()
    return query_engine, translator, answer_llm


query_engine, translator, answer_llm = load_all()

# -----------------------------
# Sidebar Settings
# -----------------------------
st.sidebar.title("⚙ Settings")

lang_pref = st.sidebar.radio(
    "Answer Language Preference",
    ["Bilingual", "Portuguese Only", "English Only"],
    index=["Bilingual", "Portuguese Only", "English Only"].index(DEFAULT_LANGUAGE_PREF),
)

debug_mode = st.sidebar.checkbox("Show Debug Info", value=DEBUG_MODE_DEFAULT)

# -----------------------------
# UI
# -----------------------------
st.title("🧪 ANVISA Navigator — ANVISA Regulatory Assistant")
st.write("Ask in English or Portuguese. The assistant rewrites, translates, retrieves ANVISA laws, and answers bilingually.")

user_input = st.text_input("Ask your ANVISA regulatory question...")

if user_input:
    with st.spinner("Processing..."):

        # 1. Rewrite query to Portuguese for retrieval
        rewritten_query = translator.rewrite_for_retrieval(user_input)

        # 2. Retrieve regulatory content
        response = query_engine.query(rewritten_query)

        raw_text = str(response)

        # 3. Generate bilingual answer
        if lang_pref == "Bilingual":
            pt_answer = translator.translate(raw_text, "Portuguese")
            en_answer = translator.translate(raw_text, "English")

            st.subheader("🇧🇷 Portuguese")
            st.write(pt_answer)

            st.subheader("🇺🇸 English")
            st.write(en_answer)

        elif lang_pref == "Portuguese Only":
            pt_answer = translator.translate(raw_text, "Portuguese")
            st.subheader("🇧🇷 Portuguese")
            st.write(pt_answer)

        elif lang_pref == "English Only":
            en_answer = translator.translate(raw_text, "English")
            st.subheader("🇺🇸 English")
            st.write(en_answer)

        if debug_mode:
            st.divider()
            st.write("### 🔍 Debug Info")
            st.write("**Rewritten Query:**", rewritten_query)
            st.write("**Raw RAG Response:**", raw_text)
            source_rows = []
            for rank, source_node in enumerate(response.source_nodes, start=1):
                metadata = source_node.node.metadata or {}
                source_rows.append(
                    {
                        "Rank": rank,
                        "Citation": metadata.get("citation_label", "Unknown source"),
                        "Chapter": metadata.get("chapter", ""),
                        "Section": metadata.get("section", ""),
                        "Score": round(float(source_node.score), 4)
                        if source_node.score is not None
                        else None,
                    }
                )
            if source_rows:
                st.write("**Retrieved Sources:**")
                st.dataframe(source_rows, hide_index=True, use_container_width=True)
