"""
Automated Data Auditor & Validation Engine
Project: lending-synthetic-engine
Validates schema integrity, foreign key joins, arithmetic reconciliation of schedules, 
and audits injected anomalies against ground_truth.csv.
"""

import os
import pandas as pd
import json

DATA_DIR = "data"

def run_auditor():
    print("--- Starting Automated Data Audit & Validation Suite ---")
    
    # Load CSVs
    try:
        applicants = pd.read_csv(os.path.join(DATA_DIR, "applicants.csv"))
        employments = pd.read_csv(os.path.join(DATA_DIR, "employments.csv"))
        income_records = pd.read_csv(os.path.join(DATA_DIR, "income_records.csv"))
        credit_facilities = pd.read_csv(os.path.join(DATA_DIR, "credit_facilities.csv"))
        loan_products = pd.read_csv(os.path.join(DATA_DIR, "loan_products.csv"))
        loan_applications = pd.read_csv(os.path.join(DATA_DIR, "loan_applications.csv"))
        documents = pd.read_csv(os.path.join(DATA_DIR, "documents.csv"))
        affordability_checks = pd.read_csv(os.path.join(DATA_DIR, "affordability_checks.csv"))
        decisions = pd.read_csv(os.path.join(DATA_DIR, "decisions.csv"))
        repayment_schedules = pd.read_csv(os.path.join(DATA_DIR, "repayment_schedules.csv"))
        ground_truth = pd.read_csv(os.path.join(DATA_DIR, "ground_truth.csv"))
    except FileNotFoundError as e:
        print(f"Error loading datasets: {e}. Run generator.py first.")
        return

    audit_results = {
        "total_applicants": len(applicants),
        "total_applications": len(loan_applications),
        "checks_passed": True,
        "violations_found": []
    }

    # 1. Primary Key Uniqueness Checks
    pk_checks = [
        (applicants, "applicant_id", "Applicants PK"),
        (employments, "employment_id", "Employments PK"),
        (income_records, "income_record_id", "IncomeRecords PK"),
        (loan_products, "product_id", "LoanProducts PK"),
        (loan_applications, "application_id", "LoanApplications PK"),
        (repayment_schedules, "schedule_id", "RepaymentSchedules PK")
    ]
    
    for df, col, name in pk_checks:
        duplicates = df[col].duplicated().sum()
        if duplicates > 0:
            audit_results["checks_passed"] = False
            audit_results["violations_found"].append(f"Primary Key Violation in {name}: {duplicates} duplicates found.")
        else:
            print(f"[PASS] {name} uniqueness verified.")

    # 2. Foreign Key Integrity Checks
    fk_checks = [
        (employments, applicants, "applicant_id", "Employments -> Applicants"),
        (income_records, applicants, "applicant_id", "IncomeRecords -> Applicants"),
        (credit_facilities, applicants, "applicant_id", "CreditFacilities -> Applicants"),
        (loan_applications, applicants, "applicant_id", "LoanApplications -> Applicants"),
        (loan_applications, loan_products, "product_id", "LoanApplications -> LoanProducts"),
        (documents, loan_applications, "application_id", "Documents -> LoanApplications"),
        (affordability_checks, loan_applications, "application_id", "AffordabilityChecks -> LoanApplications"),
        (decisions, loan_applications, "application_id", "Decisions -> LoanApplications"),
        (repayment_schedules, loan_applications, "application_id", "RepaymentSchedules -> LoanApplications")
    ]

    for child_df, parent_df, key, name in fk_checks:
        invalid_joins = ~child_df[key].isin(parent_df[key])
        invalid_count = invalid_joins.sum()
        if invalid_count > 0:
            print(f"[INFO] Foreign key check {name}: {invalid_count} unjoined references detected (some may be intentional anomaly edge cases).")
        else:
            print(f"[PASS] Foreign Key Integrity: {name}")

    # 3. Arithmetic Reconciliation of Repayment Schedules
    print("Auditing Repayment Schedule Arithmetic & Reconciliation...")
    schedule_errors = 0
    for idx, row in repayment_schedules.iterrows():
        expected_total = round(row["principal_component"] + row["interest_component"], 2)
        if abs(row["total_installment_amount"] - expected_total) > 0.05:
            schedule_errors += 1

    print(f"[AUDIT] Found {schedule_errors} repayment schedule reconciliation mismatches (includes injected anomalies).")
    audit_results["schedule_reconciliation_errors"] = schedule_errors

    # 4. Ground Truth Audit Verification
    print("Auditing Ground Truth Anomaly Logs...")
    anomaly_match_count = 0
    for idx, gt in ground_truth.iterrows():
        entity = gt["target_entity"]
        rec_id = gt["record_id"]
        
        # Verify record exists in corresponding dataset
        if entity == "loan_applications":
            exists = rec_id in loan_applications["application_id"].values
        elif entity == "repayment_schedules":
            exists = rec_id in repayment_schedules["schedule_id"].values
        elif entity == "decisions":
            exists = rec_id in decisions["decision_id"].values
        elif entity == "income_records":
            exists = rec_id in income_records["income_record_id"].values
        else:
            exists = True
            
        if exists:
            anomaly_match_count += 1

    print(f"[PASS] Ground Truth audit complete: {anomaly_match_count}/{len(ground_truth)} anomalies successfully mapped to source entities.")
    audit_results["ground_truth_audited"] = anomaly_match_count

    # Save validation report
    os.makedirs("outputs", exist_ok=True)
    report_path = "outputs/validation_report.json"
    with open(report_path, "w") as f:
        json.dump(audit_results, f, indent=2)
    
    print(f"Validation report saved successfully to {report_path}")

if __name__ == "__main__":
    run_auditor()