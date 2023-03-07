from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
import os
import json
import numpy as np
from TTS.api import TTS
import time
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

## Domain url from .env file using python-dotenv or os.environ
if os.environ.get("DOMAIN_URL"):
    domain_url = os.environ.get("DOMAIN_URL")
else:
    load_dotenv()
    domain_url = os.environ.get("DOMAIN_URL")
    

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#
def genTTS(text,lang):
    if lang == "en":
        tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=True, gpu=False)
    elif lang == "fr":
        tts = TTS(model_name="tts_models/fr/css10/vits", progress_bar=True, gpu=False)
    else:
        return "Language not supported"

    filename = time.strftime("%Y%m%d-%H%M%S") + ".wav"
    tts.tts_to_file(text, file_path=filename)

    # save the audio file un the static folder check if folder exists
    if not os.path.exists("static"):
        os.makedirs("static")
    os.rename(filename, "static/" + filename)
    return domain_url + "/static/" + filename



    

ttsInterface = gr.Interface(
    fn=genTTS,
    inputs=["text", gr.inputs.Dropdown(["en","fr" ], label="Language")],
    # output a string
    outputs="text",
    title="TTS",
    description="Text to Speech",
    
)
app = gr.mount_gradio_app(app, ttsInterface, "/api/tts" )


# Then run `uvicorn run:app` from the terminal and navigate to http://localhost:8000/gradio.