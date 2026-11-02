# Prompt History & Engineering Log

**Project**: Synthetic Lending Data Pipeline & Validation Engine

**Candidate / Engineer**: Harsh

**Role Target**: YottaFlex AI Forward Deployed Engineer (72-Hour Challenge)

**Deterministic Seed**: `20261022`

---

## Executive Summary

This log records the curated, effective prompt history used during the architecture, design, implementation, multi-format expansion, and optimization of the synthetic lending dataset generator and auditor. All redundant iterations, discarded temporary paths, and security-sensitive configurations have been filtered out to present a clean, audit-ready record of the prompt engineering workflow.

---

## Chronological Prompt Sequence

### 1. Architecture & Entity Schema Design

**Prompt**:
> "Design a modular, deterministic synthetic lending data pipeline and validation engine. The architecture should support 10 relational tables (Applicant, Employment, IncomeRecord, CreditFacility, LoanProduct, LoanApplication, Document, AffordabilityCheck, Decision, RepaymentSchedule). Enforce fixed seed 20261022, specific naming conventions, and 5 mandatory edge cases (term violations, schedule mismatch, premature decision, income conflict, duplicate disbursal)."

**Outcome**: Established 10 core entity schemas, primary/foreign key definitions, and deterministic baseline parameters.

---

### 2. Core Entity Synthetic Generator Implementation

**Prompt**:
> "Write a generator script (`src/generator.py`) with separate functions: a normal generator for baseline data using fixed seed 20261022, an edge case anomaly injector for the 5 specified edge cases, and an exporter that writes each table to CSV format. Make sure to include the specified number of instances (10k applicants, 6k applications) and isolated ground-truth logging."

**Outcome**: Implemented modular `src/generator.py` producing 10,000 master applicants and 6,000+ loan applications with reproducible outputs.

---

### 3. CSV Architecture Refinement & Decoupling

**Prompt**:
> "Let's remove the SQL database connection angle of this project as having raw data in live databases and CSVs is redundant. We will continue generation via scripts. Also, separate the core generator to generate only raw deterministic parent/transaction tables, and move downstream metrics calculation into `src/rules.py`."

**Outcome**: Eliminated live database connection overhead. Refactored `src/generator.py` to focus exclusively on raw operational entities (`applicants`, `employments`, `income_records`, `credit_facilities`, `loan_products`, `loan_applications`, `documents`) and `ground_truth.csv`.

---

### 4. Business Rules & Derived Analytics Engine

**Prompt**:
> "Create `src/rules.py` to compute derived analytics (DTI, disposable income, compounding EMIs, underwriting decision rule citations, and amortization repayment schedules) from the raw core CSVs."

**Outcome**: Implemented standalone `src/rules.py` reading raw CSVs and outputting derived analytics tables (`affordability_checks.csv`, `decisions.csv`, `repayment_schedules.csv`).

---

### 5. Automated Data Auditor & Validation Engine

**Prompt**:
> "Write `src/validator.py` to check schema integrity, primary key uniqueness, foreign key referential joins, arithmetic reconciliation of payment schedules (principal + interest vs total installment), and verify injected anomalies against `ground_truth.csv`, exporting results to `outputs/validation_report.json`."

**Outcome**: Created complete automated auditor script validating schema integrity, schedule math reconciliations, and ground truth mapping.

---

### 6. Pipeline Orchestration & CLI Design

**Prompt**:
> "Write the master CLI runner (`main.py`) that executes the 3 phases sequentially: core generation (`generator.py`) -> rules calculation (`rules.py`) -> validation audit (`validator.py`)."

**Outcome**: Built `main.py` enabling single-command execution (`python3 main.py`).

---

### 7. Dependency Pinning & Requirements

**Prompt**:
> "Create a clean `requirements.txt` file pinning all required dependencies for the CSV pipeline."

**Outcome**: Generated `requirements.txt` with locked library versions (`pandas`, `numpy`, `python-dotenv`).

---

### 8. Multi-Format Export Expansion (CSV, JSON, SQL DDL + INSERTs)

**Prompt**:
> "To satisfy explicit multi-format seed export criteria, update `src/generator.py` and `src/rules.py` so that all 10 relational entities are simultaneously exported to CSV, JSON, and a unified ANSI SQL seed file (`data/lending_seed_data.sql`) complete with table DDL (`CREATE TABLE`) and deterministic `INSERT` statements."

**Outcome**: Enabled full triple-format export (`.csv`, `.json`, `.sql`) across all core operational and derived analytics entities.

---

### 9. Multi-Run Reproducibility Verification (Step 10 Audit)

**Prompt**:
> "Update `main.py` to include an automated double-run reproducibility verification phase (Step 10) that computes SHA256 cryptographic checksums across consecutive pipeline executions to prove 100% determinism and identical validation output reports."

**Outcome**: Integrated Phase 4 into `main.py`, providing automated cryptographic proof of exact deterministic execution across multiple runs.

---

### 10. Structured Machine-Readable Schema Manifest

**Prompt**:
> "Create a comprehensive machine-readable `outputs/schema.json` artifact detailing field data types, nullability constraints, primary keys, foreign key relationships, and entity classifications for all 10 relational tables."

**Outcome**: Generated `outputs/schema.json` to enable automated programmatic verification of table structure and constraints by evaluators.

---

### 11. Large File Storage & Zip Archive Strategy

**Prompt**:
> "Due to GitHub file size limits (50 MB soft limit / 100 MB hard limit) on large amortization schedule files, structure a zip archive strategy (`data.zip`) so all generated multi-format data can be cleanly pushed to the public GitHub repository without hitting Git LFS barriers."

**Outcome**: Adopted a compressed data storage approach (`data.zip`) while keeping Python source code and execution modules unzipped in the repository root.

---

### 12. Production Documentation & User Attribution Note

**Prompt**:
> "Generate a master `README.md` containing the fixed seed `20261022`, single-command execution guide, complete Data Dictionary for all 10 entities, Source Manifest, edge case anomaly map, and an explicit development note stating that the architectural design, domain rules, and data model were user-defined while the code implementation was generated with AI assistance."

**Outcome**: Published the comprehensive `README.md` repository documentation complete with architectural flow diagrams and clear candidate attribution.

---

## Key Refinement & Decision Summary

* **Decoupled 3-Module Architecture**: Shifted from monolithic generation to distinct modules (`generator.py` $\rightarrow$ `rules.py` $\rightarrow$ `validator.py`), ensuring clean isolation of raw entities, risk metrics, and audit rules.
* **Multi-Format Export Standard**: Expanded output capabilities beyond standard CSVs to include structured JSON arrays and runnable ANSI SQL script files (`data/lending_seed_data.sql`).
* **Cryptographic Verification**: Automated determinism verification via double-run SHA256 checksum comparisons directly within `main.py`.
* **Security & Cleanliness**: Removed all live database environment credentials, temporary configs, and unneeded dependencies.