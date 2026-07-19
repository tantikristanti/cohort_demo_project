#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: Generate tables and exploratory visualizations (mirroring 03_descriptive_analysis.R)
Author: Tanti Kristanti
@2026
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set seaborn style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 100

# Load cleaned data
data = pd.read_csv("data/processed/cohort_cleaned_python.csv")

# Convert hypertension to integer to match palette keys
data["hypertension"] = data["hypertension"].astype(int)

# Ensure output directories exist
os.makedirs("outputs/figures", exist_ok=True)
os.makedirs("outputs/tables", exist_ok=True)

print("=" * 50)
print("📊 STARTING DESCRIPTIVE ANALYSIS")
print("=" * 50)

# 1. Continuous Variables Summary (Overall + by Hypertension) ----------------
continuous_vars = ["age", "bmi", "glucose", "air_quality_index"]

def continuous_summary(df, group_var=None):
    """
    Calculate descriptive statistics for continuous variables.
    Uses .agg() with a list of function names (strings) to avoid pandas version issues.
    """
    if group_var:
        # Grouped summary: apply multiple aggregations to all continuous columns
        stats = df.groupby(group_var)[continuous_vars].agg(
            ['count', 'mean', 'std', 'median', 
             lambda x: x.quantile(0.25), 
             lambda x: x.quantile(0.75)]
        )
        # Flatten the MultiIndex columns: e.g., ('age', 'mean') -> 'age_mean'
        stats.columns = [f"{col}_{stat}" for col, stat in stats.columns]
        # Reset index to bring 'hypertension' back as a column
        stats = stats.reset_index()
        # Round all numeric values
        stats = stats.round(2)
        return stats
    else:
        # Overall summary
        stats = df[continuous_vars].agg(
            ['count', 'mean', 'std', 'median', 
             lambda x: x.quantile(0.25), 
             lambda x: x.quantile(0.75)]
        )
        # Transpose so variables are rows, statistics are columns
        stats = stats.T
        # Rename columns for clarity
        stats.columns = ['N', 'Mean', 'SD', 'Median', 'Q1', 'Q3']
        stats = stats.round(2)
        return stats

# Generate the summaries
overall_continuous = continuous_summary(data)
stratified_continuous = continuous_summary(data, group_var="hypertension")

print("\n--- CONTINUOUS VARIABLES (Overall) ---")
print(overall_continuous)

print("\n--- CONTINUOUS VARIABLES (By Hypertension) ---")
print(stratified_continuous)

# 2. Categorical Variables Summary (N and %) --------------------------------
categorical_summary = (
    data.groupby(["hypertension", "smoking"])
    .size()
    .reset_index(name="N")
)
categorical_summary["Total"] = categorical_summary.groupby("hypertension")["N"].transform("sum")
categorical_summary["Pct"] = (categorical_summary["N"] / categorical_summary["Total"] * 100).round(1)

# Pivot to wide format (hypertension as columns)
categorical_pivot = categorical_summary.pivot(
    index="smoking",
    columns="hypertension",
    values=["N", "Pct"]
)
# Flatten column MultiIndex
categorical_pivot.columns = [f"{stat}_hypertension_{val}" for stat, val in categorical_pivot.columns]
categorical_pivot = categorical_pivot.round(1)

print("\n--- CATEGORICAL VARIABLES (N and %) ---")
print(categorical_pivot)

# 3. Save tables to CSV
overall_continuous.to_csv("outputs/tables/table1_continuous_overall_python.csv")
stratified_continuous.to_csv("outputs/tables/table1_continuous_stratified_python.csv", index=False)
categorical_pivot.to_csv("outputs/tables/table1_categorical_python.csv")

print("\n✅ Table 1 saved to outputs/tables/")

# 4. Exploratory Visualizations ---------------------------------------------

# 4.1 Histogram of Age
fig, ax = plt.subplots(figsize=(7, 5))
ax.hist(data["age"], bins=30, color="#2E86AB", edgecolor="white", alpha=0.9)
ax.set_title("Distribution of Maternal Age", fontweight="bold")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Count")
plt.tight_layout()
plt.savefig("outputs/figures/histogram_age_python.png", dpi=150)
plt.close()
print("✅ Saved: outputs/figures/histogram_age_python.png")

# 4.2 Boxplot of BMI by Hypertension (using seaborn for easier grouping)
fig, ax = plt.subplots(figsize=(7, 5))
sns.boxplot(x="hypertension", y="bmi", data=data, 
            #palette={0: "#A2D5C6", 1: "#E67E80"}, 
            palette=["#A2D5C6", "#E67E80"],  # List: first color = group 0, second = group 1
            flierprops=dict(marker="o", markerfacecolor="red", alpha=0.5))
ax.set_xticklabels(["No", "Yes"])
ax.set_title("BMI by Hypertension Status", fontweight="bold")
ax.set_xlabel("Hypertension")
ax.set_ylabel("BMI (kg/m²)")
plt.tight_layout()
plt.savefig("outputs/figures/boxplot_bmi_hypertension_python.png", dpi=150)
plt.close()
print("✅ Saved: outputs/figures/boxplot_bmi_hypertension_python.png")

# 4.3 Scatter plot: BMI vs Glucose, colored by Hypertension
fig, ax = plt.subplots(figsize=(7, 5))
colors = {0: "#2E86AB", 1: "#E67E80"}
for val, color in colors.items():
    subset = data[data["hypertension"] == val]
    ax.scatter(subset["bmi"], subset["glucose"], 
               alpha=0.6, s=15, color=color, label=f"Hypertension {val}")
ax.set_xlabel("BMI (kg/m²)")
ax.set_ylabel("Fasting Glucose (mg/dL)")
ax.set_title("BMI vs Glucose by Hypertension", fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig("outputs/figures/scatter_bmi_glucose_python.png", dpi=150)
plt.close()
print("✅ Saved: outputs/figures/scatter_bmi_glucose_python.png")

# 4.4 Correlation Matrix Heatmap
corr = data[continuous_vars].corr()
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, 
            square=True, linewidths=0.5, ax=ax)
ax.set_title("Correlation Matrix (Continuous Variables)", fontweight="bold")
plt.tight_layout()
plt.savefig("outputs/figures/correlation_heatmap_python.png", dpi=150)
plt.close()
print("✅ Saved: outputs/figures/correlation_heatmap_python.png")

# 4.5 Save correlation matrix as CSV
corr.to_csv("outputs/tables/correlation_matrix_python.csv")
print("✅ Saved: outputs/tables/correlation_matrix_python.csv")

# 5. Missing Data Report (Quality Check) ------------------------------------
missing_summary = data.isnull().sum().reset_index()
missing_summary.columns = ["Variable", "Missing_N"]
missing_summary["Missing_Pct"] = (missing_summary["Missing_N"] / len(data) * 100).round(2)

print("\n" + "=" * 50)
print("🔍 DATA QUALITY: Missing Values (After Cleaning)")
print("=" * 50)
print(missing_summary)

missing_summary.to_csv("outputs/tables/missing_data_report_python.csv", index=False)
print("✅ Missing data report saved to outputs/tables/missing_data_report_python.csv")

print("\n" + "=" * 50)
print("✅ DESCRIPTIVE ANALYSIS COMPLETE!")
print("📂 Check outputs/figures/ for plots")
print("📂 Check outputs/tables/ for CSV reports")
print("=" * 50)