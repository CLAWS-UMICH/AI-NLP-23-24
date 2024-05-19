import base64
import requests
import json

def encode_image_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image

def test_image_transcription(endpoint_url, image_file_path):
    # Encode the image file to base64
    base64_image = encode_image_to_base64(image_file_path)
    
    # Create the payload
    payload = {
        "id": "Astronaut_001",
        "type": "IMAGE",
        "use": "PUT",
        "data": {
            "base_64_image": base64_image,
            "text_from_VEGA": "",
            "command": []
        }
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Send the POST request
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))
    
    # Print the response
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    # Replace with the actual endpoint URL
    endpoint_url = "http://localhost:8000/CVServer/rocks/"
    
    # Replace with the path to your test image file
    image_file_path = "./rock_test.jpg"
    
    test_image_transcription(endpoint_url, image_file_path)
