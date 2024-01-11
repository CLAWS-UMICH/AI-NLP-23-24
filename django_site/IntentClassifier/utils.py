import requests
from openai import OpenAI

class ExternalServiceClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.openai_client = OpenAI(api_key="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")

    def make_request(self, endpoint, data=None):
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"}
            ]
        )
        return response.choices[0].message

        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     # You might want to handle errors more gracefully
        #     raise Exception(f"Request failed with status code {response.status_code}")
    def execute_command(self, voice_command, tags):
        tags_str = ", ".join(tags)
        prompt = f"""
            Can you take this sentence: {voice_command} and extract the tags of {tags_str} and if its not there put null. Only contain tag names and values in response.
        """
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message
