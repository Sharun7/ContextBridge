"""
List available Gemini models
"""

import google.generativeai as genai
from config import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

print("\n" + "=" * 70)
print("Available Gemini Models")
print("=" * 70 + "\n")

try:
    models = genai.list_models()
    
    for model in models:
        print(f"Model: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Description: {model.description}")
        print(f"  Supported Methods: {', '.join(model.supported_generation_methods)}")
        print()
        
except Exception as e:
    print(f"Error listing models: {e}")
