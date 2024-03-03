from openai import OpenAI
import requests
from Ai_brain import API_key
from PIL import Image
import PIL

client = OpenAI(api_key=API_key.key)


def generate_image(prompt):
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    save_path = f"Images\\{prompt}.jpg"

    # Send a request to download the generated image
    image_data = requests.get(image_url).content

    # Save the image to a local file
    with open(save_path, 'wb') as file:
        file.write(image_data)
    print(f"Image saved to {save_path}")
    im1 = Image.open(f"C:\\Users\\samui\\PycharmProjects\\MyAssistant\\{save_path}")
    im1.show()

