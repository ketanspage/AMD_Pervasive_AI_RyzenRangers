Image and Video Generation with Text Overlay
This project allows you to generate images using a text prompt, overlay text on the generated images, and create a video from these images with a background music track. The project uses Hugging Face APIs for text and image generation and OpenCV and MoviePy for video processing.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.x
requests
Pillow
numpy
opencv-python
moviepy
You can install the required packages using:

bash
Copy code
pip install requests Pillow numpy opencv-python moviepy
Files
image_gen.py: Script for generating images using text prompts and overlaying text on the images.
app.py: Main script for running the entire process, from generating images to creating a video.
video.py: Script for creating a video from generated images and adding background music.
Usage
1. Generate Images and Create Video
To generate images and create a video, run the app.py script:

bash
Copy code
python app.py
You will be prompted to enter the following details:

Base prompt for image generation
Number of unique images to generate
Path to the music file
Text to overlay on the video
Folder to save generated images (default is images)
Name of the output video file
Frame rate for the video (default is 4)
2. Individual Scripts
image_gen.py
This script generates images using text prompts and overlays specified text on the images. You can run it separately if you want to generate images without creating a video.

bash
Copy code
python image_gen.py <base_prompt> <n> <text> <output_dir> <text_color>
base_prompt: The base text prompt for generating images.
n: Number of unique images to generate.
text: Text to overlay on the images.
output_dir: Directory to save the generated images (default is images).
text_color: Color of the overlay text (default is auto).
video.py
This script creates a video from images in a specified folder and adds a background music track.

bash
Copy code
python video.py <image_folder> <output_video> <music_file> <frame_rate>
image_folder: Folder containing the generated images.
output_video: Name of the output video file.
music_file: Path to the music file.
frame_rate: Frame rate for the video (default is 4).
Example
To generate 5 images based on a prompt, overlay the text "Sample Text", save them in the images folder, and create a video with the music file background.mp3, follow these steps:

Run the app.py script:
bash
Copy code
python app.py
Enter the following when prompted:
vbnet
Copy code
Enter the base prompt for image generation: A serene landscape
Enter the number of unique images to generate: 5
Enter the path to the music file: background.mp3
Enter the text to overlay on the video: Sample Text
Enter the folder to save generated images (default is 'images'): images
Enter the name of the output video file: output_video.mp4
Enter the frame rate for the video (default is 4): 4
Notes
Ensure you have a valid Hugging Face API token and update the HEADERS variable in image_gen.py with your token.
Adjust the text_position variable in video.py if you want to change the position of the overlay text on the video frames.
License
This project is licensed under the MIT License
