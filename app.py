import os
import subprocess

def main():
    base_prompt = input("Enter the base prompt for image generation: ")
    n = int(input("Enter the number of unique images to generate: "))
    music_file = input("Enter the path to the music file: ")
    text = input("Enter the text to overlay on the video: ")
    image_folder = input("Enter the folder to save generated images (default is 'images'): ") or "images"
    output_video = input("Enter the name of the output video file: ")
    frame_rate = int(input("Enter the frame rate for the video (default is 4): "))
    # Generate images
    subprocess.run(["python", "image_gen.py", base_prompt, str(n), text, image_folder])

    # Create video from images
    subprocess.run(["python", "video.py", image_folder, output_video, music_file,str(frame_rate)])

if __name__ == "__main__":
    main()
