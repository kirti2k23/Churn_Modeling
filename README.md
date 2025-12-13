# Churn Modeling

A machine learning project to predict customer churn using various classification algorithms and exploratory data analysis.

## Overview

This project focuses on building predictive models to identify customers who are likely to churn. It includes data ingestion from Kaggle, exploratory data analysis (EDA), data preprocessing, and machine learning model development using multiple algorithms.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
## Data

### Dataset

- **Source:** Kaggle (Churn_Modelling dataset)
- **Location:** `data/raw/Churn_Modelling.csv`
- **Downloaded via:** Kaggle API

To download the dataset, you'll need:
1. A Kaggle account
2. Kaggle API credentials in `~/.kaggle/kaggle.json`

## Features

- ✅ Automated data ingestion from Kaggle
- ✅ Comprehensive logging with timestamps
- ✅ Custom exception handling with detailed traceback
- ✅ Exploratory data analysis in Jupyter notebooks
- ✅ Multiple machine learning algorithms:
  - scikit-learn classifiers
  - XGBoost
  - CatBoost
- ✅ Modular project structure for scalability

## Models

The project implements various classification models for churn prediction:

- **Scikit-learn:** Logistic Regression, Random Forest, SVM, Decision Trees
- **XGBoost:** Gradient boosting implementation
- **CatBoost:** Categorical feature-focused boosting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the LICENSE file in the repository.

---

For questions or issues, please contact the author at kv.edu14@gmail.com
