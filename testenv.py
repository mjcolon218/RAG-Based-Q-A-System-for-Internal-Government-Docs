from dotenv import load_dotenv
import os

load_dotenv()  # Looks for .env in current dir
print("KEY FROM ENV FILE:", os.getenv("OPENAI_API_KEY"))
