from openai import OpenAI
from Ai_brain import API_key

client = OpenAI(api_key=API_key.key)


def generate_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Hello i am Koushik. You are my personal desktop assistant. your name "
                                          "is park"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content.strip()


