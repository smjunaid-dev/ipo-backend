import mysql.connector
     
# ---- DB CONFIG ----
db_config = {
    "host": "localhost",
    "user": "bluestock_user",
    "password": "bluestock123",
    "database": "bluestock"
}


# ---- DATA TO INSERT (from Step 2 + Step 3) ----
company_id = "TCS"
compounded_sales_growth = "3 Years: 14%"
compounded_profit_growth = "3 Years: 12%"
stock_price_cagr = "3 Years: 8%"
roe = "3 Years: 47%"

# ---- CONNECT TO DB ----
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# ---- SAFE INSERT (avoid duplicates for same company + period) ----
check_query = """
SELECT COUNT(*) FROM analysis
WHERE company_id = %s AND compounded_sales_growth LIKE '3 Years%%'
"""
cursor.execute(check_query, (company_id,))
count = cursor.fetchone()[0]

if count == 0:
    insert_query = """
    INSERT INTO analysis
    (company_id, compounded_sales_growth, compounded_profit_growth, stock_price_cagr, roe)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(
        insert_query,
        (
            company_id,
            compounded_sales_growth,
            compounded_profit_growth,
            stock_price_cagr,
            roe
        )
    )
    conn.commit()
    print("Data inserted successfully.")
else:
    print("3 Years data for this company already exists. Skipping insert.")

cursor.close()
conn.close()
