import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    DATABASE_PATH = os.getenv('DATABASE_PATH', './database.db')
    FAQ_FILE_PATH = './data/faqs.json'