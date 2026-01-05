import requests
import json

API_URL = "https://bluemutualfund.in/server/api/company.php"
API_KEY = "ghfkffu6378382826hhdjgk"

params = {
    "id": "TCS",        # test with one company only
    "api_key": API_KEY
}

response = requests.get(API_URL, params=params)

print("Status Code:", response.status_code)

data = response.json()

print("\nRaw API Response:\n")
print(json.dumps(data, indent=2))
