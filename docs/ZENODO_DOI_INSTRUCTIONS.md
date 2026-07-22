# Zenodo DOI Instructions

The repository is ready for Zenodo archiving after GitHub-Zenodo integration is enabled.

Steps:

1. Log in to Zenodo with the GitHub-connected account.
2. Go to GitHub integration in Zenodo.
3. Enable archiving for `camontefusco/ANVISA_RAG_publication_repository_20260720`.
4. Create or re-publish a GitHub release from the latest tag.
5. Wait for Zenodo to archive the release.
6. Copy the DOI from Zenodo.
7. Add the DOI to `README.md` and `CITATION.cff`.
8. Commit and push the DOI update.

Recommended release for DOI:

`v0.1.1`

Reason:

This release includes `.zenodo.json`, so Zenodo should import the correct title, creator, ORCID, license, keywords, contributor, and description.
