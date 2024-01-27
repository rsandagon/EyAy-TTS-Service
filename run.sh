docker build . --tag eyay/tts-service
docker run -d -p 7861:7861 -v ./audio:/code/audio -v ./models:/code/models --name eyay-tts eyay/tts-service

# simulate t2nano
docker run --rm \
  --cpu-shares 512 \
  --memory 1024m \
  --memory-swap 2048m \
  -d -p 7861:7861 -v ./audio:/code/audio -v ./models:/code/models --name eyay-tts eyay/tts-service \  
  --name eyay-tts eyay/tts-service