import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()


def generate_and_download_image(prompt, filename):
    model="dall-e-2"
    size="1024x1024"
    quality="standard"
    # Generate image
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=1,
    )

    # Get image URL
    image_url = response.data[0].url
    print("Image generation response:", response)
    print("Generated image URL:", image_url)

    # Download image
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(image_response.content)
        print(f"Image downloaded successfully: {filename}")
    else:
        print(f"Failed to download image. Status code: {image_response.status_code}")
        return None

    return os.path.abspath(filename)


# Main execution
if __name__ == "__main__":
    prompt = "a white siamese cat"
    filename = "siamese_cat.png"

    saved_image_path = generate_and_download_image(prompt, filename)

    if saved_image_path:
        print(f"Image saved as: {saved_image_path}")
    else:
        print("Failed to generate and download the image.")