import requests
import re
import time
import pandas as pd 
import mysql.connector
   
# ---------------- CONFIG ----------------
API_URL = "https://bluemutualfund.in/server/api/company.php"
API_KEY = "ghfkffu6378382826hhdjgk"

DB_CONFIG = {
    "host": "localhost",
    "user": "bluestock_user",
    "password": "bluestock123",
    "database": "bluestock"
}

COMPANY_FILE = "companies.xlsx"  # update name if needed

# ---------------- HELPERS ----------------
def extract_percentage(text):
    if not text:
        return None
    match = re.search(r"(\d+(\.\d+)?)%", text)
    return float(match.group(1)) if match else None

def get_3_years_analysis(analysis_list):
    if len(analysis_list) < 3:
        return None
    return analysis_list[2]   # safe: 3 Years entry

# ---------------- MAIN LOGIC ----------------
df = pd.read_excel(COMPANY_FILE)
company_ids = df.iloc[:, 0].dropna().unique()

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

for company_id in company_ids:
    print(f"\nProcessing {company_id}...")

    # Skip if already exists
    cursor.execute(
        "SELECT COUNT(*) FROM analysis WHERE company_id=%s AND compounded_sales_growth LIKE '3 Years%%'",
        (company_id,)
    )
    if cursor.fetchone()[0] > 0:
        print("→ Already exists. Skipping.")
        continue

    # Fetch API
    params = {"id": company_id, "api_key": API_KEY}
    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        print("→ API error. Skipping.")
        continue

    data = response.json().get("data", {})
    analysis = data.get("analysis", [])

    three_year = get_3_years_analysis(analysis)
    if not three_year:
        print("→ 3 Years data missing. Skipping.")
        continue

    # Extract metrics
    sales = extract_percentage(three_year.get("compounded_sales_growth"))
    profit = extract_percentage(three_year.get("compounded_profit_growth"))
    roe = extract_percentage(three_year.get("roe"))
    cagr = extract_percentage(three_year.get("stock_price_cagr"))

    # Build strings
    sales_str = f"3 Years: {sales}%" if sales else None
    profit_str = f"3 Years: {profit}%" if profit else None
    roe_str = f"3 Years: {roe}%" if roe else None
    cagr_str = f"3 Years: {cagr}%" if cagr else None

    # Insert
    insert_query = """
    INSERT INTO analysis
    (company_id, compounded_sales_growth, compounded_profit_growth, stock_price_cagr, roe)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        insert_query,
        (company_id, sales_str, profit_str, cagr_str, roe_str)
    )
    conn.commit()

    print("→ Inserted successfully.")
    time.sleep(1)   # polite API usage

cursor.close()
conn.close()

print("\nAll companies processed.")
