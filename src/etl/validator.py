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

print("Validator loaded successfully")

save_failures()