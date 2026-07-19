# Synthetic Cohort Data Analysis - R & Python Implementation

**Context:** This project uses **R** as the primary language for statistical analysis and data management, with **Python** providing complementary support for data processing and automation.

## Approach

- **R** : Used for statistical analysis, advanced data visualization (`ggplot2`), and classical biostatistical modeling (`glm`).

* **Python** : Used to replicate core workflows, enabling interoperability between the R and Python ecosystems while supporting ETL pipeline automation.

---

## Synthetic Dataset Details & Alternatives

### Why this dataset?

This project uses a **fully synthetic dataset** deliberately designed to mirror the structure and complexity of a real maternal-child health cohort.

The variables were chosen to represent a simplified **exposome** framework:

| Variable              | Description                         | Rationale                                                                                                                 |
| --------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `age`               | Maternal age (years)                | Advanced maternal age is a known risk factor for gestational hypertension and diabetes.                                   |
| `bmi`               | Body Mass Index (kg/m²)            | A core anthropometric measure; pre-pregnancy BMI is strongly associated with adverse pregnancy outcomes.                  |
| `glucose`           | Fasting blood glucose (mg/dL)       | Proxy for gestational diabetes risk, a key exposure in mother-child cohorts.                                              |
| `air_quality_index` | Environmental exposure score        | Represents the environmental component of the exposome (air pollution).                                                   |
| `smoking`           | Smoking status (Never/Past/Current) | Classic behavioral risk factor.                                                                                           |
| `hypertension`      | Binary outcome (1=Yes)              | Serves as a measurable, clinically relevant outcome (gestational hypertension) that can be linked to the other exposures. |

### Data Generation Logic

- **Continuous variables** (`age`, `bmi`, `glucose`): Generated using normal distributions (`rnorm`) with clinically plausible means and standard deviations. Outliers are intentionally capped during the cleaning phase to simulate real-world biological extremes.
- **Environmental index** (`air_quality_index`): Generated from a uniform distribution (`runif`) to simulate a wide, unpredictable environmental range.
- **Categorical variable** (`smoking`): Sampled with probabilities reflecting French population statistics (~60% never, ~20% past, ~20% current).
- **Binary outcome** (`hypertension`): Generated with a base prevalence of 20%, consistent with estimates for gestational hypertension in developed countries.
- **Missing data**: Approximately 3-5% missing values were introduced completely at random (MCAR) in `bmi` and `glucose` to test data cleaning and imputation workflows (median imputation is used).

### Alternatives for Readers

If you wish to test this project with real or alternative datasets, here are recommended options:

1. **NHANES (National Health and Nutrition Examination Survey)**:

   - A real, large-scale survey conducted by the CDC containing health, nutrition, and environmental exposure variables.
   - **R Package**: `install.packages("NHANES")` (dataset: `NHANES`)
   - This is the closest real-world equivalent to the variables used here.

   ```r
   install.packages("NHANES")
   library(NHANES)
   data(NHANES)
   ```
2. **[TidyTuesday](https://github.com/rfordatascience/tidytuesday) 2023 Week 43 - Simulated Patient Risk Profiles**:

   - A simulated dataset containing 100 patients with medical history features and predicted 1-year risk scores for 14 different health outcomes.
   - **Access**: `tidytuesdayR::tt_load(2023, week = 43)$patient_risk_profiles`
   - *Note*: While not a mother-child cohort, it is an excellent way to practice similar statistical modeling (logistic regression, ROC curves) on health data.

   ```r
    # Using the tidytuesdayR package
    library(tidytuesdayR)
    tuesdata <- tt_load(2023, week = 43)
    patient_data <- tuesdata$patient_risk_profiles

    # Or directly from GitHub
    patient_data <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-10-24/patient_risk_profiles.csv")
   ```
3. **Modify the Generation Script**:

   - You can easily adjust the `01_generate_data.R` or `01_generate_data.py` scripts to change sample sizes (`n`), distributions, or add new variables (e.g., `gestational_age`, `birth_weight`, `medication`). This is a quick way to test the pipeline's robustness.

---

## Key Data Management Actions Demonstrated

1. **Data Generation**: Simulated realistic cohort data (N=1500) with missing values (MCAR) to mimic real-world health surveys.
2. **Cleaning & Validation**: Imputation of missing continuous variables (median imputation), outlier capping (1st/99th percentile), and creation of derived variables (e.g., `obese` from BMI).
3. **Quality Control**: Automated detection of out-of-range values and inconsistent combinations (e.g., smoking status in children).
4. **Statistical Profiling**:
   - Descriptive tables (mean, SD, frequencies) stratified by outcome.
   - Logistic Regression to estimate Odds Ratios for hypertension.
   - ROC curve and AUC to evaluate model performance.
5. **Reproducibility**: All R scripts use `renv` for package versioning; all Python scripts use `requirements.txt`.

---

## File Structure

```
cohort_demo_project/
├── data/
│   ├── raw/
│   │   └── synthetic_cohort_raw.csv
│   └── processed/
│       └── cohort_cleaned.rds
├── outputs/
│   ├── figures/
│   │   ├── histogram_age.png
│   │   ├── boxplot_bmi_hypertension.png
│   │   ├── scatter_bmi_glucose.png
│   │   └── roc_curve_R.png
│   └── tables/
│       ├── table1_continuous.csv
│       ├── table1_categorical.csv
│       ├── correlation_matrix.csv
│       └── missing_data_report.csv
├── scripts/
│   ├── R/
│   │   ├── 01_generate_data.R
│   │   ├── 02_clean_and_validate.R
│   │   ├── 03_descriptive_analysis.R
│   │   └── 04_statistical_modeling.R
│   └── python/
│       ├── 01_generate_data.py
│       ├── 02_clean_and_validate.py
│       ├── 03_descriptive_analysis.py
│       └── 04_statistical_modeling.py
├── src/
│   └── helpers.R
├── README.md
├── requirements.txt          (for Python)
├── .Rprofile
└── src/
    └── helpers.R
```

---

## Running the Project

### R (Primary)

***Install Required Libraries***

The following R libraries are required for this project. You can install them individually:

```r
install.packages("tidyverse")   # Contains dplyr, ggplot2, readr, tidyr (similar to Python pandas & seaborn)
install.packages("stringi")     # Needed for installing tidyverse correctly
install.packages("skimr")       # For quick statistical summaries
install.packages("broom")       # Converts statistical model outputs into clean data frames, like .summary() in statsmodels
install.packages("pROC")        # For generating ROC curves
install.packages("Hmisc")       # For advanced descriptive statistics
install.packages("knitr")       # 
```

Alternatively, install all required libraries at once:

```r
install.packages(c("tidyverse", "stringi", "skimr", "broom", "ggplot2", "pROC", "Hmisc"))
```

***Run the R Scripts***

Execute the scripts in the following order:

```r
source("scripts/R/01_generate_data.R")
source("scripts/R/02_clean_and_validate.R")
source("scripts/R/03_descriptive_analysis.R")
source("scripts/R/04_statistical_modeling.R")
```

### Python Workflow (Complementary Implementation)

***Install Required Libraries using `pip` or `uv`***

```bash
# Create a virtual environment (recommended)
python3 -m venv venv

# Alternatively, create an environment using uv
uv venv venv

# Activate the virtual environment
source venv/bin/activate   # macOS/Linux

# Install project dependencies
pip install -r requirements.txt

# Alternatively, install dependencies with uv
uv add -r requirements.txt
```

***Execute the Python workflow scripts sequentially***

```bash
python scripts/python/01_generate_data.py
python scripts/python/02_clean_and_validate.py
python scripts/python/03_descriptive_analysis.py
python scripts/python/04_statistical_modeling.py
```

---
