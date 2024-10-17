import praw
import os
from dotenv import load_dotenv
from pydub import AudioSegment
import requests
import json
import moviepy.editor as mp
import cv2
from PIL import Image, ImageDraw, ImageFont

# Load environment variables
load_dotenv()

# Set up Reddit API credentials (Replace with your values in .env)
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# Initialize Reddit API using PRAW
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def get_reddit_post_content(post_url):
    submission = reddit.submission(url=post_url)
    title = submission.title
    body = submission.selftext
    return title, body

def generate_audio(text, output_filename):
    # Eleven Labs API endpoint for TTS
    url = "https://api.elevenlabs.io/v1/text-to-speech"
    headers = {
        "Authorization": f"Bearer {ELEVENLABS_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice": "default",
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        audio_data = response.content
        with open(output_filename, 'wb') as f:
            f.write(audio_data)
        print(f"Audio saved as {output_filename}")
    else:
        print("Failed to generate audio:", response.text)

def combine_audio(audio_files, output_filename):
    combined = AudioSegment.empty()
    for audio_file in audio_files:
        audio = AudioSegment.from_file(audio_file)
        combined += audio
    combined.export(output_filename, format="mp3")
    print(f"Combined audio saved as {output_filename}")

def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    cap.release()
    print(f"{frame_count} frames extracted to {output_folder}")

def add_captions_to_frames(frames_folder, text, font_path, output_folder):
    font = ImageFont.truetype(font_path, 24)
    text_lines = text.split('. ')
    frame_files = sorted(os.listdir(frames_folder))
    
    for i, frame_file in enumerate(frame_files):
        frame_path = os.path.join(frames_folder, frame_file)
        frame = Image.open(frame_path)
        draw = ImageDraw.Draw(frame)
        text_to_draw = text_lines[i % len(text_lines)]
        draw.text((10, 10), text_to_draw, font=font, fill=(255, 255, 255))
        frame.save(os.path.join(output_folder, frame_file))
    print(f"Captions added to frames in {output_folder}")

def create_video_from_frames(frames_folder, audio_path, output_video_path):
    frame_files = sorted([os.path.join(frames_folder, f) for f in os.listdir(frames_folder) if f.endswith('.jpg')])
    clips = [mp.ImageClip(m).set_duration(0.1) for m in frame_files]
    video = mp.concatenate_videoclips(clips, method="compose")
    
    audio = mp.AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_video_path, fps=24)
    print(f"Video created at {output_video_path}")

def main():
    post_url = input("Enter the Reddit post URL: ")
    title, body = get_reddit_post_content(post_url)
    print(f"Title: {title}")
    print(f"Body: {body[:100]}...")  # Show only the first 100 characters of the body

    # Generate audio files
    generate_audio(title, "output/title_audio.mp3")
    generate_audio(body, "output/body_audio.mp3")
    
    # Combine audio files
    combine_audio(["output/title_audio.mp3", "output/body_audio.mp3"], "output/combined_audio.mp3")
    
    # Extract frames from the sample video
    extract_frames("video/sample.mp4", "frames/")
    
    # Add captions to frames
    add_captions_to_frames("frames/", body, "font/Cunia.ttf", "frames_with_captions/")
    
    # Create final video with audio
    create_video_from_frames("frames_with_captions/", "output/combined_audio.mp3", "output/final_video_with_audio.mp4")

if __name__ == "__main__":
    main()
