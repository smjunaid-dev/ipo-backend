import requests
import re

API_URL = "https://bluemutualfund.in/server/api/company.php"
API_KEY = "ghfkffu6378382826hhdjgk"

params = {
    "id": "TCS",
    "api_key": API_KEY
}

response = requests.get(API_URL, params=params)
api_response = response.json()

# CORRECT NESTED ACCESS
data = api_response.get("data", {})
analysis_data = data.get("analysis", [])

def extract_percentage(text):
    if not text:
        return None
    match = re.search(r"(\d+(\.\d+)?)%", text)
    return float(match.group(1)) if match else None

if not analysis_data:
    raise ValueError("Analysis data missing from API response")

# 3rd entry = 3 Years
three_year_data = analysis_data[2]

sales_growth = extract_percentage(three_year_data.get("compounded_sales_growth"))
profit_growth = extract_percentage(three_year_data.get("compounded_profit_growth"))
roe = extract_percentage(three_year_data.get("roe"))
stock_cagr = extract_percentage(three_year_data.get("stock_price_cagr"))

print("\nCleaned Metrics (3 Years):\n")
print("Sales Growth:", sales_growth, "%")
print("Profit Growth:", profit_growth, "%")
print("ROE:", roe, "%")
print("Stock Price CAGR:", stock_cagr, "%")
