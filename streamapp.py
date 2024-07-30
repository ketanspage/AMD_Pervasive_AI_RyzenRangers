import os
import subprocess
import streamlit as st

def main():
    st.title("Image and Video Generator")

    base_prompt = st.text_input("Enter the base prompt for image generation:")
    n = st.number_input("Enter the number of unique images to generate:", min_value=1, value=1)
    music_file = st.text_input("Enter the path to the music file:")
    text = st.text_input("Enter the text to overlay on the video:")
    image_folder = st.text_input("Enter the folder to save generated images (default is 'images'):", value="images")
    output_video = st.text_input("Enter the name of the output video file:", value="output.mp4")
    frame_rate = st.number_input("Enter the frame rate for the video (default is 4):", min_value=1, value=4)

    if st.button("Generate Images and Create Video"):
        # Generate images
        subprocess.run(["python", "image_gen.py", base_prompt, str(n), text, image_folder])

        # Create video from images
        subprocess.run(["python", "video.py", image_folder, output_video, music_file, str(frame_rate)])
        st.success("Video created successfully!")
        
        # Ensure the video file exists before offering download
        if os.path.exists(output_video):
            with open(output_video, "rb") as file:
                st.download_button(
                    label="Download Video",
                    data=file,
                    file_name="output.mp4",
                    mime="video/mp4"
                )

if __name__ == "__main__":
    main()
