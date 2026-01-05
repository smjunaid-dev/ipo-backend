# Step 3: Pros & Cons Logic (Single Company)

sales_growth = 14.0
profit_growth = 12.0
roe = 47.0
stock_cagr = 8.0

pros = []
cons = []

# Sales Growth
if sales_growth > 10:
    pros.append(f"Company has delivered good sales growth of {sales_growth}%")
else:
    cons.append(f"Company has delivered poor sales growth of {sales_growth}%")

# Profit Growth
if profit_growth > 10:
    pros.append(f"Company has delivered good profit growth of {profit_growth}%")
else:
    cons.append(f"Company has delivered poor profit growth of {profit_growth}%")

# ROE
if roe > 10:
    pros.append(f"Company has a strong ROE track record of {roe}%")
else:
    cons.append(f"Company has a weak ROE of {roe}%")

# Stock CAGR (optional insight)
if stock_cagr > 10:
    pros.append(f"Stock price has grown well at {stock_cagr}% CAGR")
else:
    cons.append(f"Stock price growth is weak at {stock_cagr}% CAGR")

# Limit to top 3 each
pros = pros[:3]
cons = cons[:3]

print("\nPROS:")
for p in pros:
    print("-", p)

print("\nCONS:")
for c in cons:
    print("-", c)
