#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: Clean and validate synthetic cohort data (mirroring 02_clean_and_validate.R)
Author: Tanti Kristanti
@2026
"""

import os
import pandas as pd
import numpy as np

# Read raw data
raw = pd.read_csv("data/raw/synthetic_cohort_raw_python.csv")

print("=" * 50)
print("📊 DATA QUALITY REPORT (BEFORE CLEANING)")
print("=" * 50)

# 1. Summary of missing values before cleaning
missing_before = raw.isnull().sum()
missing_pct_before = (raw.isnull().sum() / len(raw)) * 100
missing_report = pd.DataFrame({
    "Missing_N": missing_before,
    "Missing_Pct": missing_pct_before
})
print(missing_report)

# 2. Validate ranges (Data Manager mindset)
print("\n--- VALIDATION CHECKS ---")
invalid_age = raw[raw["age"] < 15]["age"].count()
invalid_bmi = raw[raw["bmi"] > 45]["bmi"].count()
invalid_glucose = raw[raw["glucose"] < 50]["glucose"].count()
print(f"❌ Age < 15: {invalid_age} rows")
print(f"❌ BMI > 45: {invalid_bmi} rows")
print(f"❌ Glucose < 50: {invalid_glucose} rows")

# 3. Cleaning pipeline (mirrors R's mutate logic)
cleaned = raw.copy()

# Impute missing BMI with median
bmi_median = cleaned["bmi"].median(skipna=True)
cleaned["bmi"] = cleaned["bmi"].fillna(bmi_median)

# Impute missing glucose with median
glucose_median = cleaned["glucose"].median(skipna=True)
cleaned["glucose"] = cleaned["glucose"].fillna(glucose_median)

# Cap extreme outliers (BMI > 40 capped to 40)
cleaned["bmi"] = np.where(cleaned["bmi"] > 40, 40, cleaned["bmi"])

# Derive new variable: obese (1 if BMI >= 30 else 0)
cleaned["obese"] = np.where(cleaned["bmi"] >= 30, 1, 0)

# Convert smoking to categorical (ordered factor in R)
smoking_order = ["Never", "Past", "Current"]
cleaned["smoking"] = pd.Categorical(
    cleaned["smoking"], 
    categories=smoking_order, 
    ordered=True
)

# Drop participant_id for modeling (keep in raw for traceability)
cleaned = cleaned.drop(columns=["participant_id"])

# Ensure processed directory exists
os.makedirs("data/processed", exist_ok=True)

# Save cleaned dataset (as CSV for interoperability, and also pickled)
cleaned.to_csv("data/processed/cohort_cleaned_python.csv", index=False)
cleaned.to_pickle("data/processed/cohort_cleaned_python.pkl")  # Alternative for Python

print("\n" + "=" * 50)
print("✅ CLEANING COMPLETE")
print("=" * 50)
print(f"   Missing values resolved via median imputation.")
print(f"   Saved: data/processed/cohort_cleaned_python.csv")