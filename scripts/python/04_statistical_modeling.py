#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: Logistic regression and ROC curve (mirroring 04_statistical_modeling.R)
Author: Tanti Kristanti
@2026
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import roc_curve, roc_auc_score

# Load cleaned data
data = pd.read_csv("data/processed/cohort_cleaned_python.csv")

# Ensure output directories exist
os.makedirs("outputs/figures", exist_ok=True)
os.makedirs("outputs/tables", exist_ok=True)

print("=" * 50)
print("📈 STARTING STATISTICAL MODELING")
print("=" * 50)

# 1. Logistic Regression using R-style formula (mirrors R's glm)
# The C() indicates categorical variable, just like R's factor()
model = smf.glm(
    formula="hypertension ~ age + bmi + glucose + C(smoking) + air_quality_index",
    data=data,
    family=sm.families.Binomial()
).fit()

# 2. Model Summary (similar to summary(model) in R)
print("\n--- MODEL SUMMARY ---")
print(model.summary())

# 3. Extract Odds Ratios and Confidence Intervals (exponentiate coefficients)
params = model.params
conf = model.conf_int()
conf.columns = ["Lower_CI", "Upper_CI"]

odds_ratios = pd.DataFrame({
    "Variable": params.index,
    "Coef": params.values,
    "OR": np.exp(params.values),
    "Lower_CI": np.exp(conf["Lower_CI"].values),
    "Upper_CI": np.exp(conf["Upper_CI"].values),
    "P_value": model.pvalues.values
}).round(3)

print("\n--- 📊 ODDS RATIOS (Exponentiated Coefficients) ---")
print(odds_ratios)

# Save to CSV
odds_ratios.to_csv("outputs/tables/logistic_regression_ors_python.csv", index=False)
print("✅ Saved: outputs/tables/logistic_regression_ors_python.csv")

# 4. Model Performance: ROC Curve and AUC
predicted_probs = model.fittedvalues  # Same as fitted(model) in R
auc_value = roc_auc_score(data["hypertension"], predicted_probs)
fpr, tpr, _ = roc_curve(data["hypertension"], predicted_probs)

print(f"\n--- MODEL PERFORMANCE ---")
print(f"AUC (Area Under the Curve): {auc_value:.3f}")

# 5. Plot and save ROC Curve
fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(fpr, tpr, color="#2E86AB", lw=2, label=f"ROC Curve (AUC = {auc_value:.3f})")
ax.plot([0, 1], [0, 1], color="grey", linestyle="--", lw=1, label="Random Guess")
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel("False Positive Rate (1 - Specificity)")
ax.set_ylabel("True Positive Rate (Sensitivity)")
ax.set_title("ROC Curve - Logistic Regression Model", fontweight="bold")
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig("outputs/figures/roc_curve_python.png", dpi=150)
plt.close()
print("✅ Saved: outputs/figures/roc_curve_python.png")

print("\n" + "=" * 50)
print("✅ STATISTICAL MODELING COMPLETE!")
print("📂 Check outputs/figures/ for plots")
print("📂 Check outputs/tables/ for CSV reports")
print("=" * 50)