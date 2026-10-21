# CTC-008 — Repository Fixture Inventory: Initial Evidence Check

**Date:** 2026-10-21  
**Status:** In Progress; not closure-ready  
**Baseline:** CTC-007 approved full Git snapshot, locally available; remote GitHub HEAD not verified.

## Scope and acceptance
Inventory and score 13 candidate repositories, including file-level fixtures, pinned commit SHA, licensing, valid/invalid cases, country/format coverage, and reproducible scores. Do not equate a public repository with a validated fixture collection.

## Current evidence
- **OpenPEPPOL/peppol-bis-invoice-3**: Public specification repository includes `rules/examples/base-example.xml` and other examples. Confirmed from GitHub file page. Source: https://github.com/OpenPEPPOL/peppol-bis-invoice-3/blob/master/rules/examples/base-example.xml
- **CIRFMF/ksef-client-java**: Public Java KSeF SDK with demo application and integration-test scenarios. Existence of independently validated invoice fixtures remains unverified. Source: https://github.com/CIRFMF/ksef-client-java
- **brasil-fiscal/nfe**: Public NF-e implementation README identifies `examples/nfe-exemplo.xml` as generated example. Its current existence, validity, and licensing for reuse require file-level verification. Source: https://github.com/brasil-fiscal/nfe
- **Other ten repositories**: Candidate list preserved; not independently verified in this pass.

## Scoring policy (not yet applied)
Each category 0–5: (1) actual payload count/diversity, (2) documented provenance and rights, (3) official schema/profile validation, (4) country and format coverage, (5) regression reproducibility (pinned SHA, deterministic fixtures). **No composite score** until commit, license and actual fixture inspection. Unknown is not zero.

## Required next bounded verification
1. Pin exact commit SHA for all reachable repositories and capture license text / SPDX where available.
2. Enumerate XML, JSON and hybrid payload files, excluding schemas, generated source code and documentation examples that are not complete invoices.
3. Identify document family and format by parsing payload roots and namespaces; avoid inferring country from repository name alone.
4. Validate against relevant pinned XSD/Schematron/JSON schemas where possible; record not-run versus invalid.
5. Produce ranked scorecard and prioritized fixture acquisition plan.

## Decisions and checkpoint
CTC-001 through CTC-007 remain Done — scoped. D2, P1–P7, T01–T03, JP-01–JP-10, C006-01–03 and V-01–V-10 unchanged. Eighteen proposed CTC-003 fields remain proposed. CTC-008 is In Progress; no new ADR approved.
