# Regulatory/pharma journal filtering

Date: 2026-07-19

Scope used for filtering: regulatory science, pharmaceutical medicine, health-product regulation, ANVISA/regulatory document interpretation, AI-assisted regulatory information retrieval.

Hard filters:

- PubMed/MEDLINE indexed, preferably currently indexed for MEDLINE.
- No required APC route, meaning subscription/hybrid publication must be available without APC and without relying on a waiver.
- Not a very high-impact venue.
- Accepts regulatory, pharmaceutical, or medical-product policy/methods work.

## Result

### Best target: Therapeutic Innovation & Regulatory Science

Decision: best current fit.

Why:

- Direct scope match: medical product discovery, development, regulation, access, and policy.
- Official scientific journal of DIA.
- Springer lists the journal as hybrid.
- Springer states authors can publish under the subscription model with no APC charges; APC applies only if open access is selected after acceptance.
- Springer lists Medline indexing.
- 2025 journal impact factor: 2.1, so it is not a super-high-impact target.
- The journal has an open topical collection on AI in Drug Development, which helps the AI/regulatory framing.

How to frame the manuscript:

"A bilingual article-aware retrieval-augmented generation system for regulatory document interpretation in Brazilian pharmaceutical and health-product regulation."

Do not frame it primarily as clinical informatics. Emphasize regulatory information access, article-level citation, bilingual regulatory terminology, and refusal under insufficient evidence.

### Second target: Pharmaceutical Medicine

Decision: good alternative, somewhat broader/higher than TIRS.

Why:

- Scope includes pharmaceutical medicine, registration, monitoring, clinical trials, regulatory and ethical requirements for drug development.
- Springer lists it as hybrid and explicitly says traditional subscription publication has no author charge.
- NLM Catalog says currently indexed for MEDLINE from v33n1, 2019 onward.
- Springer lists Medline indexing.
- 2025 impact factor: 4.7, higher than TIRS but still not top-tier clinical medicine.

Risk:

- The paper may need stronger drug-development or pharmaceutical-medicine relevance, not only regulatory document QA.
- Current ANVISA corpus should be tied to medicines, biologics, clinical trials, devices, and regulatory submissions.

### Third target: Regulatory Toxicology and Pharmacology

Decision: PubMed/MEDLINE and no-APC subscription route, but weaker topical fit.

Why:

- NLM Catalog says currently indexed for MEDLINE.
- Elsevier lists subscription publication with no publication fee charged to authors; open access APC is optional.
- Regulatory scope is real.

Risk:

- The journal is mainly toxicology, pharmacology standards, chemical safety, and hazard/risk assessment.
- A RAG system for ANVISA regulatory texts may be seen as outside scope unless the corpus focuses on toxicology/pharmacology regulatory decision-making.

Use only if the manuscript is rewritten around regulatory evaluation standards and safety-regulatory interpretation.

### Exclude: Clinical Therapeutics

Reason:

- It is PubMed/MEDLINE indexed and has a subscription route, but the guide for authors states mandatory editorial page fees after acceptance. This violates the no-APC/no-fee constraint even though the fee is not called an APC.

### Exclude: Journal of Pharmaceutical Policy and Practice

Reason:

- Conceptual fit is good, but it is fully open access and DOAJ lists publication fees/APCs. It depends on payment or waiver, so it fails the hard filter.

### Exclude: Health Policy and Technology

Reason:

- Elsevier lists subscription publication with no author fee, but NLM Catalog says PubMed has selected citations only and it is not currently indexed for MEDLINE.

### Exclude as less relevant fallback only

- Methods of Information in Medicine: PubMed/MEDLINE and no-fee subscription track, but methods/health informatics rather than regulatory/pharma.
- Applied Clinical Informatics: PubMed/MEDLINE, but clinical informatics rather than regulatory/pharma.
- Journal of Biomedical Informatics: PubMed/MEDLINE and no-fee subscription route, but higher impact and less regulatory/pharma focused.
- JAMIA: PubMed/MEDLINE and no-fee subscription route, but high impact and less natural for ANVISA regulatory science.

## Ranked shortlist

1. Therapeutic Innovation & Regulatory Science
2. Pharmaceutical Medicine
3. Regulatory Toxicology and Pharmacology, only if the manuscript is reframed toward regulatory safety/toxicology interpretation
4. Methods of Information in Medicine, fallback if regulatory journals reject the methods angle
5. Applied Clinical Informatics, fallback only if reframed as practical health-product information access

## Manuscript changes for TIRS

Title candidate:

Bilingual article-aware retrieval-augmented generation for ANVISA regulatory document interpretation

Abstract angle:

Regulatory agencies publish dense article-structured rules that are difficult to search across languages. This study evaluates a bilingual RAG pipeline for selected ANVISA pharmaceutical and health-product regulations, focusing on article-level retrieval, source citation, and refusal under insufficient evidence.

Introduction must emphasize:

- Regulatory affairs workload.
- Pharmaceutical and health-product rules.
- Bilingual access to Portuguese health-authority documents.
- Citation and abstention as safety requirements.
- ANVISA as a case corpus, not as a claim of official regulatory endorsement.

Methods must add:

- Exact ANVISA corpus table.
- Article/chunk counts.
- Benchmark schema and checksum.
- AI-judge prompt and model details.
- A statement that no ANVISA, regulatory authority, or expert panel validation was performed.

Discussion must say:

- This is technical validation of a regulatory information retrieval and answer-generation pipeline.
- It is not regulatory advice.
- It cannot answer questions about current forms, fees, private submission status, future approvals, or non-indexed ANVISA material.
