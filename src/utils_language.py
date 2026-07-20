def detect_language(llm, text: str) -> str:
    prompt = (
        "Detect the language of the following text. Respond with exactly one word: "
        "'English', 'Portuguese', or 'Other'.\n\n"
        f"{text}"
    )
    return llm.complete(prompt).strip()


def translate(llm, text: str, target: str) -> str:
    prompt = f"Translate the following text into {target}:\n\n{text}"
    return llm.complete(prompt).strip()


def rewrite_query_to_portuguese(llm, query: str) -> (str, str):
    """
    Returns: rewritten_query, detected_language
    """
    detected = detect_language(llm, query)

    if detected.lower().startswith("port"):
        return query, detected

    # Rewrite English → Portuguese
    rewritten = translate(llm, query, "Portuguese")
    return rewritten, detected
