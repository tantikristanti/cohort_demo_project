# Purpose: Generate tables and exploratory visualizations
# Author: Tanti Kristanti
# @2026

library(tidyverse)
library(ggplot2) 

data <- read_rds("data/processed/cohort_cleaned.rds")

# View the data
View(data)

# 1. Continuous variables summary (Overall + by Hypertension)
continuous_vars <- c("age", "bmi", "glucose", "air_quality_index")

table1_continuous <- data %>%
  group_by(hypertension) %>%
  summarise(across(all_of(continuous_vars), 
                   list(N = ~sum(!is.na(.)),
                        Mean = ~mean(., na.rm = TRUE),
                        SD = ~sd(., na.rm = TRUE),
                        Median = ~median(., na.rm = TRUE),
                        Q1 = ~quantile(., 0.25, na.rm = TRUE),
                        Q3 = ~quantile(., 0.75, na.rm = TRUE)), 
                   .names = "{col}_{fn}")) %>%
  pivot_longer(-hypertension, names_to = "Variable_Stat", values_to = "Value") %>%
  separate(Variable_Stat, into = c("Variable", "Stat"), sep = "_(?=[^_]+$)") %>%
  pivot_wider(names_from = c(hypertension, Stat), values_from = Value, names_sep = "_") %>%
  mutate(Variable = factor(Variable, levels = continuous_vars)) %>%
  arrange(Variable)

print("--- TABLE 1: CONTINUOUS VARIABLES ---")
print(table1_continuous)

# 2. Categorical variables summary
table1_categorical <- data %>%
  group_by(hypertension, smoking) %>%
  summarise(N = n(), .groups = "drop") %>%
  group_by(hypertension) %>%
  mutate(Total = sum(N), Pct = round(N / Total * 100, 1)) %>%
  ungroup() %>%
  select(hypertension, smoking, N, Pct) %>%
  pivot_wider(names_from = hypertension, values_from = c(N, Pct), names_sep = "_")

print("--- TABLE 1: CATEGORICAL VARIABLES ---")
print(table1_categorical)

# 3. Visualizations
dir.create("outputs/figures", recursive = TRUE, showWarnings = FALSE)

# Histogram of Age
p1 <- ggplot(data, aes(x = age)) +
  geom_histogram(bins = 30, fill = "steelblue", color = "white") +
  theme_minimal() +
  labs(title = "Distribution of Maternal Age", x = "Age (years)", y = "Count")
ggsave("outputs/figures/histogram_age.png", p1, width = 6, height = 4)

# Boxplot of BMI by Hypertension
p2 <- ggplot(data, aes(x = factor(hypertension), y = bmi, fill = factor(hypertension))) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "BMI by Hypertension Status", x = "Hypertension (0=No, 1=Yes)", y = "BMI (kg/m²)") +
  scale_fill_manual(values = c("lightblue", "salmon")) +
  theme(legend.position = "none")
ggsave("outputs/figures/boxplot_bmi_hypertension.png", p2, width = 6, height = 4)

# Correlation matrix
cor_data <- data %>%
  select(age, bmi, glucose, air_quality_index) %>%
  cor(use = "complete.obs")

# Save correlation matrix as a CSV
write_csv(as.data.frame(cor_data), "outputs/correlation_matrix.csv")

print("✅ Descriptive analysis complete! Check outputs/figures/ and outputs/correlation_matrix.csv")