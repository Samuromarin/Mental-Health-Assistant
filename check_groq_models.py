#!/usr/bin/env python
"""
Script to verify the connection with GroqCloud and list available models.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Get the API key
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: GroqCloud API key not found")
        print("Please configure the GROQ_API_KEY environment variable in the .env file")
        return 1
    
    # Endpoint to list models
    url = "https://api.groq.com/openai/v1/models"
    
    # Request headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🔄 Connecting to GroqCloud to list available models...")
    
    try:
        # Make the request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception if HTTP error
        
        # Process the response
        models_data = response.json()
        
        print("✅ Connection successful!")
        print("\n📋 Available models in your GroqCloud account:")
        
        if "data" in models_data and isinstance(models_data["data"], list):
            for model in models_data["data"]:
                model_id = model.get("id", "No ID")
                print(f"- {model_id}")
                
                # Show additional details if available
                if "created" in model:
                    created_timestamp = model["created"]
                    print(f"  • Created: {created_timestamp}")
                
                if "owned_by" in model:
                    owned_by = model["owned_by"]
                    print(f"  • Owner: {owned_by}")
                
                print("") 
            
            print("\n💡 Tip: Use exactly these model IDs in your configuration")
            print("   Update the src/config/settings.py file with these values")
        else:
            print("⚠️ Unexpected response structure. Full response:")
            print(models_data)
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to GroqCloud: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Error details: {e.response.text}")
        return 1
    
    # Test a simple chat completion request
    print("\n🔄 Testing a simple chat completion request...")
    
    try:
        # Use the first model from the list
        if "data" in models_data and models_data["data"]:
            model_id = models_data["data"][0]["id"]
            
            # Endpoint for chat completions
            chat_url = "https://api.groq.com/openai/v1/chat/completions"
            
            # Request body
            data = {
                "model": model_id,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello, how are you?"}
                ],
                "temperature": 0.7,
                "max_tokens": 50
            }
            
            print(f"Using model: {model_id}")
            
            # Make the request
            response = requests.post(chat_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()  # Raise exception if HTTP error
            
            # Process the response
            chat_response = response.json()
            
            print("✅ Chat completion request successful!")
            
            if "choices" in chat_response and len(chat_response["choices"]) > 0:
                message_content = chat_response["choices"][0]["message"]["content"]
                print(f"\nResponse: {message_content}")
            else:
                print("⚠️ Unexpected response structure. Full response:")
                print(chat_response)
        else:
            print("⚠️ No models found to test")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making chat completion request: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Error details: {e.response.text}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())