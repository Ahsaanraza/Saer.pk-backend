import requests

# Your valid access token
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNTcxOTAwLCJpYXQiOjE3NjE1NzAxMDAsImp0aSI6ImE0Yzk0Y2Y4YzUyYjQ0MzM5Y2NiYjhmODhmNWVkYzZmIiwidXNlcl9pZCI6Mn0.OB7qiuGvVsAXHhurPW9dDyVtuoi2QHENHNXLFXXS6ZY"

# API endpoint with organization parameter
url = "http://127.0.0.1:8000/api/umrah-packages/?organization=9"
headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.json())