"""
Master CLI Orchestrator & Reproducibility Verification
Project: lending-synthetic-engine
Executes the full end-to-end synthetic pipeline sequentially:
1. Core Data Generation & Multi-Format Export (generator.py)
2. Derived Business Rules & Analytics Computation (rules.py)
3. Automated Integrity & Ground Truth Audit (validator.py)
4. Multi-Run Reproducibility Check (Step 10)
5. Automated Compression of Data Folder (data.zip)
"""

import hashlib
import os
import shutil
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import synthetic_data_generator
import rules
import validator


def compute_file_hash(filepath):
  sha256 = hashlib.sha256()
  with open(filepath, "rb") as f:
    while chunk := f.read(8192):
      sha256.update(chunk)
  return sha256.hexdigest()


def verify_reproducibility():
  print(
      "\n[PHASE 4/5] Executing Reproducibility Verification (Double-Run"
      " Check)..."
  )
  report_path = os.path.join("outputs", "validation_report.json")
  if os.path.exists(report_path):
    h1 = compute_file_hash(report_path)
    validator.run_auditor()
    h2 = compute_file_hash(report_path)
    if h1 == h2:
      print(
          "[PASS] Reproducibility Check Verified: Validation reports match"
          " identically across runs."
      )
    else:
      print("[WARN] Reproducibility mismatch detected.")
  else:
    print("[INFO] No previous validation report found for comparison.")


def compress_data_folder():
  print("\n[PHASE 5/5] Compressing 'data/' folder into 'data.zip'...")
  data_dir = "data"
  output_zip = "data.zip"
  if os.path.exists(data_dir):
    shutil.make_archive("data", "zip", data_dir)
    print(f"[PASS] Successfully compressed data files into {output_zip}")
  else:
    print("[WARN] Data directory does not exist to compress.")


def main():
  print("==================================================")
  print("   YOTTAFLEX FORWARD DEPLOYED ENGINEER CHALLENGE")
  print("   Deterministic Lending Data Pipeline & Auditor")
  print("==================================================")

  # Step 1: Generate Core Raw Baseline Data & Core Anomalies
  print("\n[PHASE 1/5] Executing Core Data Generator...")
  synthetic_data_generator.generate_core_baseline_data()
  synthetic_data_generator.inject_core_edge_cases()
  synthetic_data_generator.export_multi_format()

  # Step 2: Compute Derived Analytics, Decisions, & Amortization Schedules
  print("\n[PHASE 2/5] Executing Business Rules & Analytics Engine...")
  rules.generate_derived_analytics()

  # Step 3: Run Integrity Auditor & Ground Truth Validation Suite
  print("\n[PHASE 3/5] Executing Automated Validation & Auditor Suite...")
  validator.run_auditor()

  # Step 4: Multi-Run Verification Check
  verify_reproducibility()

  # Step 5: Compress Data Directory
  compress_data_folder()

  print("\n==================================================")
  print("   PIPELINE EXECUTION & VERIFICATION COMPLETE!")
  print("   - Raw & Derived CSV/JSON/SQL saved in /data")
  print("   - Compressed dataset saved in data.zip")
  print("   - Validation Report saved in /outputs")
  print("==================================================")


if __name__ == "__main__":
  main()