# Nike Global Pricing & Assortment Analytics

### Global Pricing and Product Assortment Strategy Analysis for Nike

![Nike Data Project](https://img.shields.io/badge/Data_Level-Professional-blue)
![Tech Stack](https://img.shields.io/badge/Stack-Python_|_SQL_|_PostgreSQL-green)
![Dataset](https://img.shields.io/badge/Rows-1.4M+-orange)

## 1. Project Overview

This project focuses on building an end-to-end data pipeline, transforming raw retail product data into strategic business insights about Nike’s global pricing and assortment operations.

**Data Scope:**

- **Scale:** 1,447,795 rows
- **Coverage:** 45 countries
- **Content:** Product metadata, local prices, sale prices, ratings, and model identifiers

## 2. Tech Stack

- **Programming Language:** Python (Pandas, NumPy, PyArrow)
- **Database:** PostgreSQL (SQLAlchemy, Psycopg2)
- **Analytics Tools:** SQL (Window Functions, CTEs, Data Profiling)
- **Security:** `python-dotenv` (Environment variable management)
- **Version Control:** Git & GitHub

## 3. ETL Pipeline Architecture

The project is divided into modular pipeline stages for scalability and maintainability:

1. **Extract & Clean (`01_extract_clean.py`)**
   - Merge dozens of raw CSV files into a unified dataset
   - Handle type casting issues and clean malformed characters
   - Store cleaned output in **Parquet** format for memory and performance optimization

2. **Feature Engineering (`02_feature_eng.py`)**
   - **Currency Conversion:** Normalize 20+ local currencies into USD using exchange rates
   - **Promotion Logic:** Classify `is_on_sale` products and compute discount percentages
   - **Current Price Standardization:** Align final transaction-ready price using `current_price_usd`

3. **Load to Database (`03_load_to_db.py`)**
   - Load processed data into PostgreSQL using chunked inserts (`chunksize=50,000`)
   - **Optimization:** Create indexes on `country_code` and `model_number` to improve query speed by up to 10x
   - **Security:** Use `.env` to securely manage database credentials

## 4. Business Insights

The project answers key strategic business questions through advanced SQL analytics:

| Analysis Area           | Key Insight                                                                                                                                                 |
| :---------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Global Pricing**      | Nike applies price discrimination across markets. Model `HV0360` shows a price gap of up to **$224 USD** between the cheapest and most expensive countries. |
| **Vietnam Market**      | In Vietnam, the **mid-range segment ($50–$120)** dominates the product assortment, accounting for nearly **50%** of all listed products.                    |
| **Regional Exclusives** | Japan (JP) and China (CN) are the two largest Asian markets for exclusive footwear models, with **1,718** and **1,357** exclusive SKUs respectively.        |
| **Inventory Overlap**   | The United Kingdom (GB) and France (FR) share over **90%** product assortment overlap, suggesting a highly centralized inventory strategy in Europe.        |

## 5. Project Structure

```text
nike/
├── pipelines/                 # Data processing scripts (Python)
│   ├── 01_extract_clean.py
│   ├── 02_feature_eng.py
│   └── 03_load_to_db.py
├── sql/                       # Analytical SQL queries
│   ├── 01_pricing_analysis.sql
│   ├── 02_promotional_strategy.sql
│   └── 03_product_assortment.sql
├── dataset/                   # Raw and processed data (ignored by Git)
├── .env                       # Environment variables (ignored by Git)
├── .gitignore                 # Ignore heavy and sensitive files
└── README.md                  # Project documentation


```

## 6. Setup

1. Clone the repository

```bash
git clone https://github.com/dtngnn/nike-global-analytics.git
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a .env file and configure your PostgreSQL connection credentials.

4. Run the scripts in the pipelines/ directory sequentially to process and load the data.

5. Open the SQL files in DBeaver (or any SQL client) to explore the analytical reports.
