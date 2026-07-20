# Source Reproducibility and Redistribution Note

Date: 2026-07-20

This project used public ANVISA regulatory documents. For a future public repository, the safest default is to provide official source links, file checksums, and cleaning/indexing scripts rather than republishing full cleaned copies of the source regulatory text.

## Recommended Public Repository Policy

Include:

- Official AnvisaLegis URLs for each regulation.
- SHA-256 checksums for the raw local files used in the study.
- SHA-256 checksums for the cleaned files used to build the index.
- The cleaning script `clean_regulatory_texts.py`.
- The article-chunking/indexing scripts and benchmark/evaluation artifacts.
- A note that exact generated answers may vary when hosted LLM behavior changes.

Do not include by default:

- Full cleaned copies of ANVISA regulatory text.
- Full raw downloaded MHTML/text captures of ANVISA pages.

Rationale: the source regulations are public, but repository redistribution is cleaner if readers can retrieve the official source directly and verify that the local files used in the study match the reported checksums. Full cleaned text can be added later only if redistribution is confirmed to be acceptable and necessary for peer review or reproducibility.

## Files in This Folder

- `ANVISA_SOURCE_LINKS_AND_CHECKSUMS_20260720.csv`: official source URLs and raw/cleaned file checksums.
- `clean_regulatory_texts.py`: cleaning script used for the source text.

## Cleaning Script Checksum

`clean_regulatory_texts.py`

SHA-256: `5653e7930739f710e49dd921a75e731518984db53f45f30384bc27829d2306ca`
