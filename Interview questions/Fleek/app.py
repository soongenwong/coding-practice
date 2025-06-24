import os
import json
import random # NEW: Import the random library
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request

# --- Setup ---
load_dotenv()
app = Flask(__name__)
try:
    client = OpenAI()
except Exception as e:
    print("Error: OpenAI client could not be initialized. Check your .env file and API key.")
    exit()

def price_distance(price, min_p, max_p):
    """Calculates distance of a price from a given min/max range."""
    if min_p and max_p and min_p <= price <= max_p:
        return 0 # Perfect match
    if max_p and price < min_p: # Case where range is e.g. 800-1000 and price is 700
        return min_p - price
    if min_p and price > max_p: # Case where range is e.g. 800-1000 and price is 1100
        return price - max_p
    if max_p and price > max_p: # Case for "under 1000" and price is 1100
        return price - max_p
    if min_p and price < min_p: # Case for "over 800" and price is 700
        return min_p - price
    return 0 # No constraints, no distance

# ==============================================================================
# UPDATED: Generate 50 fake laptops to expand our database
# ==============================================================================
def generate_fake_laptops():
    laptops = []
    brands = ["Dell", "HP", "Lenovo", "Asus", "Acer", "Razer", "MSI", "Apple"]
    models = ["Spectre", "XPS", "ThinkPad", "ZenBook", "Swift", "Blade", "Prestige", "MacBook Pro"]
    suffixes = ["Gaming", "Creator", "Ultra", "Go", "Pro", "Air", ""]
    use_cases = ["students", "professional work", "gaming", "creatives", "everyday use"]
    
    for i in range(50):
        brand = random.choice(brands)
        model = random.choice(models)
        suffix = random.choice(suffixes)
        ram = random.choice([8, 16, 32, 64])
        ssd = random.choice([256, 512, 1024, 2048])
        price = random.randint(500, 3500)
        
        laptops.append({
            "ID": 8 + i, # Start IDs after our initial products
            "title": f"{brand} {model} {suffix} 1{random.randint(3,6)}",
            "description": f"A powerful and portable {ram}GB RAM, {ssd}GB SSD laptop, perfect for {random.choice(use_cases)}.",
            "category": "laptops",
            "price": price,
            "popularity": random.randint(60, 99),
            "average_rating": round(random.uniform(3.8, 4.9), 1)
        })
    return laptops

# --- Fake In-Memory Database (now with more laptops) ---
INITIAL_PRODUCTS = [
    {"ID": 1, "title": "Carhartt WIP Active Jacket", "description": "A durable, water-repellent jacket for all seasons.", "category": "jackets", "price": 180, "popularity": 95, "average_rating": 4.8},
    {"ID": 2, "title": "Dell XPS 15 Laptop", "description": "A powerful laptop for gaming and professional work with a 4K OLED screen.", "category": "laptops", "price": 2200, "popularity": 85, "average_rating": 4.7},
    {"ID": 3, "title": "Sony WH-1000XM5 Headphones", "description": "Industry-leading noise-cancelling headphones.", "category": "headphones", "price": 399, "popularity": 98, "average_rating": 4.9},
    {"ID": 4, "title": "The North Face Apex Bionic Jacket", "description": "A windproof softshell jacket for cold weather.", "category": "jackets", "price": 149, "popularity": 90, "average_rating": 4.6},
    {"ID": 5, "title": "Apple MacBook Air M2", "description": "An incredibly thin and light laptop with amazing battery life.", "category": "laptops", "price": 1199, "popularity": 92, "average_rating": 4.8},
    {"ID": 6, "title": "Affordable Anker Soundcore Headphones", "description": "Great value headphones with decent sound.", "category": "headphones", "price": 79, "popularity": 88, "average_rating": 4.4},
    {"ID": 7, "title": "Carhartt Heavyweight T-Shirt", "description": "A classic, durable t-shirt.", "category": "t-shirts", "price": 25, "popularity": 99, "average_rating": 4.9},
]
FAKE_PRODUCTS_DB = INITIAL_PRODUCTS + generate_fake_laptops()


# --- Core Logic (OpenAI Parser is the same) ---
def parse_search_query_with_openai(nlp_query: str) -> dict:
    # This function remains unchanged
    # ... (same as before)
    system_prompt = """
    You are an expert API for parsing user search queries into a structured JSON object.
    The database has products with fields: 'title', 'category', and 'price'.
    Known categories are: "laptops", "jackets", "headphones", "t-shirts".

    The JSON output MUST have the following keys:
    - "title_keywords": A list of important nouns/adjectives for searching.
    - "category": A single string for the product category.
    - "min_price": A number for the minimum price.
    - "max_price": A number for the maximum price.
    
    RULES:
    - If the user gives a range like "between X and Y", set both min_price and max_price.
    - If the user says "under X" or "less than X", set only max_price.
    - If the user says "over X" or "more than X", set only min_price.
    - For "cheap", set max_price to 200. For "expensive", set min_price to 1000.
    - IGNORE subjective words like "best", "top", "great". Do NOT include them in title_keywords.
    - If a price or category is not mentioned, its value in the JSON MUST be `null`.
    - Respond ONLY with the JSON object.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": nlp_query}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": f"OpenAI API Error: {e}"}

# ==============================================================================
# FIXED: This function now finds the CLOSEST match if an exact match isn't found.
# ==============================================================================
def query_fake_database(criteria: dict) -> (list, str):
    """
    Finds products, prioritizing exact matches then falling back to closest price matches.
    """
    if not criteria or "error" in criteria:
        sorted_db = sorted(FAKE_PRODUCTS_DB, key=lambda p: -p['popularity'])
        return sorted_db[:5], "Here are our most popular products!"

    # --- Prepare Filters from new JSON structure ---
    stop_words = {"best", "top", "great", "find", "me"}
    category = criteria.get("category")
    min_price = criteria.get("min_price")
    max_price = criteria.get("max_price")
    keywords = [k for k in criteria.get("title_keywords", []) if k not in stop_words and k.rstrip('s') != category]

    # --- Start with a base of products (e.g., all in the right category) ---
    base_results = list(FAKE_PRODUCTS_DB)
    if category:
        base_results = [p for p in base_results if p['category'].lower() == category.lower()]
    
    # Filter by keywords
    if keywords:
        for keyword in keywords:
            base_results = [p for p in base_results if keyword.lower() in p['title'].lower() or keyword.lower() in p['description'].lower()]

    # --- Attempt 1: Find products STRICTLY within the price range ---
    strict_results = list(base_results)
    if min_price: strict_results = [p for p in strict_results if p['price'] >= min_price]
    if max_price: strict_results = [p for p in strict_results if p['price'] <= max_price]

    if strict_results:
        message = "Here are the best products matching your request:"
        sorted_results = sorted(strict_results, key=lambda p: (-p['popularity'], -p['average_rating']))
        return sorted_results[:5], message

    # --- Attempt 2: If no strict match, find the CLOSEST products by price ---
    if base_results and (min_price or max_price):
        # Sort by price distance first, then by popularity/rating to break ties
        sorted_by_closest = sorted(
            base_results,
            key=lambda p: (price_distance(p['price'], min_price, max_price), -p['popularity'], -p['average_rating'])
        )
        message = "We couldn't find items exactly in your price range, so here are the closest matches:"
        return sorted_by_closest[:5], message

    # --- Attempt 3: If there were no keywords or category, just show popular items ---
    if base_results:
        message = "Here are the most popular products based on your query:"
        sorted_results = sorted(base_results, key=lambda p: (-p['popularity'], -p['average_rating']))
        return sorted_results[:5], message

    # --- Ultimate Fallback ---
    message = "We couldn't find anything for your query, here are our overall best-sellers:"
    sorted_db = sorted(FAKE_PRODUCTS_DB, key=lambda p: -p['popularity'])
    return sorted_db[:5], message


# Also, update the main `home` route to handle the new return format
# In the `home()` function:
@app.route('/', methods=['GET', 'POST'])
def home():
    result_data = None
    if request.method == 'POST':
        user_query = request.form.get('query')
        if user_query:
            structured_data = parse_search_query_with_openai(user_query)
            
            # UPDATED: The function now returns two values
            recommended_products, search_message = query_fake_database(structured_data)
            
            best_recommendation = None
            other_recommendations = []
            if recommended_products:
                best_recommendation = recommended_products[0]
                other_recommendations = recommended_products[1:]

            sql_query, sql_params = build_sql_query_for_demo(structured_data)
            
            result_data = {
                "original_query": user_query,
                "best_recommendation": best_recommendation,
                "other_recommendations": other_recommendations,
                "search_message": search_message, # NEW: Pass the message to the template
                "structured_data": structured_data,
                "sql_query": sql_query,
                "sql_params": sql_params
            }
    return render_template('index.html', result=result_data)

# In app.py
def build_sql_query_for_demo(criteria: dict):
    if not criteria or "error" in criteria: return "Could not generate SQL.", []
    base_query = "SELECT ID, title, price, description, category FROM products"
    conditions = []; params = []
    
    # Keyword logic
    title_keywords = criteria.get("title_keywords", [])
    if title_keywords:
        for keyword in title_keywords:
            conditions.append("(title ILIKE %s OR description ILIKE %s)")
            params.extend([f"%{keyword}%", f"%{keyword}%"])

    # Category logic
    category = criteria.get("category")
    if category:
        conditions.append("category = %s")
        params.append(category)

    # UPDATED: Price logic using min/max
    min_price = criteria.get("min_price")
    max_price = criteria.get("max_price")

    if min_price is not None and max_price is not None:
        conditions.append("price BETWEEN %s AND %s")
        params.extend([min_price, max_price])
    elif min_price is not None:
        conditions.append("price >= %s")
        params.append(min_price)
    elif max_price is not None:
        conditions.append("price <= %s")
        params.append(max_price)

    # Assemble the final query
    if conditions: 
        query_string = f"{base_query} WHERE " + " AND ".join(conditions)
    else: 
        query_string = base_query
        
    query_string += " ORDER BY popularity DESC, average_rating DESC LIMIT 50;"
    return query_string, params

if __name__ == '__main__':
    app.run(debug=True)