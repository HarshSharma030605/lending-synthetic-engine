"""
Deterministic Core Entity Synthetic Data Generator & Multi-Format Exporter
Project: lending-synthetic-engine
Seed: 20261022
Generates raw operational tables and exports them to CSV, JSON, and SQL DDL + INSERT formats.
"""

import json
import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Set deterministic fixed seed
FIXED_SEED = 20261022
random.seed(FIXED_SEED)
np.random.seed(FIXED_SEED)

# Output directories setup
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

NUM_APPLICANTS = 10000
NUM_APPLICATIONS = 6000

LOAN_PRODUCTS = [
    {
        "product_id": "PROD-PERSONAL",
        "product_name": "Personal Unsecured Loan",
        "min_principal": 1000.00,
        "max_principal": 50000.00,
        "min_term_months": 12,
        "max_term_months": 60,
        "base_interest_rate": 0.1250,
    },
    {
        "product_id": "PROD-AUTO",
        "product_name": "Auto Financing Loan",
        "min_principal": 5000.00,
        "max_principal": 75000.00,
        "min_term_months": 24,
        "max_term_months": 84,
        "base_interest_rate": 0.0750,
    },
    {
        "product_id": "PROD-HOME",
        "product_name": "Residential Mortgage Loan",
        "min_principal": 50000.00,
        "max_principal": 750000.00,
        "min_term_months": 120,
        "max_term_months": 360,
        "base_interest_rate": 0.0550,
    },
    {
        "product_id": "PROD-BIZ",
        "product_name": "Small Business Expansion Loan",
        "min_principal": 10000.00,
        "max_principal": 250000.00,
        "min_term_months": 12,
        "max_term_months": 120,
        "base_interest_rate": 0.0950,
    },
]

FIRST_NAMES = [
    "Aarav",
    "Vihaan",
    "Aditya",
    "Sai",
    "Reyansh",
    "Ananya",
    "Diya",
    "Priya",
    "Rahul",
    "Sneha",
    "Kavya",
    "Rohan",
    "Tanvi",
    "Vikram",
    "Neha",
    "Amit",
    "Pooja",
    "Raj",
    "Siddharth",
    "Meera",
]
LAST_NAMES = [
    "Sharma",
    "Verma",
    "Patel",
    "Rao",
    "Reddy",
    "Gupta",
    "Nair",
    "Kumar",
    "Singh",
    "Joshi",
    "Chawla",
    "Mehta",
    "Deshmukh",
    "Bhat",
    "Kapoor",
]
EMPLOYERS = [
    "TechCorp Global",
    "Vertex Solutions",
    "Apex Healthcare",
    "Innovate Analytics",
    "Metropolis Logistics",
    "Horizon Retail",
    "Titan Infra",
    "CloudScale Labs",
]
JOB_TITLES = [
    "Software Engineer",
    "Data Analyst",
    "Operations Manager",
    "Sales Executive",
    "Financial Specialist",
    "HR Generalist",
    "Systems Architect",
    "Product Designer",
]

tables = {
    "loan_products": LOAN_PRODUCTS,
    "applicants": [],
    "employments": [],
    "income_records": [],
    "credit_facilities": [],
    "loan_applications": [],
    "documents": [],
    "ground_truth": [],
}


def generate_core_baseline_data():
  print("Generating Core Raw Baseline Entities...")
  start_date = datetime(1975, 1, 1)
  end_date = datetime(2003, 1, 1)

  for i in range(1, NUM_APPLICANTS + 1):
    app_id = f"APP-2026-{i:06d}"
    fn = random.choice(FIRST_NAMES)
    ln = random.choice(LAST_NAMES)
    dob = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )
    email = f"{fn.lower()}.{ln.lower()}{i}@example.com"
    phone = f"+9198{random.randint(10000000, 99999999)}"
    emp_flag = True if random.random() > 0.05 else False

    tables["applicants"].append({
        "applicant_id": app_id,
        "first_name": fn,
        "last_name": ln,
        "dob": dob.strftime("%Y-%m-%d"),
        "email": email,
        "phone": phone,
        "employment_status_flag": emp_flag,
        "created_at": datetime.astimezone(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
    })

    emp_id = f"EMP-2026-{i:06d}"
    emp_type = (
        random.choice([
            "FULL_TIME",
            "FULL_TIME",
            "FULL_TIME",
            "PART_TIME",
            "CONTRACT",
        ])
        if emp_flag
        else "UNEMPLOYED"
    )
    monthly_inc = round(random.uniform(25000, 250000), 2) if emp_flag else 0.0

    tables["employments"].append({
        "employment_id": emp_id,
        "applicant_id": app_id,
        "employer_name": random.choice(EMPLOYERS) if emp_flag else "N/A",
        "job_title": random.choice(JOB_TITLES) if emp_flag else "Unemployed",
        "tenure_months": random.randint(6, 180) if emp_flag else 0,
        "employment_type": emp_type,
        "monthly_income": monthly_inc,
        "created_at": datetime.astimezone(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
    })

    inc_id = f"INC-2026-{i:06d}"
    tables["income_records"].append({
        "income_record_id": inc_id,
        "applicant_id": app_id,
        "employment_id": emp_id,
        "verified_monthly_income": monthly_inc,
        "verification_source": random.choice(
            ["PAYSLIP", "TAX_RETURN", "BANK_STATEMENT"]
        ),
        "effective_date": "2026-01-01",
        "created_at": datetime.astimezone(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
    })

    num_facilities = random.randint(1, 3)
    for f_idx in range(1, num_facilities + 1):
      fac_id = f"CF-2026-{i:06d}-{f_idx:02d}"
      f_type = random.choice(["CREDIT_CARD", "AUTO_LOAN", "PERSONAL_LOAN"])
      bal = round(random.uniform(5000, 150000), 2)
      pmt = round(bal * random.uniform(0.03, 0.08), 2)
      tables["credit_facilities"].append({
          "facility_id": fac_id,
          "applicant_id": app_id,
          "facility_type": f_type,
          "current_balance": bal,
          "monthly_payment": pmt,
          "status": "ACTIVE",
          "created_at": datetime.astimezone(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
      })

  applicant_sample = random.sample(tables["applicants"], NUM_APPLICATIONS)
  for idx, app in enumerate(applicant_sample, 1):
    app_id = app["applicant_id"]
    loan_app_id = f"LOAN-2026-{idx:06d}"
    prod = random.choice(LOAN_PRODUCTS)

    req_principal = round(
        random.uniform(prod["min_principal"], prod["max_principal"]), 2
    )
    req_term = random.randint(prod["min_term_months"], prod["max_term_months"])

    tables["loan_applications"].append({
        "application_id": loan_app_id,
        "applicant_id": app_id,
        "product_id": prod["product_id"],
        "requested_principal": req_principal,
        "requested_term_months": req_term,
        "application_status": "SUBMITTED",
        "applied_at": datetime.astimezone(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
    })

    doc_types = ["ID_PROOF", "INCOME_PROOF", "BANK_STATEMENT"]
    for d_idx, d_type in enumerate(doc_types, 1):
      tables["documents"].append({
          "document_id": f"DOC-{loan_app_id}-{d_idx:03d}",
          "application_id": loan_app_id,
          "document_type": d_type,
          "verification_status": "VERIFIED",
          "uploaded_at": datetime.astimezone(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
      })


def inject_core_edge_cases():
  print("Injecting Core Raw Anomalies...")
  app_indices = list(range(len(tables["loan_applications"])))
  random.shuffle(app_indices)

  for idx in app_indices[:50]:
    app = tables["loan_applications"][idx]
    prod = next(
        p
        for p in tables["loan_products"]
        if p["product_id"] == app["product_id"]
    )
    corrupted_term = prod["max_term_months"] + 60
    app["requested_term_months"] = corrupted_term
    tables["ground_truth"].append({
        "target_entity": "loan_applications",
        "record_id": app["application_id"],
        "issue_type": "TERM_OUTSIDE_PRODUCT_RANGE",
        "description": (
            f"Term {corrupted_term} exceeds max allowed"
            f" {prod['max_term_months']}"
        ),
        "is_anomaly": True,
    })

  for idx in app_indices[150:200]:
    app = tables["loan_applications"][idx]
    applicant_id = app["applicant_id"]
    inc_rec = next(
        i
        for i in tables["income_records"]
        if i["applicant_id"] == applicant_id
    )
    inc_rec["verified_monthly_income"] = round(
        inc_rec["verified_monthly_income"] * 0.4, 2
    )
    tables["ground_truth"].append({
        "target_entity": "income_records",
        "record_id": inc_rec["income_record_id"],
        "issue_type": "INCOME_SOURCE_CONFLICT",
        "description": "Verified income conflicts with claimed employment income",
        "is_anomaly": True,
    })

  for idx in app_indices[200:220]:
    orig_app = tables["loan_applications"][idx]
    dup_app_id = f"{orig_app['application_id']}-DUP"
    dup_record = dict(orig_app)
    dup_record["application_id"] = dup_app_id
    dup_record["application_status"] = "DISBURSED"
    orig_app["application_status"] = "DISBURSED"
    tables["loan_applications"].append(dup_record)
    tables["ground_truth"].append({
        "target_entity": "loan_applications",
        "record_id": dup_app_id,
        "issue_type": "DUPLICATE_APPLICATION_DISBURSED_TWICE",
        "description": "Duplicate application instance disbursed twice",
        "is_anomaly": True,
    })


def export_multi_format():
  """Exports all core tables to CSV, JSON, and SQL DDL + INSERT statements."""
  print("Exporting Core Tables to CSV, JSON, and SQL Formats...")

  sql_lines = [
      "-- YottaFlex AI Synthetic Lending Engine SQL Seed Data",
      f"-- Generated with Fixed Seed: {FIXED_SEED}",
      "-- Target Dialect: ANSI SQL / MySQL / PostgreSQL",
      "",
  ]

  for table_name, records in tables.items():
    if not records:
      continue
    df = pd.DataFrame(records)

    # 1. Export CSV
    csv_path = os.path.join(DATA_DIR, f"{table_name}.csv")
    df.to_csv(csv_path, index=False)

    # 2. Export JSON
    json_path = os.path.join(DATA_DIR, f"{table_name}.json")
    df.to_json(json_path, orient="records", indent=2)

    # 3. Build SQL DDL & Inserts
    sql_lines.append(f"-- Table: {table_name}")
    sql_lines.append(f"DROP TABLE IF EXISTS `{table_name}`;")

    cols = df.columns.tolist()
    col_defs = []
    for c in cols:
      sample_val = df[c].iloc[0] if len(df) > 0 else ""
      if isinstance(sample_val, (int, np.integer)):
        dtype = "INT"
      elif isinstance(sample_val, (float, np.floating)):
        dtype = "DECIMAL(15,2)"
      elif isinstance(sample_val, bool):
        dtype = "BOOLEAN"
      else:
        dtype = "VARCHAR(255)"
      col_defs.append(f"  `{c}` {dtype}")

    sql_lines.append(
        f"CREATE TABLE `{table_name}` (\n"
        + ",\n".join(col_defs)
        + "\n);\n"
    )

    for _, row in df.iterrows():
      vals = []
      for val in row:
        if pd.isna(val):
          vals.append("NULL")
        elif isinstance(val, (int, float, np.number)):
          vals.append(str(val))
        elif isinstance(val, bool):
          vals.append("1" if val else "0")
        else:
          escaped = str(val).replace("'", "''")
          vals.append(f"'{escaped}'")
      sql_lines.append(
          f"INSERT INTO `{table_name}` (`{'`,`'.join(cols)}`) VALUES"
          f" ({','.join(vals)});"
      )
    sql_lines.append("\n")

    print(f" Saved {table_name} -> CSV, JSON, and SQL ({len(records)} rows)")

  sql_path = os.path.join(DATA_DIR, "lending_seed_data.sql")
  with open(sql_path, "w") as f:
    f.write("\n".join(sql_lines))
  print(f" Saved master SQL dump to {sql_path}")


if __name__ == "__main__":
  print(f"--- Starting Multi-Format Exporter Generator (Seed: {FIXED_SEED}) ---")
  generate_core_baseline_data()
  inject_core_edge_cases()
  export_multi_format()
  print("--- Multi-Format Export Complete! ---")