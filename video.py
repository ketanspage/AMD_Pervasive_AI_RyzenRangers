import cv2
import os
from moviepy.editor import VideoFileClip, AudioFileClip

#def add_text_to_frame(frame, text, position, font, font_scale, color, thickness):
#    return cv2.putText(frame, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

def images_to_video_with_music_and_text(image_folder, output_video, music_file, text, text_position, frame_rate=1):
    # Get list of images
    images = [img for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort()  # Sort images by name

    # Read the first image to get the size
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    temp_video = 'temp_video.avi'
    video = cv2.VideoWriter(temp_video, fourcc, 1, (width, height))

    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        
        # Add text to frame
        #frame = add_text_to_frame(frame, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
        
        # Repeat each frame according to frame_rate
        for _ in range(frame_rate):
            video.write(frame)

    # Release the VideoWriter object
    video.release()

    # Load the video and the audio
    video_clip = VideoFileClip(temp_video)
    audio_clip = AudioFileClip(music_file).subclip(0, video_clip.duration)

    # Set the audio to the video
    final_video = video_clip.set_audio(audio_clip)

    # Write the final video to file
    final_video.write_videofile(output_video, codec='libx264')

    # Clean up the temporary video file
    os.remove(temp_video)

    print(f"Video saved as {output_video}")

if __name__ == "__main__":
    import sys
    image_folder = sys.argv[1]
    output_video = sys.argv[2]
    music_file = sys.argv[3]
    
    text_position = (50, 250)  # Adjust position (x, y) as needed
    frame_rate = int(sys.argv[4]) if len(sys.argv) > 5 else 4
    images_to_video_with_music_and_text(image_folder, output_video, music_file,text_position, frame_rate)
