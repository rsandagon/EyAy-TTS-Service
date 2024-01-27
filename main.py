from typing import Union
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from balacoon_tts import TTS
from llama_cpp import Llama
# from huggingface_hub import hf_hub_download
from typing import List
import wave
import re

# Model can be dowloaded in huggingface
# from huggingface_hub import hf_hub_download, list_repo_files
# tts_model_path = hf_hub_download(repo_id="balacoon/tts", filename="en_us_hifi92_light_cpu.addon")

# tts model
tts_model_path = "models/en_us_hifi_jets_cpu.addon"
tts = TTS(tts_model_path)
speakers = tts.get_speakers()

# chat model
## Download the GGUF model
# model_name = "brittlewis12/stablelm-2-zephyr-1_6b-GGUF"
# model_file = "stablelm-2-zephyr-1_6b.Q4_K_M.gguf"
# model_path = hf_hub_download(model_name, filename=model_file, local_dir="models" )

llm = Llama(model_path="models/stablelm-zephyr-3b.Q4_K_M.gguf", chat_format="zephyr", n_ctx=512, n_gpu_layers=0)
# llm = Llama(model_path="models/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf", chat_format="llama-2", n_ctx=512, n_gpu_layers=0)

app = FastAPI(
    title="REST_TTS_Dockerized",
    description="TTS REST API wrapper with FastAPI and Docker, for your text-to-speech needs🤖",
    summary="TTS REST API Dockerized",
    version="0.0.1",
    terms_of_service="https://github.com/rsandagon/REST_TTS_Dockerized/README.md",
    contact={
        "name": "rsandagon",
        "url": "https://github.com/rsandagon",
        "email": "rsandagon.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

class Item(BaseModel):
    name: str
    message: str
    sample_rate: float 
    speaker: int

class ChatCompletion(BaseModel):
    model: str = ""
    messages:  List[dict] = []
    stream: bool = False
    max_tokens: float = 50
    temperature: float = 1
    top_p:float = 1 
    stop: List[str] = []

def remove_between_asterisks(text):
  pattern = r"\*.*?\*"
  return re.sub(pattern, "", text)

@app.get("/")
def read_root():
    return {"Hello": "I'm alive!"}

@app.get("/api/small")
def small_model():
    llm = Llama(model_path="models/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf", chat_format="llama-2", n_ctx=512, n_gpu_layers=0)
    return {"Hello": "small!"}

@app.get("/api/big")
def big_model():
    llm = Llama(model_path="models/stablelm-zephyr-3b.Q4_K_M.gguf", chat_format="zephyr", n_ctx=512, n_gpu_layers=0)
    return {"Hello": "big!"}

@app.get(
    path="/api/snd"
)
async def post_media_file(name:str='default'):
    return FileResponse("audio/outputs/"+name, media_type="audio/mpeg")

@app.post("/api/tts")
async def post_tts(item: Item):
    now = datetime.now()
    nowstr = now.strftime("%m%d%Y_%H%M%S")
    outname = item.name+nowstr+".wav"
    sample_rate = item.sample_rate
    samples = tts.synthesize(remove_between_asterisks(item.message), speakers[item.speaker])

    with wave.open("audio/outputs/"+outname, "w") as fp:
        fp.setparams((1, 2, tts.get_sampling_rate()*sample_rate, len(samples), "NONE", "NONE"))
        fp.writeframes(samples)

    return {"file":outname}

@app.post("/api/chat")
async def post_chat(item: ChatCompletion):
    response = llm.create_chat_completion(
        model = item.model,
        messages = item.messages,
        stop = item.stop,
        stream = item.stream,
        max_tokens = item.max_tokens,
        temperature = item.temperature,
        top_p = item.top_p
    )
    print("response",response['choices'])
    return response['choices'][0]