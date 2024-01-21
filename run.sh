docker build . --tag eyay/tts-service
docker run -d -p 7861:7861 -p 11434:11434 -v ./audio:/code/audio -v ./models:/code/models --name tts eyay/tts-service