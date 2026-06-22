import pandas as pd

validation_errors = []

def log_failure(rule_id, severity, table_name, message):
    validation_errors.append({
        "rule_id": rule_id,
        "severity": severity,
        "table_name": table_name,
        "message": message
    })

def save_failures():
    df = pd.DataFrame(validation_errors)
    df.to_csv("output/validation_failures.csv", index=False)

# DQ-01
def dq01_pk_uniqueness(df, pk_column, table_name):

    duplicates = df[df.duplicated(pk_column)]

    if not duplicates.empty:
        log_failure(
            "DQ-01",
            "CRITICAL",
            table_name,
            f"Duplicate values found in {pk_column}"
        )

# DQ-02
def dq02_company_year_unique(df, table_name):

    duplicates = df[df.duplicated(["company_id","year"])]

    if not duplicates.empty:
        log_failure(
            "DQ-02",
            "CRITICAL",
            table_name,
            "Duplicate company_id + year combinations"
        )

# DQ-03
def dq03_fk_integrity(child_df,parent_df):

    invalid = child_df[
        ~child_df["company_id"].isin(parent_df["id"])
    ]

    if not invalid.empty:
        log_failure(
            "DQ-03",
            "CRITICAL",
            "foreign_keys",
            "Invalid company references"
        )

# DQ-04 to DQ-16 placeholders

def dq04_bs_balance():
    pass

def dq05_positive_sales():
    pass

def dq06_stock_price_validation():
    pass

def dq07_net_cash_check():
    pass

def dq08_tax_rate_check():
    pass

def dq09_dividend_cap_check():
    pass

def dq10_url_validation():
    pass

def dq11_eps_sign_check():
    pass

def dq12_year_coverage_check():
    pass

def dq13_sector_mapping_check():
    pass

def dq14_duplicate_documents_check():
    pass

def dq15_stock_price_range_check():
    pass

def dq16_null_critical_fields_check():
    pass

save_failures()

print("Validation framework created successfully")