"""Test environment variables."""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("Environment variables:")
print(f"SURREAL_URL: {os.getenv('SURREAL_URL')}")
print(f"SURREAL_USER: {os.getenv('SURREAL_USER')}")
print(f"SURREAL_PASSWORD: {os.getenv('SURREAL_PASSWORD')}")
print(f"SURREAL_NAMESPACE: {os.getenv('SURREAL_NAMESPACE')}")
print(f"SURREAL_DATABASE: {os.getenv('SURREAL_DATABASE')}")
