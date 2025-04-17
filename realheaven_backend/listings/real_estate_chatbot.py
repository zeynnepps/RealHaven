import spacy
import pandas as pd 
import numpy as np
import joblib
import os 
import re
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from spacy.language import Language
from xgboost import XGBRegressor

# Load real estate data
file_path = "/Users/akhilkumar/Desktop/MSCS-SEM4/capstone course/RealHaven/real_estate_data_with_images_v1.csv"
df = pd.read_csv(file_path)

# Load trained models
nlp = spacy.load("/Users/akhilkumar/Desktop/MSCS-SEM4/capstone course/RealHaven/realheaven_backend/RealHaven_Models/real_estate_nlp_model")  # Load NLP model

@Language.component("remove_money_ents")
def remove_money_ents(doc):
    """Remove MONEY entities from the document."""
    doc.ents = [ent for ent in doc.ents if ent.label_ != "MONEY"]
    return doc

if "remove_money_ents" not in nlp.pipe_names:
    nlp.add_pipe("remove_money_ents", last=True)

# Extract search filters from user query
def extract_query_details(user_query):
   
    # Handle small talk & greetings
    greetings = ["hi", "hello", "hey", "hola", "merhaba", "namaste", "good morning", "good evening", "how are you", "what's up", "howdy"]
    if any(phrase in user_query.lower() for phrase in greetings):
        return {"message": "👋 Hello! I'm your RealHeaven assistant. Ask me about homes, prices, or neighborhoods in San Jose!"}

    try:
        doc = nlp(user_query)
        print("🧠 Extracted Entities:", [(ent.text, ent.label_) for ent in doc.ents])
        filters = {}

        # Real estate-specific keywords
        real_estate_keywords = ["apartment", "house", "bedroom", "bathroom", "price", "rent", "buy", "sell", "property", "listing",
                                "villa", "townhouse", "duplex", "condo", "downtown", "neighborhood", "valley", "glen", "district", "flat", "bungalow", "luxury"]
        
        if not any(word in user_query.lower() for word in real_estate_keywords):
            return {"message": "Hello! How can I assist you with real estate today?"}

        # --- Extract from NER ---
        for ent in doc.ents:
            if ent.label_ == "CITY":
                filters["city"] = ent.text
            elif ent.label_ == "BEDROOM":
                print("🛏️ BEDROOM RAW TEXT:", ent.text)
                match = re.search(r'\d+', ent.text)
                if match:
                    filters["bedrooms"] = int(match.group())
            elif ent.label_ == "BATHROOM":
                print("🛁 BATHROOM RAW TEXT:", ent.text)
                match = re.search(r'\d+', ent.text)
                if match:
                    filters["bathrooms"] = int(match.group())
            elif ent.label_ == "PRICE":
                try:
                    filters["max_price"] = int(ent.text.replace("$", "").replace(",", "").replace("M", "000000").replace("K", "000"))
                except:
                    pass
            elif ent.label_ == "PROPERTY_TYPE":
                filters["property_type"] = ent.text.lower().rstrip("s")  # Normalize plural types

        # --- Fallback for BHK like "2BHK", "3-BHK", etc. ---
        if "bedrooms" not in filters:
            bhk_match = re.search(r'(\d+)[-\s]?BHK', user_query.upper())
            if bhk_match:
                filters["bedrooms"] = int(bhk_match.group(1))
                print(f"📦 Fallback BHK extracted: {filters['bedrooms']}")

        # --- Fallback for price using regex ---
        # 💡 Improved fallback price detection that avoids small unrelated digits
        if "max_price" not in filters:
            # Try to extract numbers like $850000, 1.5M, 2M, 3000000 etc.
            price_match = re.findall(r'\$?\d{2,3}(?:,\d{3})+(?:\.\d+)?[KkMm]?|\d{5,}', user_query)

            if price_match:
                best_price = price_match[-1]  # Choose the last plausible price-like value
                print(f"💰 Raw Fallback Price Found: {best_price}")

                best_price = best_price.lower().replace("$", "").replace(",", "")
                try:
                    if "k" in best_price:
                        filters["max_price"] = int(float(best_price.replace("k", "")) * 1000)
                    elif "m" in best_price:
                        filters["max_price"] = int(float(best_price.replace("m", "")) * 1000000)
                    else:
                        filters["max_price"] = int(float(best_price))
                except Exception as e:
                    print("⚠️ Failed to parse fallback price:", e)

        """
        if "max_price" not in filters:
            price_match = re.search(r'\$?[\d,.]+[KkMm]?|\d{5,}', user_query)
            if price_match:
                price_text = price_match.group()
                numeric_price = price_text.lower().replace("$", "").replace(",", "")
                if "k" in numeric_price:
                    filters["max_price"] = int(float(numeric_price.replace("k", "")) * 1000)
                elif "m" in numeric_price:
                    filters["max_price"] = int(float(numeric_price.replace("m", "")) * 1000000)
                else:
                    filters["max_price"] = int(numeric_price)
        """
        # --- Default fallback city ---
        filters["city"] = "San Jose"

        # --- Normalize property type to singular ---
        if "property_type" in filters:
            filters["property_type"] = filters["property_type"].lower().rstrip("s")

        # Fallback message
        if not filters or all(v is None for v in filters.values()):
            return {
                "message": "🤔 I'm having trouble understanding your query. Try something like: '2-bedroom apartment in San Jose under $1M'"
            }

        print("✅ Final Parsed Filters:", filters)
        return filters

    except Exception as e:
        print(f"[NER Error] Failed to extract query details: {e}")
        return {"message": "Sorry, I couldn't understand your query. Could you try rephrasing it?"}

##############################

"""
price_model = XGBRegressor()
price_model.load_model("/Users/rgvmingudiya/Documents/RealHaven/realheaven_backend/RealHaven_Models/final_xgboost_model.xgb")  # Load XGBoost model

#price_model = joblib.load("/Users/skondra/Documents/RealHaven/realheaven_backend/RealHaven_Models/final_xgboost_property_price_predictor.pkl")  # Load ML model
feature_columns = joblib.load("/Users/rgvmingudiya/Documents/RealHaven/realheaven_backend/RealHaven_Models/final_xgboost_features.pkl")  # Load feature names

#print(os.path.abspath("realheaven_backend/RealHaven_Models/real_estate_nlp_model"))

if not os.path.exists(file_path):
    raise FileNotFoundError(f"Dataset file not found: {file_path}")
#if not os.path.exists("final_xgboost_property_price_predictor.pkl"):
#    raise FileNotFoundError("Model file not found: final_xgboost_property_price_predictor.pkl")



# Predict price using ML model
def predict_price(filters):
    # Ensure all required numerical features exist
    sample_features = {
        "Bedrooms": filters.get("bedrooms", 3),
        "Bathrooms": filters.get("bathrooms", 2),
        "Square Footage": filters.get("square_footage", 1500),  # Default value
    }

    # Feature engineering
    sample_features["Bedrooms x Bathrooms"] = sample_features["Bedrooms"] * sample_features["Bathrooms"]
    sample_features["Price per Sqft"] = 0  # Placeholder, used in training

    # One-hot encode categorical features
    categorical_features = ["City", "Property Type", "State"]
    for category in categorical_features:
        for col in feature_columns:  # Ensure alignment with trained columns
            if col.startswith(category + "_"):
                val = filters.get(category.lower().replace(" ", "_"), "")  # Normalize key
                col_value = col.split("_", 1)[1]
                sample_features[col] = 1 if col_value.lower() == val.lower() else 0

    # Convert to DataFrame (ensure missing columns are set to 0)
    feature_vector = pd.DataFrame([sample_features])
    feature_vector = feature_vector.reindex(columns=feature_columns, fill_value=0)  # Align columns

    # Predict price
    return price_model.predict(feature_vector)[0]

"""
# Search properties with AI recommendation
def search_properties(filters):
    results = df.copy()
    original_filters = filters.copy()
    #print(results.columns)

    #Apply filters
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

      # --- Return if matching results found ---
    if not results.empty:
        return {
            "filters_used": original_filters,
            "properties": results.head(5).to_dict(orient="records")
        }
    else:
         print("🚫 No exact matches found with current filters")

    # --- Relax filters ---
    relaxed_results = df.copy()
    print("Relaxing filters to find approximate matches...")

    if "city" in filters:
        city_matches = df["City"].dropna().unique()
        best_city = None
        best_score = 0
        for city in city_matches:
            score = fuzz.partial_ratio(city.lower(), filters["city"].lower())
            if score > best_score:
                best_score = score
                best_city = city
        if best_score > 70:
            relaxed_results = relaxed_results[relaxed_results["City"].str.contains(best_city, case=False, na=False)]
            filters["city"] = best_city

    if "bedrooms" in filters:
        relaxed_results = relaxed_results[relaxed_results["Bedrooms"] >= max(1, filters["bedrooms"] - 1)]

    if "bathrooms" in filters:
        relaxed_results = relaxed_results[relaxed_results["Bathrooms"] >= max(1, filters["bathrooms"] - 1)]

    if "max_price" in filters:
        relaxed_results = relaxed_results[relaxed_results["Price"] <= filters["max_price"] * 1.05]

    if not relaxed_results.empty:
        return {
            "filters_used": filters,
            "properties": relaxed_results.head(5).to_dict(orient="records"),
            "message": "Showing close matches based on your preferences."
        }

"""
    # --- Fallback: Predict price using model ---
    if "bedrooms" in filters or "bathrooms" in filters:
        try:
            predicted = predict_price(filters)
            return {
                "message": f"No properties found. Based on our prediction model, a property with your requirements may cost around ${predicted:,.0f}"
            }
        except Exception as e:
            print("Prediction failed:", e)

    return {
        "message": "Sorry, no matching properties were found. Try modifying your search."
    }

    # Recommend price if no properties match
    if "city" in filters:
            sample_features = [
                filters.get("bedrooms", 3), 
                filters.get("bathrooms", 2), 
                1500  # Default sqft
                ]
            predicted_price = predict_price(sample_features)
            return {
                "message": f"No exact match. Predicted price: ${predicted_price:.2f}"}
"""   


def format_chatbot_response(filters, properties, message=None):
    emoji = "🏡" if properties else "😕"
    if not message:
        message = (
            f"{emoji} Here are some properties matching your search."
            if properties else
            f"{emoji} No exact match found. Try modifying your search."
        )

    response = {
        "query_interpretation": filters,
        "recommendations": properties,
        "message": message,
    }
    return response