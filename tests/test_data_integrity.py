"""
Data Integrity and Schema Validation Tests for NASA PSI Combustion Science Dataset.

Validates that:
- The JSON dataset file exists and adheres to the expected ~285 KB enriched file size.
- Exactly 24 flight investigations are present with complete schema and flight metadata.
- All 347 peer-reviewed articles load cleanly, with valid titles and valid DOIs where present.
"""

import json
import os
import re

DATASET_PATH = os.path.join("data", "psi_combustion_science.json")
EXPECTED_CATEGORIES = {
    "Spacecraft Fire Safety",
    "Droplet Combustion",
    "Gaseous Combustion",
}
EXPECTED_PLATFORMS = {
    "International Space Station (ISS)",
    "Cygnus Spacecraft",
    "Not Applicable",
}


def test_json_file_exists_and_size() -> None:
    """Action 2.1: Enforce JSON dataset existence and enriched flight payload size."""
    assert os.path.exists(DATASET_PATH), f"Dataset not found at {DATASET_PATH}"
    file_size = os.path.getsize(DATASET_PATH)
    assert 280000 <= file_size <= 305000, (
        f"Unexpected dataset size: {file_size} bytes (expected 280,000 - 305,000 bytes)"
    )


def test_investigations_count_and_keys() -> None:
    """Action 2.2: Verify 24 investigations load with complete scientific flight metadata."""
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list), (
        "Root dataset must be a list of investigation records"
    )
    assert len(data) == 24, f"Expected exactly 24 investigations, found {len(data)}"

    accessions_seen = set()

    for item in data:
        acc = item.get("accession")
        assert acc and acc.startswith("PSI-"), f"Invalid accession: {acc}"
        assert acc not in accessions_seen, f"Duplicate accession detected: {acc}"
        accessions_seen.add(acc)

        assert item.get("title") and len(item["title"].strip()) > 0, (
            f"Empty title in {acc}"
        )
        assert item.get("category") in EXPECTED_CATEGORIES, (
            f"Invalid category '{item.get('category')}' in {acc}"
        )
        assert item.get("platform") in EXPECTED_PLATFORMS, (
            f"Invalid platform '{item.get('platform')}' in {acc}"
        )
        assert item.get("objectives") and len(item["objectives"].strip()) > 0, (
            f"Missing objectives in {acc}"
        )
        assert item.get("hypothesis") and len(item["hypothesis"].strip()) > 0, (
            f"Missing hypothesis in {acc}"
        )
        assert item.get("approach") and len(item["approach"].strip()) > 0, (
            f"Missing approach in {acc}"
        )
        assert isinstance(item.get("publications"), list), (
            f"Invalid publications in {acc}"
        )


def test_publications_total_and_dois() -> None:
    """Action 2.3: Verify all 347 publications exist with valid titles and DOIs where present."""
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_publications = 0
    publications_with_doi = 0
    doi_pattern = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$")

    for item in data:
        pubs = item.get("publications", [])
        total_publications += len(pubs)
        for pub in pubs:
            title = pub.get("title", "")
            assert isinstance(title, str) and len(title.strip()) > 0, (
                f"Empty publication title found in investigation {item.get('accession')}"
            )

            doi = pub.get("doi", "")
            if doi and len(doi.strip()) > 0:
                publications_with_doi += 1
                assert doi.startswith("10."), (
                    f"DOI '{doi}' does not start with standard prefix '10.' in {item.get('accession')}"
                )
                assert doi_pattern.match(doi.strip()), (
                    f"Malformed DOI string: '{doi}' in {item.get('accession')}"
                )

    assert total_publications == 347, (
        f"Expected 347 publications, found {total_publications}"
    )
    assert publications_with_doi == 280, (
        f"Expected 280 publications with DOI (67 empty), found {publications_with_doi}"
    )
