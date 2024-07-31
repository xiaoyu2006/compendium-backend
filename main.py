import os

from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
from openai import AsyncOpenAI

from helper import process_upload, query_gpt

load_dotenv()

app = FastAPI()
openai = AsyncOpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.environ.get("OPENAI_API_KEY"),
)


@app.get("/")
async def root():
    return {"health": "ok", "version": "0"}


@app.post("/query/")
async def query_iamge(file: UploadFile):
    contents = await file.read()
    img_str = process_upload(contents)
    response = await query_gpt(openai, img_str)
    return {"response": response}
