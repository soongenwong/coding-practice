def build_sql_query(criteria: dict):
    # This is a conceptual example. Use a library like SQLAlchemy for production
    # to prevent SQL injection vulnerabilities.
    
    base_query = "SELECT ID, title, price, description, category FROM products WHERE 1=1"
    params = []
    
    # Add title/description keyword search
    if criteria.get("title_keywords"):
        for keyword in criteria["title_keywords"]:
            base_query += " AND (title ILIKE %s OR description ILIKE %s)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
    
    # Add category filter
    if criteria.get("category"):
        base_query += " AND category = %s"
        params.append(criteria["category"])
        
    # Add price filter
    price_info = criteria.get("price_constraint")
    if price_info and "operator" in price_info and "value" in price_info:
        op = price_info["operator"]
        val = price_info["value"]
        if op == "<":
            base_query += " AND price < %s"
            params.append(val)
        elif op == ">":
            base_query += " AND price > %s"
            params.append(val)
        elif op == "=":
            base_query += " AND price = %s"
            params.append(val)
        elif op == "~":
            # "Around" can be interpreted as a +/- 10-20% range
            base_query += " AND price BETWEEN %s AND %s"
            params.extend([val * 0.8, val * 1.2])

    base_query += " LIMIT 50;" # Always a good idea to limit results
    
    return base_query, params

# --- Example of using the builder function ---
test_query = "cheap headphones"
parsed_criteria = parse_search_query_with_openai(test_query)
# Expected output: {'title_keywords': None, 'category': 'headphones', 'price_constraint': {'operator': '<', 'value': 200}}

sql, query_params = build_sql_query(parsed_criteria)

print("\n--- Generated SQL ---")
print("SQL Statement:", sql)
print("Parameters:", query_params)

# In a real app, you would execute this with your DB connector
# cursor.execute(sql, tuple(query_params))