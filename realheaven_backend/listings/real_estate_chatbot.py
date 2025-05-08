import spacy
import pandas as pd
import re
import os
from fuzzywuzzy import process, fuzz
from spacy.language import Language

# --- Load Data and Model ---
file_path = "/Users/rgvmingudiya/Documents/RealHaven/data_part/real_estate_data_v3.csv"
df = pd.read_csv(file_path)
#df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Price"] = df["Price"].astype(str).str.replace(",", "").astype(float)

df["Bedrooms"] = pd.to_numeric(df["Bedrooms"], errors="coerce")
df["Bathrooms"] = pd.to_numeric(df["Bathrooms"], errors="coerce")

nlp = spacy.load("/Users/rgvmingudiya/Documents/RealHaven/realheaven_backend/RealHaven_Models/real_estate_nlp_model")
print("NLP Model loaded successfully")

@Language.component("remove_money_ents")
def remove_money_ents(doc):
    doc.ents = [ent for ent in doc.ents if ent.label_ != "MONEY"]
    return doc

if "remove_money_ents" not in nlp.pipe_names:
    nlp.add_pipe("remove_money_ents", last=True)

# --- Extract Query Filters ---
def extract_query_details(user_query):
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    if any(word in user_query.lower() for word in greetings):
        return {"message": "👋 Hello! I'm your RealHeaven assistant. Ask me about homes, prices, or neighborhoods in San Jose!"}

    try:
        doc = nlp(user_query)
        filters = {}

        for ent in doc.ents:
            if ent.label_ == "CITY":
                filters["city"] = ent.text
            elif ent.label_ == "BEDROOM":
                match = re.search(r'\d+', ent.text)
                if match:
                    filters["bedrooms"] = int(match.group())
            elif ent.label_ == "BATHROOM":
                match = re.search(r'\d+', ent.text)
                if match:
                    filters["bathrooms"] = int(match.group())
            elif ent.label_ == "PRICE":
                try:
                    price = ent.text.replace("$", "").replace(",", "")
                    if "K" in price.upper():
                        filters["max_price"] = int(float(price.replace("K", "")) * 1000)
                    elif "M" in price.upper():
                        filters["max_price"] = int(float(price.replace("M", "")) * 1e6)
                    else:
                        filters["max_price"] = int(price)
                except:
                    pass
            elif ent.label_ == "PROPERTY_TYPE":
                filters["property_type"] = ent.text.lower().rstrip("s")

        # --- Fallbacks ---
        if "bedrooms" not in filters:
            bhk_match = re.search(r'(\d+)[-\s]?BHK', user_query.upper())
            if bhk_match:
                filters["bedrooms"] = int(bhk_match.group(1))
        if "max_price" not in filters:
            fallback = re.findall(r'\$?\d{2,3}(?:,\d{3})+(?:\.\d+)?[KkMm]?|\d{5,}', user_query)
            if fallback:
                last = fallback[-1].replace("$", "").replace(",", "").lower()
                try:
                    if "k" in last:
                        filters["max_price"] = int(float(last.replace("k", "")) * 1000)
                    elif "m" in last:
                        filters["max_price"] = int(float(last.replace("m", "")) * 1e6)
                    else:
                        filters["max_price"] = int(float(last))
                except:
                    pass

        filters["city"] = "San Jose"

        if not filters or all(v is None for v in filters.values()):
            return {"message": "🤔 I couldn't understand your query. Try: '2-bedroom apartment in San Jose under $1M'"}

        return filters
    except Exception:
        return {"message": "Sorry, I had trouble understanding your query. Try rephrasing it."}

# --- Search Dataset ---
def search_properties(filters):
   # results = df.copy()
   # df["Price"] = pd.to_numeric(df["Price"], errors="coerce")  # force numeric again
    results = df.dropna(subset=["Price"]).copy()               # Drop any rows where price is invalid

    if "city" in filters:
        results = results[results["City"].str.contains(filters["city"], case=False, na=False)]
    if "bedrooms" in filters:
        results = results[results["Bedrooms"] == filters["bedrooms"]]
    if "bathrooms" in filters:
        results = results[results["Bathrooms"] >= filters["bathrooms"]]
    if "max_price" in filters:
        results = results[results["Price"] <= filters["max_price"]]
    if "property_type" in filters:
        results = results[results["Property Type"].str.lower() == filters["property_type"].lower()]

    if not results.empty:
        return {
            "filters_used": filters,
            "properties": results.head(5).to_dict(orient="records")
        }

    # --- Relax filters ---
    relaxed = df.copy()
    if "city" in filters:
        best_match, score = process.extractOne(filters["city"], df["City"].unique())
        if score > 70:
            relaxed = relaxed[relaxed["City"].str.contains(best_match, case=False, na=False)]
            filters["city"] = best_match
    if "bedrooms" in filters:
        relaxed = relaxed[relaxed["Bedrooms"] >= max(1, filters["bedrooms"] - 1)]
    if "bathrooms" in filters:
        relaxed = relaxed[relaxed["Bathrooms"] >= max(1, filters["bathrooms"] - 1)]
    if "max_price" in filters:
        relaxed = relaxed[relaxed["Price"] <= filters["max_price"] * 1.05]

    if not relaxed.empty:
        return {
            "filters_used": filters,
            "properties": relaxed.head(5).to_dict(orient="records"),
            "message": "🔎 Showing close matches based on your query."
        }

    return {"message": "❌ Sorry, no matching properties found. Try modifying your search."}

# --- Format Chatbot Response ---
def format_chatbot_response(filters, properties, message=None):
    emoji = "🏡" if properties else "😕"
    if not message:
        message = (
            f"{emoji} Here are some properties matching your search."
            if properties else
            f"{emoji} No exact match found. Try modifying your search."
        )

    return {
        "query_interpretation": filters,
        "recommendations": properties,
        "message": message
    }