import requests
import json

# Define the URL for the endpoint you want to test
url = 'http://localhost:8000/IntentClassifier/webhook/'  # Replace with your actual endpoint URL

# Example data to send in the POST request
test_data = {
    "command": ["I want to collect soil samples"],
    "sender": "test_sender"
}

# Headers for the POST request
headers = {
    'Content-Type': 'application/json'
}

# Function to perform the test
def test_post_endpoint():
    try:
        # Send POST request
        response = requests.post(url, data=json.dumps(test_data), headers=headers)
        
        # Print the response status code
        print(f"Status Code: {response.status_code}")
        
        # Print the response JSON data
        print("Response JSON:")
        print(response.json())
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the test
test_post_endpoint()
