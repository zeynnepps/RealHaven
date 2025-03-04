import openai
import os
import time
import requests
from PIL import Image
from io import BytesIO
import pandas as pd

# Set up OpenAI API key
openai.api_key = "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"

# Create directories to store images
apartment_dir = "apartment_images"
single_family_dir = "single_family_images"

os.makedirs(apartment_dir, exist_ok=True)
os.makedirs(single_family_dir, exist_ok=True)

# Generate AI images and save as JPG
def generate_ai_image(prompt, save_path):
    try:
        # Generate AI Image
        response = openai.images.generate(
            model="dall-e-2",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        # Extract the image URL safely
        image_url = response.data[0].url if response and response.data else None

        # Validate image_url before making a request
        if not image_url:
            raise ValueError("Failed to retrieve image URL from OpenAI response.")

        # Download the image
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))

        # Convert to JPG and Save
        img = img.convert("RGB")
        img.save(save_path, "JPEG", quality=90)

        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

# Lists to store dataset entries
apartment_data = []
single_family_data = []

# Generate 251 AI-generated apartments because our dataset have this number of apartments
apartment_prompt = "A beautifully designed apartment building that looks realistic but is completely AI-generated. Modern architecture with large windows, balconies, and a welcoming entrance."

for i in range(2):
    filename = f"{apartment_dir}/apartment_{i+1}.jpg"
    image_url = generate_ai_image(apartment_prompt, filename)
    if image_url:
        apartment_data.append([f"Apartment_{i+1}", "Apartment", filename])
    time.sleep(5)

# Generate 249 AI-generated single-family homes because our dataset have this number of houses
single_family_prompt = "A beautifully designed single-family home that looks realistic but is completely AI-generated. A modern yet cozy look, with a front yard, a welcoming entrance, and large windows."

for i in range(249):
    filename = f"{single_family_dir}/single_family_{i+1}.jpg"
    image_url = generate_ai_image(single_family_prompt, filename)
    if image_url:
        single_family_data.append([f"Single_Family_{i+1}", "Single Family", filename])
    time.sleep(5)

# Create DataFrames
apartment_df = pd.DataFrame(apartment_data, columns=["Image_ID", "Property_Type", "Image_Path"])
single_family_df = pd.DataFrame(single_family_data, columns=["Image_ID", "Property_Type", "Image_Path"])

# Save datasets to CSV
apartment_df.to_csv("apartment_images_dataset.csv", index=False)
single_family_df.to_csv("single_family_images_dataset.csv", index=False)

print("Datasets created successfully!")
