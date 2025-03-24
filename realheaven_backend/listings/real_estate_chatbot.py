import spacy
import pandas as pd 
import numpy as np
import joblib
import os 

"""
# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_query_details(user_query):
    doc = nlp(user_query)
    filters = {}

    # Extract city name (handle multi-word cities)
    for ent in doc.ents:
        if ent.label_ == "GPE":  # GPE stands for Geo-Political Entity (e.g., cities, countries)
            filters["city"] = ent.text

    # Extract bedroom and bathroom counts
    for token in doc:
        if token.text.isdigit():
            # Check if the number is associated with "bedroom" or "bathroom"
            if "bedroom" in user_query.lower() or "bed" in user_query.lower():
                filters["bedrooms"] = int(token.text)
            elif "bathroom" in user_query.lower() or "bath" in user_query.lower():
                filters["bathrooms"] = int(token.text)

    # Extract maximum price
    for token in doc:
        if token.like_num:  # Check if the token is a number
            # Check if the token is part of a price (e.g., "$2,000,000")
            if "$" in token.text or "dollar" in token.text.lower():
                # Remove non-numeric characters (e.g., "$", ",") and convert to integer
                numeric_price = "".join([c for c in token.text if c.isdigit()])
                if numeric_price:
                    filters["max_price"] = int(numeric_price)
            # Check if the token is part of a price range (e.g., "under 2 million")
            elif "under" in [t.text.lower() for t in token.head.subtree]:
                numeric_price = "".join([c for c in token.text if c.isdigit()])
                if numeric_price:
                    filters["max_price"] = int(numeric_price)

    return filters

file_path = '/Users/skondra/Documents/RealHaven/real_estate_data_with_images_v1.csv'
df = pd.read_csv(file_path)

# Convert column names to lowercase
df.columns = df.columns.str.lower()
def search_properties(filters):
    results = df.copy()

    if "city" in filters:
        results = results[results["city"].str.contains(filters["city"], case=False, na=False)]
    if "bedrooms" in filters:
        results = results[results["bedrooms"] >= filters["bedrooms"]]
    if "bathrooms" in filters:
        results = results[results["bathrooms"] >= filters["bathrooms"]]
    if "max_price" in filters:
        results = results[results["price"] <= filters["max_price"]]

    return results.head(5).to_dict(orient="records")
"""
#######################

import spacy
from spacy.language import Language

@Language.component("remove_money_ents")
def remove_money_ents(doc):
    """Remove MONEY entities from the document."""
    doc.ents = [ent for ent in doc.ents if ent.label_ != "MONEY"]
    return doc

# Load trained models
nlp = spacy.load("/Users/skondra/Documents/RealHaven/realheaven_backend/RealHaven_Models/real_estate_nlp_model")  # Load NLP model

from xgboost import XGBRegressor

price_model = XGBRegressor()
price_model.load_model("/Users/skondra/Documents/RealHaven/realheaven_backend/RealHaven_Models/final_xgboost_model.xgb")  # Load XGBoost model


#price_model = joblib.load("/Users/skondra/Documents/RealHaven/realheaven_backend/RealHaven_Models/final_xgboost_property_price_predictor.pkl")  # Load ML model
feature_columns = joblib.load("/Users/skondra/Documents/RealHaven/realheaven_backend/RealHaven_Models/final_xgboost_features.pkl")  # Load feature names

if "remove_money_ents" not in nlp.pipe_names:
    nlp.add_pipe("remove_money_ents", last=True)
 
#print(os.path.abspath("realheaven_backend/RealHaven_Models/real_estate_nlp_model"))
# Load real estate data
file_path = "/Users/skondra/Documents/RealHaven/real_estate_data_with_images_v1.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"Dataset file not found: {file_path}")
#if not os.path.exists("final_xgboost_property_price_predictor.pkl"):
#    raise FileNotFoundError("Model file not found: final_xgboost_property_price_predictor.pkl")

df = pd.read_csv(file_path)

# Extract search filters from user query
def extract_query_details(user_query):
    doc = nlp(user_query)
    filters = {}

    # Real estate-specific keywords
    real_estate_keywords = ["apartment", "house", "bedrooms", "bathrooms", "price", "rent", "buy", "sell", "property", "listing"]

    # If no real estate-related words are found, return a default chatbot response
    if not any(word in user_query.lower() for word in real_estate_keywords):
        return {"message": "Hello! How can I assist you with real estate today?"}

   
    for ent in doc.ents:
        if ent.label_ == "CITY":
            filters["city"] = ent.text
        elif ent.label_ == "BEDROOMS":
            filters["bedrooms"] = int(ent.text)
        elif ent.label_ == "BATHROOMS":
            filters["bathrooms"] = int(ent.text)
        elif ent.label_ == "PRICE":
            filters["max_price"] = int(ent.text.replace("$", "").replace(",", ""))
    print("Extracted filters", filters)
    return filters
    
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
                sample_features[col] = 1 if col.split("_")[1] == filters.get(category.lower(), "") else 0

    # Convert to DataFrame (ensure missing columns are set to 0)
    feature_vector = pd.DataFrame([sample_features])
    feature_vector = feature_vector.reindex(columns=feature_columns, fill_value=0)  # Align columns

    # Predict price
    return price_model.predict(feature_vector)[0]


# Search properties with AI recommendation
def search_properties(filters):
    results = df.copy()
    print(results.columns)

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

    #Check if no properties match
    if results.empty:
        print("No matching properties found.")

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
   
    return {
        "filters":filters,
        "properties": results.head(5).to_dict(orient="records")
    }
