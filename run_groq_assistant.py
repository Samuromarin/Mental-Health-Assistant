#!/usr/bin/env python
"""
Mental Health Assistant - Main Application

A comprehensive mental health support system that combines GroqCloud LLMs 
with RAG technology to provide specialized therapeutic assistance.

This script starts the mental health assistant using the GroqCloud API
to process user queries.

Author: Samuel Romero Marín
"""

import os
import sys
import argparse
import time
from dotenv import load_dotenv
import gradio as gr

# Add root directory to path for relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Mental Health Assistant with GroqCloud")
    parser.add_argument("--port", type=int, default=7860, help="Port for web interface")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host for web interface")
    parser.add_argument("--share", action="store_true", help="Share web interface with public link")
    parser.add_argument("--model", type=str, help="GroqCloud model to use")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    return parser.parse_args()

def verify_groq_api_key():
    """Verify that GroqCloud API key is configured"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: GroqCloud API key not found")
        print("Please configure the GROQ_API_KEY environment variable in the .env file")
        print("You can get an API key at https://console.groq.com/")
        return False
    return True

def get_gradio_version():
    """Get installed Gradio version"""
    try:
        return float(gr.__version__.split('.')[0])
    except (AttributeError, ValueError, IndexError):
        return 0  

def main():
    """Main function"""
    try:
        args = parse_args()
        
        print("🧠 Initializing Mental Health Assistant...")
        
        # Verify we have all requirements
        if not verify_groq_api_key():
            return 1
        
        # Import GroqCloud client and test connection
        from src.utils.groq_client import GroqClient
        
        try:
            client = GroqClient()
            models = client.get_available_models()
            print("✅ GroqCloud API connection verified")
            print(f"✅ Will use default model: {models[0]}")
            
            # If a model was specified, verify it exists
            if args.model and args.model not in models:
                print(f"⚠️  Model {args.model} is not available.")
                print(f"Will use default model: {models[0]}")
                args.model = models[0]
            elif args.model:
                print(f"✅ Will use model: {args.model}")
        except Exception as e:
            print(f"⚠️ Could not connect to GroqCloud: {e}")
            print("Continuing with default configuration...")
        
        # Import interface
        from src.interface import create_mental_health_interface
        
        # Create interface
        print("🚀 Starting user interface...")
        demo = create_mental_health_interface()
        
        # Show startup information
        print("\n" + "=" * 50)
        print("✨ Assistant started successfully!")
        print(f"💬 Web interface available at http://localhost:{args.port}")
        if args.share:
            print("🌐 Interface will also be available with a public link")
        print("💡 Press Ctrl+C to stop the assistant")
        print("=" * 50 + "\n")
        
        # Check Gradio version for compatibility
        gradio_version = get_gradio_version()
        
        # Activate queue compatible with version
        try:
            if gradio_version >= 3:
                # Version 3.x or higher (concurrency_count)
                try:
                    demo.queue(concurrency_count=5)
                except TypeError:
                    # Fallback if it doesn't have concurrency_count
                    demo.queue()
            else:
                # Earlier version
                demo.queue()
        except Exception as e:
            print(f"⚠️ Could not activate Gradio queue: {e}")
            print("Continuing without queue...")
        
        # Start interface
        demo.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            debug=args.debug,
            # Use show_error only if available (newer versions)
            **({"show_error": args.debug} if hasattr(gr, "__version__") and gr.__version__ >= "3.0" else {})
        )
        
        return 0
    except KeyboardInterrupt:
        print("\n👋 Stopping assistant...")
        return 0
    except Exception as e:
        print(f"❌ Error starting assistant: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())