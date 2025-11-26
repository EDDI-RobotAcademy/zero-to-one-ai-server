from openai import APIError, Timeout
class OpenAIClient:
    def __init__(self, openai_client):
        self.openai_client = openai_client  # config에서 만든 OpenAI client

    def call_openai(self, prompt: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0
        )
        return response.choices[0].message.content