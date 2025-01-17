import base64
import requests
import json

def encode_audio_to_base64(file_path):
    with open(file_path, "rb") as audio_file:
        base64_audio = base64.b64encode(audio_file.read()).decode('utf-8')
    return base64_audio

def test_audio_transcription(endpoint_url, audio_file_path):
    # Encode the audio file to base64
    base64_audio = encode_audio_to_base64(audio_file_path)
    
    # Create the payload
    payload = {
        "id": "Astronaut_001",
        "type": "AUDIO",
        "use": "PUT",
        "data": {
            "base_64_audio": base64_audio,
            "text_from_VEGA": "",
            "command": [],
            "classify": True
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
    endpoint_url = "http://localhost:8000/IntentClassifier/transcription/"
    
    # Replace with the path to your test MP3 file
    audio_file_path = "./test3.mp3"
    
    test_audio_transcription(endpoint_url, audio_file_path)
