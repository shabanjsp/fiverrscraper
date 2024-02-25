import os
import json
from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient('localhost', 27017)
db = client['fiverr']  # Replace 'your_database_name' with your actual database name
collection = db['fake']  # Replace 'your_collection_name' with your actual collection name

# Path to the folder containing JSON files
folder_path = 'results'

# Iterate through each JSON file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        try:
                # Load JSON data from the file
            with open(file_path, 'r', encoding='utf8') as file:
                json_data = json.load(file)
            
            # Insert the JSON data into the MongoDB collection
            collection.insert_one(json_data)
        except:
            pass

print("Upload completed.")
