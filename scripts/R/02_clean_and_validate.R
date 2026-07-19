# Purpose: Clean and validate synthetic cohort data
# Author: Tanti Kristanti
# @2026

# Load required libraries
library(tidyverse) 
library(dplyr) 
library(skimr)
library(knitr)

# Import Raw Dataset
raw <- read_csv("data/raw/synthetic_cohort_raw.csv")

# 1. Quality Report before cleaning
print("--- MISSING DATA SUMMARY ---")
raw %>% skim() # Create a data summary

# 2. Validation rules (impossible values)
raw %>%
  filter(bmi > 45 | age < 15 | glucose < 50) %>%
  summarise(impossible_records = n())
  # count() # Count for impossible values

# 3. Cleaning strategy
cleaned <- raw %>%
  mutate(
    # Impute missing BMI with median (non-random imputation)
    bmi = if_else(is.na(bmi), median(bmi, na.rm = TRUE), bmi),
    # Impute missing glucose
    glucose = if_else(is.na(glucose), median(glucose, na.rm = TRUE), glucose),
    # Cap extreme outliers
    bmi = if_else(bmi > 40, 40, bmi),
    # Derive new variable (obesity)
    obese = if_else(bmi >= 30, 1, 0),
    # Factorize smoking
    smoking = factor(smoking, levels = c("Never", "Past", "Current")) # Changes smoking from text into a categorical variable.
  ) %>%
  select(-participant_id) # Remove ID for modeling; keep in raw for traceability

# Check the results
View(cleaned)

# Show a nice HTML/PDF table of the first 10 rows
kable(head(cleaned, 10), caption = "Cleaned Cohort Data (First 10 rows)")

# 4. Save cleaned dataset for versioning
write_rds(cleaned, "data/processed/cohort_cleaned.rds")
print("--- ✅ DCLEANING COMPLETE. Missing values resolved via median imputation. ---")