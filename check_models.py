import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the API key from your .env file
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("--- 🚨 ERROR ---")
    print("Google API key not found in your .env file.")
else:
    try:
        genai.configure(api_key=api_key)
        print("✅ Successfully connected to the API.")
        print("The following models are available for your key:")
        print("-------------------------------------------")

        model_found = False
        for m in genai.list_models():
            # We only care about models that can be used for chat/text generation
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
                model_found = True

        if not model_found:
            print("No text generation models found for this API key.")

    except Exception as e:
        print(f"--- 🚨 An error occurred ---")
        print(f"Failed to connect or list models: {e}")