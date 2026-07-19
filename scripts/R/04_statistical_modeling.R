# Statistics
# @2026 - Tanti Kristanti

library(tidyverse)
library(broom)
library(pROC)
library(ggplot2)

data <- read_rds("data/processed/cohort_cleaned.rds")

# View the data
View(data)

# Logistic Regression (logit)
model <- glm(hypertension ~ age + bmi + glucose + smoking + air_quality_index, 
             data = data, family = binomial)

# View the results (Odds Ratios with confidence intervals)
model_summary <- model %>%
  tidy(conf.int = TRUE, exponentiate = TRUE) %>%
  mutate(across(where(is.numeric), ~ round(., 3)))

print("--- 📊 MODEL RESULTS (Odds Ratios) ---")
print(model_summary)

# ROC Curve
roc_obj <- roc(data$hypertension, fitted(model))
auc_val <- auc(roc_obj)

dir.create("outputs/figures", recursive = TRUE, showWarnings = FALSE)

# Plot and save
ggroc(roc_obj) +
  geom_abline(slope = 1, intercept = 1, linetype = "dashed", color = "grey") +
  ggtitle(paste0("ROC Curve - AUC = ", round(auc_val, 3))) +
  theme_minimal()

# Calculate the optimal cutoff using the Youden Index
optimal <- coords(roc_obj, "best", ret = c("threshold", "specificity", "sensitivity"))
print(optimal)

ggsave("outputs/figures/roc_curve_R.png", width = 6, height = 5)

print("✅ Modeling complete! ROC Curve saved to outputs/figures/.")
