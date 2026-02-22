#!/usr/bin/env python3
"""
Record a 7-second video and audio, then generate captions using Whisper.
"""

import cv2
import subprocess
import os
from pathlib import Path
import whisper
from datetime import datetime
import pyaudio
import numpy as np
import wave
import threading


def record_audio(duration=7, audio_file="audio.wav"):
    """Record audio from microphone for specified duration."""
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print(f"🎤 Recording audio for {duration} seconds...")
    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(np.frombuffer(data, dtype=np.float32))

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save audio file
    audio_data = np.concatenate(frames)
    audio_data = (audio_data * 32767).astype(np.int16)

    with wave.open(audio_file, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(audio_data.tobytes())

    print(f"✅ Audio saved: {audio_file}")
    return True


def record_video(duration=7, output_file="video_recording.mp4"):
    """Record video from webcam for specified duration."""
    import time

    print(f"🎥 Starting video recording for {duration} seconds...")
    print("Position yourself in front of the camera!")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Could not open webcam")
        return False

    # Get video properties
    fps = 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    frame_count = 0
    total_frames = duration * fps
    start_time = time.time()

    while frame_count < total_frames:
        ret, frame = cap.read()

        if not ret:
            print("❌ Error: Failed to capture frame")
            break

        # Write frame to video
        out.write(frame)

        # Print countdown to console (avoid cv2.imshow issues with threading)
        elapsed = time.time() - start_time
        remaining = int(duration - elapsed)
        if remaining > 0:
            print(f"  Recording: {remaining}s remaining...", end='\r')

        frame_count += 1

    cap.release()
    out.release()

    print(f"\n✅ Video saved: {output_file}")
    return True


def generate_captions(audio_file, output_file="captions.txt"):
    """Generate captions from audio using Whisper."""
    print(f"📝 Generating captions with Whisper (English)...")

    try:
        # Load Whisper model (base model is fast and accurate enough)
        model = whisper.load_model("base")

        # Transcribe audio with English language specified
        result = model.transcribe(audio_file, language="en")

        # Extract text
        caption_text = result["text"].strip()

        # Save to file
        with open(output_file, 'w') as f:
            f.write(caption_text)

        print(f"✅ Captions generated: {output_file}")
        print(f"\n📌 Captions:\n{caption_text}\n")

        return True
    except Exception as e:
        print(f"❌ Error generating captions: {e}")
        return False


def main():
    """Main function to run the entire pipeline."""
    print("=" * 50)
    print("🎬 Video to Captions")
    print("=" * 50)

    # Create timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_file = f"video_{timestamp}.mp4"
    audio_file = f"audio_{timestamp}.wav"
    captions_file = f"captions_{timestamp}.txt"

    # Record video and audio in parallel
    print("\n🎬 Starting recording (video + audio)...\n")

    video_thread = threading.Thread(target=record_video, args=(7, video_file))
    audio_thread = threading.Thread(target=record_audio, args=(7, audio_file))

    video_thread.start()
    audio_thread.start()

    video_thread.join()
    audio_thread.join()

    # Step 2: Generate captions
    if not generate_captions(audio_file, captions_file):
        return

    print("=" * 50)
    print("✨ All done!")
    print(f"Video: {video_file}")
    print(f"Audio: {audio_file}")
    print(f"Captions: {captions_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()
