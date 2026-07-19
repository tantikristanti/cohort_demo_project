# Purpose: Generate synthetic cohort data (1500 participants, 7 variables)
# Author: Tanti Kristanti
# @2026

# Load required Libraries
library(tidyverse)

set.seed(2026) # For reproducibility

# Each row represents one participant
n <- 1500

# Create a dataframe
synthetic_data <- tibble(
  participant_id = 1:n, # Unique participant identifiers
  age = round(rnorm(n, mean = 30, sd = 5), 0), # Random maternal ages using a normal distribution with a mean of 30 years and a standard deviation of 5 years
  bmi = round(rnorm(n, mean = 24, sd = 4), 1), # Random BMI values using a normal distribution with a mean of 24 kg/m² and standard deviation of 4 kg/m² 
  glucose = round(rnorm(n, mean = 95, sd = 15), 1), # Glucose measurements
  air_quality_index = round(runif(n, min = 20, max = 120), 0), # Air quality index values
  smoking = sample(c("Never", "Past", "Current"), n, replace = TRUE, prob = c(0.6, 0.2, 0.2)), # Smoking status: Never (60%), Past (20%), Current (20%)
  hypertension = rbinom(n, 1, prob = 0.2) # Binary outcome (1 = hypertension): Hypertension (20%), No hypertension (80%)
)

# Introduce intentional missing values (for validation practice)
synthetic_data$bmi[sample(1:n, 50)] <- NA # Randomly select 50 participants and changee those BMI values into missing values
synthetic_data$glucose[sample(1:n, 30)] <- NA # Randomly select 30 participant IDs with missing glucose measurements

# Save raw data as CSV
write_csv(synthetic_data, "data/raw/synthetic_cohort_raw.csv")
print("✅ Data generated successfully! Check your data/raw folder.")