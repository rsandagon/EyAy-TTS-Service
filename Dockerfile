FROM balacoon/tts_server:0.2

WORKDIR /code

# install tts
COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
COPY ./main.py .
COPY ./start.sh .
RUN chmod +x start.sh

# install llamaccp
RUN pip3 install --no-cache-dir llama-cpp-python

VOLUME ["/audio","/models"]

EXPOSE 7861

ENTRYPOINT ./start.sh