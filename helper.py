import os
from dotenv import load_dotenv

def load_env():
    """Load environment variables from .env file"""
    load_dotenv()
    
    # Set Ollama as default if not configured
    if not os.getenv('OPENAI_API_BASE'):
        os.environ['OPENAI_API_BASE'] = 'http://localhost:11434/v1'
        os.environ['OPENAI_MODEL_NAME'] = 'qwen3:1.7b'
        os.environ['OPENAI_API_KEY'] = 'ollama'
        print("Ollama (qwen3:1.7b) configured successfully!")
    
    print(f" Using model: {os.getenv('OPENAI_MODEL_NAME')}")