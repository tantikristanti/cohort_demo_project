#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: Generate synthetic cohort data (mirroring 01_generate_data.R)
Author: Tanti Kristanti
@2026
"""

import os
import numpy as np
import pandas as pd

# Set seed for reproducibility (matches R's set.seed(2026))
np.random.seed(2026)

# Parameters
n = 1500

# Generate data
data = pd.DataFrame({
    "participant_id": np.arange(1, n + 1),
    "age": np.round(np.random.normal(loc=30, scale=5, size=n), 0).astype(int),
    "bmi": np.round(np.random.normal(loc=24, scale=4, size=n), 1),
    "glucose": np.round(np.random.normal(loc=95, scale=15, size=n), 1),
    "air_quality_index": np.round(np.random.uniform(low=20, high=120, size=n), 0).astype(int),
    "smoking": np.random.choice(
        ["Never", "Past", "Current"], 
        size=n, 
        replace=True, 
        p=[0.6, 0.2, 0.2]
    ),
    "hypertension": np.random.binomial(n=1, p=0.2, size=n)
})

# Introduce intentional missing values (MCAR)
# R code: synthetic_data$bmi[sample(1:n, 50)] <- NA
bmi_na_indices = np.random.choice(n, size=50, replace=False)
data.loc[bmi_na_indices, "bmi"] = np.nan

glucose_na_indices = np.random.choice(n, size=30, replace=False)
data.loc[glucose_na_indices, "glucose"] = np.nan

# Ensure the raw data directory exists
os.makedirs("data/raw", exist_ok=True)

# Save to CSV
data.to_csv("data/raw/synthetic_cohort_raw_python.csv", index=False)

print("✅ Data generated successfully! Check data/raw/synthetic_cohort_raw_python.csv")
print(f"   Total participants: {n}")
print(f"   Missing BMI: {data['bmi'].isna().sum()}")
print(f"   Missing Glucose: {data['glucose'].isna().sum()}")