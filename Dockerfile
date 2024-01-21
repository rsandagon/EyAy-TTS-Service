FROM balacoon/tts_server:0.2

WORKDIR /code

# install tts
COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
COPY ./main.py .
COPY ./start.sh .
RUN chmod +x start.sh
COPY ./modelfiles/Liza/Modelfile Modelfile

# install llamaccp
RUN pip3 install --no-cache-dir llama-cpp-python[server]
COPY ./run_ollama.sh .
RUN chmod +x run_ollama.sh

VOLUME ["/audio","/models"]

EXPOSE 7861
EXPOSE 11434

ENTRYPOINT ./start.sh