# EyAy TTS Service
This is the tts service which accepsts REST API `/tts` post. Generated `wav` is then saved to repository🤖
# REST-TTS-Dockerfize
TTS REST API wrapper with FastAPI and Docker, for your text-to-speech needs🤖

## Installation
1. To build image, run `docker build . --tag eyay/tts-service`
1. To run image, run`docker run -d -p 7861:7861 -v ./audio:/code/audio --name tts-service eyay/tts-service`
1. Make sure to have the `-v` volume parameter to avoid redownloading models.
1. For CPU only, use `ghcr.io/coqui-ai/tts-cpu`, for GPU use `ghcr.io/coqui-ai/tts` as Dockerfile base image.
1. Go to `http://127.0.0.1:7861/api/` to check the app

## USAGE
* to convert text to speech, use the `POST` endpoint `/api/tts/`
with payload of `{message:"read this"}`. this returns the filename of the audio
* to read back converted speech, use the `GET` endpoint `/api/voice/`
with audio filename set a query params `name`  e.g. `.../api/voice?name=sample01.wav`

