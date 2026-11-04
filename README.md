# Bilingual ANVISA regulatory RAG

## Current review release

**[v0.3.0](https://github.com/camontefusco/ANVISA_RAG_publication_repository_20260720/releases/tag/v0.3.0)** is the 4 November 2026 review snapshot. Download **ANVISA_RAG_v0.3.0_review_package.zip** from that release. It includes the updated clean and cumulative tracked manuscript, justified reviewer response, tables, supplementary material, seven 600-dpi TIFFs, curated implementation/data and inventories.

Start with [the package guide](revisions/reviewer_2_20261104_final/README.md), [review status](revisions/reviewer_2_20261104_final/REVIEW_STATUS.md) and [file inventory](revisions/reviewer_2_20261104_final/inventory.csv). The [journal-upload candidates](revisions/reviewer_2_20261104_final/journal_upload/) are separated from [reproducibility evidence](revisions/reviewer_2_20261104_final/evidence/) and [release audit records](revisions/reviewer_2_20261104_final/release_audit/).

This is the **finalized revision release; no journal submission has been made**. All supplied reviewer responses are approved. The repository is public; no reviewer-specific access is needed. Earlier release assets and tags remain unchanged and may contain superseded text, scores or review status. Do not mix their documents with this package.

## Purpose and evidence

This prototype evaluates article-level retrieval and cited Portuguese/English answers against archived public ANVISA documents. It supports investigation of evidence access and answer failures, not autonomous regulatory decisions. Citations do not establish completeness or current applicability. The corpus is not automatically maintained as consolidated current law.

The common-prompt coauthor comparison remains hybrid 39/40, BM25 38/40 and model-only 9/40 successful answers, or 19/20, 18/20 and 4/20 bilingual pairs. Hybrid minus BM25 success is +5 percentage points (95% paired interval -10 to +20), without established superiority or equivalence. Model-only receives no retrieved passages or web search; it is not a professional using ordinary search.

The added dated-corpus comparison is provisional AI assessment of 188 revised development-exposed questions: 144/188 versus 172/188 successes, difference +14.9 points (95% paired interval 7.4 to 22.9). Source updates and structural curation were bundled. Regressions, obsolete cross-references and unresolved dependencies remain reported. Comprehensive current-law accuracy, fresh independent external validation and measured human workflow benefit remain unestablished.

The historical 94-output review was AI-draft-assisted. The corresponding author corrected the exposure account on 4 November: Howard had not seen automated judge scores before finalizing those ratings. This is recorded separately; full blinding is not inferred. The later 118-distinct-answer review was self-drafted, with its separate provenance retained.

## Reproducibility

- [Root implementation](src/) and [evaluation code](evaluation/).
- [Cleaning script](scripts/clean_regulatory_texts.py).
- [Historical benchmark](evaluation/publication_benchmark_200.jsonl).
- [Historical official-source manifest and checksums](docs/ANVISA_SOURCE_LINKS_AND_CHECKSUMS_20260720.csv). These document a snapshot, not comprehensive current-law verification.
- [Current curated evidence archive](revisions/reviewer_2_20261104_final/evidence/revision_data.zip): source checksums, frozen outputs, separate AI/author assessments, dated-corpus analysis, negative controls, S13 run-date ledger and S14 complete rule audit.
- [Supplementary Data S16](revisions/reviewer_2_20261104_final/evidence/Supplementary_Data_S16.zip): dated-corpus experiment and first-level source-dependency audit.
- [Inventory audit](docs/GITHUB_PACKAGE_INVENTORY_20261104.md).

The new package preserves the full 114-entry glossary, the separate Translator-mode distinction and existing glossary/rule-family ablations. It does not establish an effect for every individual rule or generalization to fresh independent questions.

Full raw/cleaned corpora, vector indexes, credentials and concealed coordinator keys are excluded. Use the included source links/checksums and retained implementation to reconstruct sources where available. Historical data inside archives retain original values; consult the active evidence guide and correction overlays before interpretation.

## Running the historical prototype

Create the environment from environment.yml, activate rag-project-env and copy .env.example to a local .env. Add a valid Google API key locally; never commit it. Obtain the archived sources from the manifest, clean them with scripts/clean_regulatory_texts.py, then run rebuild_index.py. See evaluation/publication_eval.py --help for evaluation options. API generation, translation and judging may incur provider usage; publishing this release made no new model calls.

Run the historical interface with streamlit run app.py. Its old smoke test answered an English question in Portuguese. It demonstrates app/backend wiring, not reliable bilingual deployment or equivalence to the frozen experimental pipeline. Deployment validation remains separate.

## Authorship and license

Carlos Victor Montefusco-Pereira wrote the implementation after teaching/examples from WBS Coding School, the DSAI02 class and Shenia Bosch; no copied Shenia code is claimed. Howard Lopes Ribeiro Junior contributed regulatory/pharmaceutical framing, interpretation, author assessment and critical manuscript revision. AI assistance and review provenance are disclosed in the manuscript and Supplementary S11.

Repository-authored code/documentation use the [MIT license](LICENSE); official sources and third-party materials are not relicensed.

## Citation and version history

Use [CITATION.cff](CITATION.cff) and cite the exact GitHub tag for this review release. No new Zenodo DOI is claimed. The previous v0.2.1 snapshot is archived at https://doi.org/10.5281/zenodo.23925532; it does not contain the subsequent additions. The concept DOI https://doi.org/10.5281/zenodo.21504181 identifies the version family, not this exact file set.
