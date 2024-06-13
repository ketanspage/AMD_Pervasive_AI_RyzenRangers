import requests
import io
import os
from PIL import Image

# Set up the API URLs and headers
IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
TEXT_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HEADERS = {"Authorization": "Bearer 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"}

def query_image(payload):
    response = requests.post(IMAGE_API_URL, headers=HEADERS, json=payload)
    return response.content

def query_text(payload):
    response = requests.post(TEXT_API_URL, headers=HEADERS, json=payload)
    return response.json()

def generate_images(base_prompt, n, output_dir="images"):
    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate unique variations
    prompt_variations = []
    for i in range(n):
        payload = {"inputs": base_prompt, "max_length": 50, "num_return_sequences": i, "temperature": 0.9}
        response = query_text(payload)
        generated_text = response[0]["generated_text"]
        prompt_variations.append(generated_text)

    # Generate and save images with the unique variations
    for i, prompt_variation in enumerate(prompt_variations):
        # Query the image generation API
        image_bytes = query_image({"inputs": prompt_variation})

        # Create an image from the bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Save the image with a unique filename in the specified directory
        image_path = os.path.join(output_dir, f"image_{i+1}.jpg")
        image.save(image_path, "JPEG")

        # Confirm the file is saved
        print(f"image_{i+1} saved")

if __name__ == "__main__":
    import sys
    base_prompt = sys.argv[1]
    n = int(sys.argv[2])
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "images"
    generate_images(base_prompt, n, output_dir)
