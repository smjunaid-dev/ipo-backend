from flask import Flask, render_template, request
import mysql.connector
 
app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "bluestock_user",
    "password": "bluestock123",
    "database": "bluestock"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT DISTINCT company_id 
        FROM analysis 
        WHERE compounded_sales_growth LIKE '3 Years%'
        ORDER BY company_id
    """)
    companies = cursor.fetchall()

    selected_company = None
    data = None

    if request.method == "POST":
        selected_company = request.form.get("company")
        cursor.execute("""
            SELECT * FROM analysis
            WHERE company_id = %s
            AND compounded_sales_growth LIKE '3 Years%'
        """, (selected_company,))
        data = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        companies=companies,
        data=data,
        selected_company=selected_company
    )

if __name__ == "__main__":
    app.run(debug=True)
