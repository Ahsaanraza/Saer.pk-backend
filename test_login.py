import requests

# Your local API URL
url = "http://127.0.0.1:8000/api/token/"

# Your credentials
data = {
    "username": "rafay",
    "password": "hyd12233"
}

# Send POST request
response = requests.post(url, json=data)

# Show full response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
