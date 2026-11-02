"""
Business Rules & Derived Analytics Multi-Format Exporter
Project: lending-synthetic-engine
Reads core deterministic entities, computes derived analytics tables,
and exports them to CSV, JSON, and SQL DDL + INSERT formats.
"""

from datetime import datetime, timedelta
import os
import numpy as np
import pandas as pd

DATA_DIR = "data"


def calculate_emi(
    principal: float, annual_interest_rate: float, term_months: int
) -> float:
  """Derives standard monthly Equated Monthly Installment (EMI) using compounding formula."""
  if term_months <= 0 or principal <= 0:
    return 0.0
  r = annual_interest_rate / 12.0
  if r == 0:
    return round(principal / term_months, 2)
  emi = (principal * r * (1 + r) ** term_months) / (
      ((1 + r) ** term_months) - 1
  )
  return round(emi, 2)


def generate_derived_analytics():
  """Reads raw baseline entity CSVs and generates derived analytics & schedule records."""
  print("--- Running Business Rules Engine to Generate Derived Analytics ---")

  applicants = pd.read_csv(os.path.join(DATA_DIR, "applicants.csv"))
  employments = pd.read_csv(os.path.join(DATA_DIR, "employments.csv"))
  credit_facilities = pd.read_csv(
      os.path.join(DATA_DIR, "credit_facilities.csv")
  )
  loan_products = pd.read_csv(os.path.join(DATA_DIR, "loan_products.csv"))
  loan_applications = pd.read_csv(
      os.path.join(DATA_DIR, "loan_applications.csv")
  )

  affordability_checks = []
  decisions = []
  repayment_schedules = []

  emp_map = employments.set_index("applicant_id")["monthly_income"].to_dict()
  facility_debt_map = (
      credit_facilities.groupby("applicant_id")["monthly_payment"]
      .sum()
      .to_dict()
  )
  product_map = loan_products.set_index("product_id")[
      "base_interest_rate"
  ].to_dict()

  for _, app in loan_applications.iterrows():
    app_id = app["application_id"]
    applicant_id = app["applicant_id"]
    prod_id = app["product_id"]
    req_principal = app["requested_principal"]
    req_term = app["requested_term_months"]

    gross_income = emp_map.get(applicant_id, 0.0)
    existing_debt = facility_debt_map.get(applicant_id, 0.0)
    base_rate = product_map.get(prod_id, 0.10)

    proposed_emi = calculate_emi(req_principal, base_rate, req_term)
    total_monthly_debt = existing_debt + proposed_emi

    dti_ratio = (
        round(total_monthly_debt / gross_income, 4)
        if gross_income > 0
        else 0.9999
    )
    disposable_income = round(gross_income - total_monthly_debt, 2)
    afford_pass = bool((dti_ratio <= 0.50) and (disposable_income >= 5000))

    affordability_checks.append({
        "check_id": f"AFF-{app_id}-01",
        "application_id": app_id,
        "gross_monthly_income": gross_income,
        "total_existing_monthly_debt": existing_debt,
        "proposed_emi": proposed_emi,
        "dti_ratio": dti_ratio,
        "disposable_income": disposable_income,
        "affordability_passed": afford_pass,
        "created_at": datetime.astimezone(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
    })

    decision_outcome = "APPROVED" if afford_pass else "REJECTED"
    rule_citations = (
        "['DTI_UNDER_50', 'DOCS_VERIFIED']"
        if afford_pass
        else "['HIGH_DTI_EXCEEDS_50']"
    )

    decisions.append({
        "decision_id": f"DEC-{app_id}-01",
        "application_id": app_id,
        "decision_outcome": decision_outcome,
        "rule_citations": rule_citations,
        "decided_at": datetime.astimezone(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
    })

    if afford_pass:
      monthly_rate = base_rate / 12.0
      balance = req_principal
      start_pay_date = datetime(2026, 3, 1)

      for pmt_num in range(1, int(req_term) + 1):
        interest_comp = round(balance * monthly_rate, 2)
        principal_comp = round(proposed_emi - interest_comp, 2)

        if pmt_num == req_term:
          principal_comp = balance
          total_inst = round(principal_comp + interest_comp, 2)
          ending_bal = 0.0
        else:
          total_inst = proposed_emi
          ending_bal = round(balance - principal_comp, 2)

        due_d = start_pay_date + timedelta(days=30 * (pmt_num - 1))
        repayment_schedules.append({
            "schedule_id": f"SCH-{app_id}-PMT-{pmt_num:02d}",
            "application_id": app_id,
            "installment_number": pmt_num,
            "due_date": due_d.strftime("%Y-%m-%d"),
            "principal_component": principal_comp,
            "interest_component": interest_comp,
            "total_installment_amount": total_inst,
            "ending_balance": ending_bal,
        })
        balance = ending_bal

  derived_tables = {
      "affordability_checks": affordability_checks,
      "decisions": decisions,
      "repayment_schedules": repayment_schedules,
  }

  sql_append_lines = [
      "\n-- Derived Analytics Tables (Affordability, Decisions, Repayment"
      " Schedules)"
  ]

  for table_name, records in derived_tables.items():
    if not records:
      continue
    df = pd.DataFrame(records)

    # 1. Export CSV
    df.to_csv(os.path.join(DATA_DIR, f"{table_name}.csv"), index=False)

    # 2. Export JSON
    df.to_json(
        os.path.join(DATA_DIR, f"{table_name}.json"), orient="records", indent=2
    )

    # 3. Build SQL DDL & Inserts
    sql_append_lines.append(f"-- Table: {table_name}")
    sql_append_lines.append(f"DROP TABLE IF EXISTS `{table_name}`;")

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

    sql_append_lines.append(
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
      sql_append_lines.append(
          f"INSERT INTO `{table_name}` (`{'`,`'.join(cols)}`) VALUES"
          f" ({','.join(vals)});"
      )
    sql_append_lines.append("\n")

    print(f" Saved {table_name} -> CSV, JSON, and SQL ({len(records)} rows)")

  sql_path = os.path.join(DATA_DIR, "lending_seed_data.sql")
  with open(sql_path, "a") as f:
    f.write("\n".join(sql_append_lines))

  print(
      f"Derived analytics successfully generated & multi-format exported:\n"
      f" - Affordability Checks: {len(affordability_checks)} rows\n"
      f" - Decisions: {len(decisions)} rows\n"
      f" - Repayment Schedules: {len(repayment_schedules)} rows"
  )


if __name__ == "__main__":
  generate_derived_analytics()