import os

from dotenv import load_dotenv

load_dotenv()

llm_config = {
    "config_list": [
        {
            "model": "llama-3.1-70b-versatile",
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": os.getenv("GROQ_API_KEY"),
            "temperature": 0.0,
            "price": [0, 0],
        }
    ]
}
