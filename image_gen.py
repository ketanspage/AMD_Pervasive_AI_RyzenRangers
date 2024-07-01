import requests
import io
import os
from PIL import Image, ImageDraw, ImageFont
import re
import cv2
import numpy as np

# Set up the API URLs and headers
IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"
TEXT_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HEADERS = {"Authorization": "Bearer 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"}

def query_image(payload):
    response = requests.post(IMAGE_API_URL, headers=HEADERS, json=payload)
    return response.content

def query_text(payload):
    response = requests.post(TEXT_API_URL, headers=HEADERS, json=payload)
    return response.json()

def trim_incomplete_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    
    if not sentences[-1].endswith(('.', '?', '!')):
        sentences = sentences[:-1]
    
    return ' '.join(sentences)

def calculate_brightness_around_position(image, position, text_width, text_height):
    grayscale = image.convert('L')
    left, top = position
    right, bottom = left + text_width, top + text_height
    cropped = grayscale.crop((left, top, right, bottom))
    histogram = cropped.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale

def calculate_edge_density(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 100, 200)
    return edges

def find_best_text_position(edge_density, text_width, text_height):
    # Define the step size for sliding window
    step_size = 10
    best_position = (0, 0)
    min_density = float('inf')

    # Slide the window across the image
    for y in range(0, edge_density.shape[0] - text_height, step_size):
        for x in range(0, edge_density.shape[1] - text_width, step_size):
            # Extract the region of interest (ROI)
            roi = edge_density[y:y + text_height, x:x + text_width]
            # Calculate the sum of edge densities in the ROI
            edge_sum = np.sum(roi)
            # Update the best position if a lower edge density is found
            if edge_sum < min_density:
                min_density = edge_sum
                best_position = (x, y)

    return best_position

def get_contrast_color(brightness, text_color):
    if text_color != "auto":
        return text_color    
    # Based on brightness, choose a color with sufficient contrast
    if 0.2<brightness <0.5 :
        return "yellow"  # For darker backgrounds, use lighter text
    elif 0.5<brightness < 0.7:
        return "gray"
    elif 0.7<brightness < 1:
        return "black"
    else:
        return "white"  # For lighter backgrounds, use darker text

def add_text_to_image(image, text, text_color, font_path="arial.ttf", initial_font_size=100):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Convert the image to OpenCV format for edge detection
    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR

    # Calculate the edge density
    edge_density = calculate_edge_density(open_cv_image)

    # Initialize font size
    font_size = initial_font_size
    text_width, text_height = 0, 0
    best_position = (0, 0)
    
    # Try different font sizes until the text fits in the image
    while font_size > 0:
        font = ImageFont.truetype(font_path, font_size)
        text_bbox = draw.textbbox((1, 1), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Find the best position for the text
        best_position = find_best_text_position(edge_density, text_width, text_height)

        # Check if the text fits within the image boundaries
        if (best_position[0] + text_width <= width) and (best_position[1] + text_height <= height):
            break
        font_size -= 5  # Decrease font size if it doesn't fit

    # Calculate brightness around the best position
    brightness = calculate_brightness_around_position(image, best_position, text_width, text_height)
    color = get_contrast_color(brightness, text_color)
    
    x, y = best_position

    # Add outline or shadow for better visibility
    draw.text((x-1, y-1), text, font=font, fill="black")
    draw.text((x+1, y-1), text, font=font, fill="black")
    draw.text((x-1, y+1), text, font=font, fill="black")
    draw.text((x+1, y+1), text, font=font, fill="black")

    # Add main text
    draw.text((x, y), text, font=font, fill=color)

def generate_images(base_prompt, n, text, output_dir="images", text_color="auto"):
    os.makedirs(output_dir, exist_ok=True)

    prompt_variations = []
    for i in range(n):
        payload = {
            "inputs": base_prompt,
            "parameters":  {"inputs": base_prompt,"num_return_sequences": i, "max_length": 200,  
        "min_length": 50, 
        "temperature": 0.7,  
        "top_p": 0.9,  
        "top_k": 50   }
        }
        response = query_text(payload)
        generated_text = response[0]["generated_text"]
        cleaned_text = trim_incomplete_sentences(generated_text)
        prompt_variations.append(cleaned_text)

    for i, prompt_variation in enumerate(prompt_variations):
        image_bytes = query_image({"inputs": prompt_variation})
        image = Image.open(io.BytesIO(image_bytes))

        add_text_to_image(image, text, text_color)

        image_path = os.path.join(output_dir, f"image_{i+1}.jpg")
        image.save(image_path, "JPEG")

        print(f"image_{i+1} saved with text: {prompt_variation}")

if __name__ == "__main__":
    import sys
    base_prompt = sys.argv[1]
    n = int(sys.argv[2])
    text = sys.argv[3]
    output_dir = sys.argv[4] if len(sys.argv) > 4 else "images"
    text_color = sys.argv[5] if len(sys.argv) > 5 else "auto"
    generate_images(base_prompt, n, text, output_dir, text_color)
