
!pip install praw

!pip install opencv-python

!pip install torch transformers soundfile

def ttsp(text: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # uncomment the line below to play the audio back
    # play(response)

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

!pip install requests pydub

!pip install elevenlabs

!pip install python-dotenv

!pip install --upgrade elevenlabs

!pip install --upgrade pillow

import os
import uuid
import praw
from pydub import AudioSegment
from elevenlabs.client import ElevenLabs

# Set up the Reddit API client
reddit = praw.Reddit(
    client_id='Xz9t1Wwvp9Qnj2pRitbDAQ',
    client_secret='YxgZKGK1WFxVd9p156hUsj6CDUsh4w',
    user_agent='Deepanshutomarji'
)

# Eleven Labs API configuration
ELEVENLABS_API_KEY = "sk_48f698775dd9638258c423854347d450a0c80ab65cf1947d"

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

# Prompt the user for the Reddit post URL
post_url = input("Enter the Reddit post URL: ")

try:
    # Fetch the submission using the URL
    submission = reddit.submission(url=post_url)

    # Extract the title and body
    title = submission.title
    body = submission.selftext

    # Generate audio for title and body
    title_audio_file = ttsp(title)
    body_audio_file = ttsp(body)

    if title_audio_file and body_audio_file:
        # Combine title and body audio
        title_audio = AudioSegment.from_mp3(title_audio_file)
        body_audio = AudioSegment.from_mp3(body_audio_file)
        combined_audio = title_audio + AudioSegment.silent(duration=1000) + body_audio  # 1 second pause between title and body

        # Export the combined audio
        combined_audio_file = f"{title}.mp3"
        combined_audio.export(combined_audio_file, format="mp3")

        print("\nTitle:", title)
        print("\nBody:", body)
        print(f"\nCombined audio saved as: {combined_audio_file}")

        # Clean up individual audio files
        os.remove(title_audio_file)
        os.remove(body_audio_file)
    else:
        print("Failed to generate audio files.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

!pip install ImageMagic

!pip install moviepy
!pip install pillow
!pip install ffmpeg-python
!pip install textwrap3

"""New Code Block for specific tasks"""

from concurrent.futures import ThreadPoolExecutor
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os

# Set paths for video, font, and output
video_path = 'video/sample.mp4'
audio_path = f"{post_title}.mp3"  # Audio generated from the Reddit post title
font_path = 'font/Cunia.ttf'
output_path = 'output/final_video.mp4'

# Define Reddit post title and content
post_title = title
post_content = body

# Ensure the frames directory exists
output_frames_dir = "frames/"
os.makedirs(output_frames_dir, exist_ok=True)
print(audio_path)

import os
from IPython.display import Audio

# Set paths for video, font, and output
video_path = 'video/sample.mp4'
audio_path = f"{post_title}.mp3"  # Corrected audio path
font_path = 'font/Cunia.ttf'
output_path = 'output/final_video.mp4'

# Function to play the audio file
def play_audio(audio_file):
    if os.path.exists(audio_file):
        display(Audio(audio_file, autoplay=True))
    else:
        print(f"Audio file {audio_file} not found.")

# Call this function to play the audio
play_audio(audio_path)

def get_audio_duration(audio_path):
    audio = AudioFileClip(audio_path)
    return audio.duration  # Returns the duration in seconds

def extract_frames_matching_audio(video_path, output_dir, audio_duration):
    vidcap = cv2.VideoCapture(video_path)
    fps = 24  # Fixed frame rate
    total_frames_to_extract = int(fps * audio_duration)  # Frames matching audio duration

    count = 0
    success, image = vidcap.read()
    while success and count < total_frames_to_extract:
        cv2.imwrite(f"{output_dir}/frame_{count:05d}.png", image)
        success, image = vidcap.read()
        count += 1
    return count, fps  # Return the number of frames extracted and the FPS

# Updated captions with only up to 3 words per frame
def split_caption(post_content, max_words=3):
    words = post_content.split()
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

captions = split_caption(post_content)  # Automatically splits the content into multiple captions

# Add text to each frame (optimized)
def add_text_to_frame(img_path, text, font_path):
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)

    # Set an initial font size and adjust dynamically
    img_width, img_height = img.size
    font_size = int(img_height * 0.1)  # Set font size relative to image height (10%)

    font = ImageFont.truetype(font_path, font_size)

    # Ensure text fits within the image width by adjusting font size
    while True:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if text_width <= img_width * 0.9:  # Make sure text width fits within 90% of the frame width
            break
        font_size -= 2
        font = ImageFont.truetype(font_path, font_size)

    # Center text position
    position = ((img_width - text_width) // 2, (img_height - text_height) // 2)

    # Add text to the frame
    draw.text(position, text, font=font, fill="white", stroke_width=2, stroke_fill="black")

    # Save modified frame
    img.save(img_path)

# Add text to frames with multithreading
def add_text_to_frames(output_dir, num_frames, captions, font_path, video_height):
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(num_frames):
            img_path = f"{output_dir}/frame_{i:05d}.png"
            caption_index = min(i // (num_frames // len(captions)), len(captions) - 1)
            text = captions[caption_index]
            futures.append(executor.submit(add_text_to_frame, img_path, text, font_path, video_height))

        # Wait for all threads to complete
        for future in futures:
            future.result()  # This will raise any exceptions raised in the threads

# Add text to each frame (optimized)
def add_text_to_frame(img_path, text, font_path, original_height):
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)

    # Set an initial font size and adjust dynamically based on the original height
    img_width, img_height = img.size
    font_size = int(original_height * 0.1)  # Use original video height for font size scaling

    font = ImageFont.truetype(font_path, font_size)

    # Ensure text fits within the image width by adjusting font size
    while True:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if text_width <= img_width * 0.9:  # Make sure text width fits within 90% of the frame width
            break
        font_size -= 2
        font = ImageFont.truetype(font_path, font_size)

    # Center text position
    position = ((img_width - text_width) // 2, (img_height - text_height) // 2)

    # Add text to the frame
    draw.text(position, text, font=font, fill="white", stroke_width=2, stroke_fill="black")

    # Save modified frame
    img.save(img_path)
# Add text to frames with multithreading and original height consideration
def add_text_to_frames(output_dir, num_frames, captions, font_path, original_height):
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(num_frames):
            img_path = f"{output_dir}/frame_{i:05d}.png"
            caption_index = min(i // (num_frames // len(captions)), len(captions) - 1)
            text = captions[caption_index]
            futures.append(executor.submit(add_text_to_frame, img_path, text, font_path, original_height))

        # Wait for all threads to complete
        for future in futures:
            future.result()  # This will raise any exceptions raised in the threads

# Convert frames back to video with original resolution
def frames_to_video(output_dir, output_video_path, fps, original_width, original_height):
    frame_files = [f"{output_dir}/frame_{i:05d}.png" for i in range(len(os.listdir(output_dir)))]
    if not frame_files:
        print("No frames found in the directory.")
        return
    # Use original width and height
    video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (original_width, original_height))

    for file in frame_files:
        video.write(cv2.imread(file))
    video.release()
    print(f"Video saved as {output_video_path}")

def add_audio_to_video(video_path, audio_path, output_path):
    if not os.path.exists(video_path):
        print(f"Error: Video file {video_path} not found!")
        return
    if not os.path.exists(audio_path):
        print(f"Error: Audio file {audio_path} not found!")
        return

    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"Final video with audio saved at: {output_path}")

# Define captions from the Reddit post content
captions = [
    post_title,
    post_content[:60],  # Example splitting of post content for captions
    post_content[60:120],
    # Add more splits as needed
]

# Get the original video dimensions
original_video = VideoFileClip(video_path)
original_width, original_height = original_video.size

# Get the audio duration
audio_duration = get_audio_duration(audio_path)

# Extract frames matching the audio length
num_frames, fps = extract_frames_matching_audio(video_path, output_frames_dir, audio_duration)
print(f"Extracted {num_frames} frames from the video.")

# Add text to frames with the original video height
add_text_to_frames(output_frames_dir, num_frames, captions, font_path, original_height)

# Convert frames back to video with original resolution
frames_to_video(output_frames_dir, output_path, fps, original_width, original_height)
# Add audio to the video
final_output = "output/final_video_with_audio.mp4"
add_audio_to_video(output_path, audio_path, final_output)

print("Video processing complete!")

"""**sk_48f698775dd9638258c423854347d450a0c80ab65cf1947d**"""