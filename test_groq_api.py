#!/usr/bin/env python
"""
Script to test GroqCloud API

This script allows you to quickly test if your GroqCloud configuration works correctly,
sending a test message and displaying the response.
"""

import os
import sys
import argparse
import time
from dotenv import load_dotenv
from typing import List, Optional

# Add root directory to path for relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="GroqCloud API Test")
    parser.add_argument("--message", "-m", type=str, help="Message to send")
    parser.add_argument("--category", "-c", type=str, default="General", 
                       help="Mental health category: General, Anxiety, Depression, etc.")
    parser.add_argument("--model", type=str, help="GroqCloud model to use")
    parser.add_argument("--list-models", "-l", action="store_true", help="List available models")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Interactive mode for multiple queries")
    parser.add_argument("--temperature", "-t", type=float, default=0.7,
                       help="Temperature for generation (0.1-1.5)")
    parser.add_argument("--max-tokens", "-mt", type=int, default=500,
                       help="Maximum number of tokens in response")
    return parser.parse_args()

def get_available_categories() -> List[str]:
    """Gets available categories from configuration"""
    try:
        from src.config.settings import MENTAL_HEALTH_CATEGORIES
        return MENTAL_HEALTH_CATEGORIES
    except ImportError:
        return ["General", "Anxiety", "Depression", "Stress", "Relationships", "Self-esteem"]

def validate_category(category: str) -> str:
    """Validates that category exists or returns 'General'"""
    categories = get_available_categories()
    if category in categories:
        return category
    
    print(f"⚠️ Category '{category}' not valid. Available categories: {', '.join(categories)}")
    print("Using 'General' category by default.")
    return "General"

def interactive_mode(client, model_id: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 500):
    """Interactive mode for multiple queries"""
    categories = get_available_categories()
    
    print("\n===== INTERACTIVE MODE - MENTAL HEALTH ASSISTANT =====")
    print("Type 'exit', 'quit' or 'q' to finish")
    print("Type 'category' to change current category")
    print("Type 'model' to change current model")
    
    category = "General"
    
    while True:
        print(f"\n[Category: {category}] [Model: {model_id}]")
        message = input(">>> ")
        
        # Special commands
        if message.lower() in ["exit", "quit", "q"]:
            print("See you later!")
            break
        
        elif message.lower() in ["category"]:
            print(f"Available categories: {', '.join(categories)}")
            new_category = input("New category: ")
            if new_category in categories:
                category = new_category
                print(f"Category changed to: {category}")
            else:
                print(f"⚠️ Invalid category. Still using: {category}")
            continue
        
        elif message.lower() in ["model"]:
            models = client.get_available_models()
            print(f"Available models: {', '.join(models)}")
            new_model = input("New model: ")
            if new_model in models:
                model_id = new_model
                print(f"Model changed to: {model_id}")
            else:
                print(f"⚠️ Invalid model. Still using: {model_id}")
            continue
        
        elif not message.strip():
            continue
        
        # Send message
        print("🤔 Generating response...")
        start_time = time.time()
        
        try:
            response = client.generate_mental_health_response(
                message,
                category=category,
                model_id=model_id,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            elapsed_time = time.time() - start_time
            
            print("\n" + "=" * 80)
            print(response)
            print("=" * 80)
            print(f"⏱️  Time: {elapsed_time:.2f} seconds")
        
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function"""
    args = parse_args()
    
    try:
        # Import GroqCloud client
        from src.utils.groq_client import GroqClient
        
        # Create client
        client = GroqClient()
        
        # List models if requested
        if args.list_models:
            print("📋 Available models in GroqCloud:")
            for model_id in client.get_available_models():
                model_info = client.get_model_info(model_id)
                print(f"- {model_id}: {model_info['name']} (context: {model_info['context_length']} tokens)")
                print(f"  {model_info['description']}")
            return 0
        
        # Validate category
        category = validate_category(args.category)
        
        # Determine which model to use
        model = args.model
        if not model:
            # Use first available model
            model = client.get_available_models()[0]
        
        # Interactive mode
        if args.interactive:
            interactive_mode(client, model, args.temperature, args.max_tokens)
            return 0
        
        # Single message mode
        # If no message provided, request one
        message = args.message
        if not message:
            message = input("Write your message: ")
        
        # Show information
        print(f"🔄 Sending message to GroqCloud...")
        print(f"📝 Message: {message}")
        print(f"🧠 Model: {model}")
        print(f"📚 Category: {category}")
        print(f"🌡️ Temperature: {args.temperature}")
        print(f"🔢 Max tokens: {args.max_tokens}")
        
        # Start timer
        start_time = time.time()
        
        # Send request
        response = client.generate_mental_health_response(
            message,
            category=category,
            model_id=model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
        
        # Calculate time
        elapsed_time = time.time() - start_time
        
        # Show response
        print("\n" + "=" * 80)
        print("✅ Response received:")
        print("-" * 80)
        print(response)
        print("=" * 80)
        print(f"⏱️  Response time: {elapsed_time:.2f} seconds")
        
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())