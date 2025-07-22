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
        
        chat_models = []
        audio_models = []
        
        if "data" in models_data and isinstance(models_data["data"], list):
            for model in models_data["data"]:
                model_id = model.get("id", "No ID")
                
                # Separate chat models from audio models
                if "whisper" in model_id.lower():
                    audio_models.append(model)
                else:
                    chat_models.append(model)
                
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
            
            print(f"\n📊 Summary:")
            print(f"   • Chat models: {len(chat_models)}")
            print(f"   • Audio models (Whisper): {len(audio_models)}")
            
            # Check if Gemma is available
            gemma_models = [m for m in chat_models if "gemma" in m.get("id", "").lower()]
            if gemma_models:
                print(f"   • Gemma models available: {len(gemma_models)}")
                for gemma in gemma_models:
                    print(f"     - {gemma.get('id', 'Unknown')}")
            else:
                print(f"   • ⚠️  No Gemma models found in your account")
                
        else:
            print("⚠️ Unexpected response structure. Full response:")
            print(models_data)
            return 1

    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to GroqCloud: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Error details: {e.response.text}")
        return 1

    # Test a simple chat completion request with Gemma
    print("\n🔄 Testing a simple chat completion request with Gemma...")
    
    try:
        # Use Gemma directly for chat completion test
        test_model = "gemma2-9b-it"
        
        # Verify Gemma is available in the account
        if "data" in models_data:
            available_models = [m.get("id", "") for m in models_data.get("data", [])]
            if test_model not in available_models:
                print(f"⚠️ Warning: {test_model} not found in your account")
                print("Available chat models:")
                for model_id in available_models:
                    if "whisper" not in model_id.lower():
                        print(f"   - {model_id}")
                print(f"Proceeding with test anyway...")
        
        print(f"📋 Note: Using Gemma model specifically for chat test")
        print(f"Using model: {test_model}")
        
        # Endpoint for chat completions
        chat_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Request body with mental health context
        data = {
            "model": test_model,
            "messages": [
                {"role": "system", "content": "You are a helpful mental health assistant."},
                {"role": "user", "content": "Hello! Can you help me with some anxiety management techniques?"}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        # Make the request
        response = requests.post(chat_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()  # Raise exception if HTTP error
        
        # Process the response
        chat_response = response.json()
        
        print("✅ Chat completion request with Gemma successful!")
        
        if "choices" in chat_response and len(chat_response["choices"]) > 0:
            message_content = chat_response["choices"][0]["message"]["content"]
            print(f"\n📝 Gemma Response:")
            print("-" * 50)
            print(message_content)
            print("-" * 50)
            
            # Show usage stats if available
            if "usage" in chat_response:
                usage = chat_response["usage"]
                print(f"\n📊 Usage stats:")
                print(f"   • Input tokens: {usage.get('prompt_tokens', 'N/A')}")
                print(f"   • Output tokens: {usage.get('completion_tokens', 'N/A')}")
                print(f"   • Total tokens: {usage.get('total_tokens', 'N/A')}")
        else:
            print("⚠️ Unexpected response structure. Full response:")
            print(chat_response)
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making chat completion request with Gemma: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Error details: {e.response.text}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())