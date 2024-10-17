# RedditStoryToVideo
Here's a sample **README.md** file for your **Reddit Story to Video Generator** project, complete with a description and placeholders for images:


# Reddit Story to Video Generator

This project automates the process of converting Reddit posts into videos. It fetches the content from a given Reddit post URL, generates audio using text-to-speech (TTS), and combines it with video frames to produce a complete video. The generated videos can be used for creating YouTube content, social media posts, or other creative projects.

## Features

- Fetches the title and content of Reddit posts.
- Uses Eleven Labs' API to generate realistic audio from text.
- Converts audio and video frames into a cohesive video.
- Supports adding captions directly onto video frames.
- Includes text splitting for better readability and presentation.
- Automatically adds audio to video using `moviepy`.

## Installation

Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/reddit-story-to-video-generator.git
   cd reddit-story-to-video-generator
   ```

2. Install the required Python packages:
   ```bash
   pip install praw opencv-python torch transformers soundfile requests pydub elevenlabs python-dotenv moviepy pillow ffmpeg-python
   ```

3. Set up your **Reddit** API credentials:
   - Create a `.env` file and add your `client_id`, `client_secret`, and `user_agent`:
     ```env
     REDDIT_CLIENT_ID=your_client_id
     REDDIT_CLIENT_SECRET=your_client_secret
     REDDIT_USER_AGENT=your_user_agent
     ELEVENLABS_API_KEY=your_elevenlabs_api_key
     ```

## Usage

1. Run the script and provide the Reddit post URL when prompted:
   ```bash
   python reddit_to_video.py
   ```

2. The script will:
   - Fetch the post title and body.
   - Generate audio files for the title and body.
   - Combine the audio files into a single audio track.
   - Extract frames from a sample video and add captions.
   - Combine frames into a video with synchronized audio.

3. The output video will be saved as `output/final_video_with_audio.mp4`.

## Example

Here's an example of how the output might look:

![Example Thumbnail](images/example_thumbnail.png)
*Example of the generated video thumbnail.*

![Frame with Caption](images/frame_with_caption.png)
*A frame from the video showing a caption extracted from the Reddit post.*

## Project Structure

```plaintext
reddit-story-to-video-generator/
│
├── reddit_to_video.py            # Main script to convert Reddit posts to videos
├── .env                          # Stores API keys (not included in the repository)
├── README.md                     # Project documentation
├── video/                        # Directory containing sample video files
│   └── sample.mp4                # Sample video to use as background
├── font/                         # Directory for custom fonts
│   └── Cunia.ttf                 # Font used for captions
├── output/                       # Directory where the final video is saved
├── images/                       # Directory for README images
│   ├── example_thumbnail.png     # Thumbnail showing the output video
│   └── frame_with_caption.png    # Example frame with caption overlay
└── frames/                       # Directory for extracted frames (generated at runtime)
```

## Dependencies

- Python 3.8+
- Libraries: `praw`, `opencv-python`, `torch`, `transformers`, `soundfile`, `requests`, `pydub`, `elevenlabs`, `python-dotenv`, `moviepy`, `pillow`, `ffmpeg-python`

## Contributing

Feel free to fork this repository and submit pull requests if you want to improve the project. Make sure to adhere to the contribution guidelines and code of conduct.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, feel free to reach out at <a href="https://www.instagram.com/deepanshutomarg">Instagram</a>.

```
