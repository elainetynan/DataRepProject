import requests
import json

# Fetch data from the JSON URL
url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/HEO14/JSON-stat/2.0/en"
response = requests.get(url)
data = response.json()

# Extract information from the JSON data
dataset_id = data["id"]
dataset_label = data["label"]
dataset_dimensions = data["dimension"]

# Print information about the dataset
print(f"Dataset ID: {dataset_id}")
print(f"Dataset Label: {dataset_label}")

# Print information about dimensions
for dimension, info in dataset_dimensions.items():
    print(f"\nDimension: {dimension}")
    print(f"  Label: {info['label']}")
    print(f"  Categories:")
    for category_id, category_label in info["category"]["label"].items():
        print(f"    {category_id}: {category_label}")