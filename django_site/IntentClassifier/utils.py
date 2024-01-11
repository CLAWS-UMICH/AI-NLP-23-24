import requests
from openai import OpenAI
import json

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
            Can you take this sentence: {voice_command} and extract the tags of {tags_str} and if its not there put null.
        """
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content":"""
                    You are a helpful assistant.
                    You will give the result of my query in the following format:
                    {"tag1":"value of tag1", "tag2":"value of tag2"}
                """},
                {"role": "user", "content": prompt},
            ]
        )
        resp = response.choices[0].message.content
        json_resp = json.loads(resp)

        return json_resp


            

esc = ExternalServiceClient("")
a = esc.execute_command("geosample this rock that basalt and yellow", ["rock color", "rock type", "rock_size"])
print(a)
