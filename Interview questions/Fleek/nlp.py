import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
# The client automatically reads the OPENAI_API_KEY from the environment
try:
    client = OpenAI()
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    print("Please make sure your OPENAI_API_KEY is set in your .env file.")
    exit()

def parse_search_query_with_openai(nlp_query: str) -> dict:
    """
    Takes a natural language query and uses OpenAI to extract structured search criteria.

    Args:
        nlp_query: The user's search query string.

    Returns:
        A dictionary with the extracted criteria, or an error dictionary.
    """
    # This is the "magic" part. We give the model very specific instructions.
    # We tell it what our database schema looks like and what JSON format we want back.
    system_prompt = """
    You are an expert API for parsing user search queries. Your task is to convert a natural
    language query into a structured SQL object that can be used to query a database.

    The database has products with the following fields: 'title', 'category', and 'price'.

    The SQL output MUST have the following keys:
    - "title_keywords": A list of strings containing important nouns or adjectives from the query
      that should be searched for in the product's title or description.
    - "category": A single string identifying the product category.
    - "price_constraint": An object with "operator" and "value" keys.
      - The "operator" can be one of: "<" (less than), ">" (greater than), "~" (around), or "=" (exactly).
      - The "value" is a number.
      - For qualitative terms like "cheap" or "affordable", use operator "<" and an estimated value like 200.
      - For "expensive", use ">" and an estimated value like 1000.

    RULES:
    1. If a piece of information is NOT in the query, its value in the SQL MUST be `null`.
    2. Do not include any explanations or text outside of the SQL object in your response.
    3. Be concise and extract only the most relevant information.
    """

    try:
        response = client.chat.completions.create(
            # We use a newer model that is good at following instructions and JSON mode
            model="gpt-3.5-turbo-1106", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": nlp_query}
            ],
            # This is a crucial parameter that forces the model to return valid JSON
            response_format={"type": "json_object"},
            temperature=0.1 # Lower temperature for more predictable, factual results
        )

        # The response content is a JSON string, so we parse it into a Python dict
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print(f"An error occurred with the OpenAI API call: {e}")
        return {"error": str(e)}

# --- Example Usage ---
if __name__ == "__main__":
    # Test with a few different queries to see how it works
    queries = [
        "show me some cheap noise cancelling headphones under $150",
        "laptops for students",
        "a red t-shirt around 25 dollars",
        "the new iPhone",
        "anything expensive from sony",
    ]

    for query in queries:
        print(f"--- Query: '{query}' ---")
        structured_data = parse_search_query_with_openai(query)
        print(json.dumps(structured_data, indent=2))
        print("\n")