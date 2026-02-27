# Docker Setup for Video Captioner

## Prerequisites

- Docker and Docker Compose installed
- On Linux: Camera and microphone access
- On Mac/Windows: May require additional configuration

## Building and Running

### Build the Docker image:
```bash
docker-compose build
```

### Run the application:
```bash
docker-compose up
```

## Platform-Specific Setup

### macOS
On macOS, you'll need to use Docker Desktop with special configuration:

1. **Camera and Microphone Access:**
   - Edit `docker-compose.yml` to use your specific devices
   - Find your device IDs:
     ```bash
     ls -la /dev/video* /dev/audio*
     ```

2. **Alternative - Run with host network:**
   ```bash
   docker-compose up --privileged
   ```

### Linux
Camera and microphone should work out of the box, but ensure:

1. Your user is in the `video` and `audio` groups:
   ```bash
   sudo usermod -aG video,audio $USER
   ```

2. Verify device access:
   ```bash
   ls -la /dev/video0 /dev/snd
   ```

### Windows (WSL2)
1. Enable device passthrough in Docker Desktop settings
2. Update `docker-compose.yml` device paths for WSL2 compatibility

## Output Files

Generated files will be saved in the `./output` directory:
- `video_[timestamp].mp4` - Recorded video
- `audio_[timestamp].wav` - Extracted audio
- `captions_[timestamp].txt` - Generated captions

## Troubleshooting

**Camera not found:**
- Check device exists: `ls /dev/video0`
- Run container with: `docker-compose run --privileged video-captioner`

**Microphone not working:**
- Verify sound devices: `docker exec -it video-captioner arecord -l`
- Check ALSA configuration in container

**Whisper model download slow:**
- First run downloads ~141MB model to container
- Model is cached after first run

**Container exits immediately:**
- Check logs: `docker-compose logs`
- Run interactively: `docker-compose run -it video-captioner bash`

## Development

### Run with bash instead of app:
```bash
docker-compose run -it video-captioner bash
```

### View container logs:
```bash
docker-compose logs -f
```

### Stop and remove containers:
```bash
docker-compose down
```

## Performance Notes

- First run: ~1-2 minutes (Whisper model download)
- Subsequent runs: ~30-60 seconds
- GPU acceleration not configured (can be added if needed)
