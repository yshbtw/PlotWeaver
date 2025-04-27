import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MODEL_NAME = "llama-3.3-70b-versatile"

# Email configuration using Resend
RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY', '')
# Validate email configuration
if not RESEND_API_KEY:
    print("Warning: Email configuration is missing. Please set RESEND_API_KEY in .env file")

GENRE_TEMPLATES = {
    "Fantasy": "In a magical realm where {context}, a hero emerges to...",
    "Science Fiction": "In a distant future where {context}, an unexpected journey begins...",
    "Mystery": "In a quiet town shrouded in secrets, {context} threatens to unravel...",
    "Romance": "Against the backdrop of {context}, two souls were about to intersect...",
    "Adventure": "Driven by an inexplicable calling, {context} set the stage for an epic quest..."
}