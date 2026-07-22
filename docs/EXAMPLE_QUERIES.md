# Example Queries With Cited Outputs

These examples are provided as public-facing demonstrations of the prototype behavior. They are not a replacement for the benchmark files in `evaluation/`.

## Example 1

Question:

> What does RDC 945/2024 regulate?

Answer:

> A RDC 945/2024 regulamenta as diretrizes e os procedimentos para a realização de ensaios clínicos com medicamentos no país, incluindo a submissão do Dossiê de Desenvolvimento Clínico de Medicamento (DDCM), visando a posterior concessão de registro de medicamentos [RDC 945/2024, Art. 1].

Interpretation:

This is the Streamlit smoke-test example. It demonstrates a valid answer with a regulation and article citation.

## Example 2

Question:

> In a clinical trial, when must unblinding be reported to ANVISA?

Expected behavior:

The answer should retrieve the clinical-trial regulation and cite the specific article governing unblinding or reporting. If the retrieved context only contains general safety-reporting language and not the specific unblinding rule, the system should refuse rather than answer from nearby rules.

## Example 3

Question:

> Quais informacoes minimas tornam uma notificacao valida e notificavel?

Expected behavior:

The answer should identify the relevant stability or notification provision, cite the source document and article, and avoid expanding beyond the article text.

## Example 4

Question:

> What MedDRA version is currently required today?

Expected behavior:

This is an unanswerable/adversarial style question unless the retrieved ANVISA context states the current version. The system should answer that the documents do not provide enough information.

## Example 5

Question:

> For a medical device, where should the instructions for use be made available?

Expected behavior:

The answer should retrieve the medical-device regulation, cite the specific article, and keep the response limited to the retrieved provision.
