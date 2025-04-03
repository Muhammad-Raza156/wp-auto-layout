import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROK_API_KEY = os.environ.get("GROK_API_KEY", "")

MODEL_NAME_GROQ = "llama3-70b-8192"
#MODEL_NAME_GEMINI = "gemini-1.5-flash"
MODEL_NAME_GEMINI="gemini-2.0-pro-exp-02-05"
GROK_MODEL_NAME = "grok-2-latest" 

