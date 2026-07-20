import unittest

from evaluation.answer_quality import citation_validity, sanitize_answer_citations


class CitationQualityTests(unittest.TestCase):
    def test_sanitizes_paragraph_suffix_to_retrieved_article_label(self):
        answer = "Use this rule [RDC 945/2024, Art. 85, § 2º]."
        sanitized = sanitize_answer_citations(answer, ["RDC 945/2024, Art. 85"])
        self.assertEqual(sanitized, "Use this rule [RDC 945/2024, Art. 85].")

    def test_malformed_citation_counts_against_validity(self):
        answer = (
            "One exact [RDC 945/2024, Art. 85] and one embellished "
            "[RDC 945/2024, Art. 85, § 2º]."
        )
        present, validity = citation_validity(answer, ["RDC 945/2024, Art. 85"])
        self.assertTrue(present)
        self.assertEqual(validity, 0.5)


if __name__ == "__main__":
    unittest.main()
