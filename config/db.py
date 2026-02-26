from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB URI
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select database
db = client["SmartLoanML"]

# Select collection
loan_collection = db["loan_applications"]

print("✅ MongoDB connected successfully")
