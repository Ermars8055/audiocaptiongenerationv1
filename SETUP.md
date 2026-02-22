# Video to Captions - Setup Guide

## Prerequisites

You need Python 3.8+ and ffmpeg installed.

### Install ffmpeg (Mac)
```bash
brew install ffmpeg
```

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the script:**
```bash
python video_captioner.py
```

## What it does

1. 🎥 Records a 7-second video from your webcam
2. 🎵 Extracts audio from the video
3. 📝 Generates captions using OpenAI's Whisper
4. 💾 Saves everything with timestamps

## Output Files

- `video_[timestamp].mp4` - Your recorded video
- `audio_[timestamp].wav` - Extracted audio
- `captions_[timestamp].txt` - Generated captions

## Tips

- Position yourself in front of your webcam before running
- Speak clearly for better caption accuracy
- Press 'q' during recording to stop early
- First run downloads Whisper model (~141MB) - takes ~1-2 minutes

## Troubleshooting

**"ffmpeg not found"**
```bash
brew install ffmpeg
```

**Webcam not working**
- Check if your camera is connected
- Check system privacy settings (System Preferences > Security & Privacy > Camera)

**Slow first run**
- Whisper downloads a ~141MB model on first use, this is normal
