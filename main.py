import os

from fastapi import FastAPI, UploadFile, HTTPException
from dotenv import load_dotenv
from openai import AsyncOpenAI
from anthropic import Anthropic
from PIL import UnidentifiedImageError

from helper import process_upload, query_gpt, query_claude  # pylint: disable=unused-import

load_dotenv()

app = FastAPI()
openai = AsyncOpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.environ.get("OPENAI_API_KEY"),
)
anthropic = Anthropic(
    base_url=os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com/"),
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


@app.get("/")
async def root():
    return {"health": "ok", "version": "1"}


@app.post("/query/")
async def query_iamge(file: UploadFile):
    contents = await file.read()
    try:
        img_str = process_upload(contents)
    except UnidentifiedImageError as e:
        raise HTTPException(status_code=400, detail="Invalid image file") from e
    # response = await query_gpt(openai, img_str)
    response = query_claude(anthropic, img_str)
    if response == {}:
        raise HTTPException(status_code=400, detail="No object detected")
    return {"response": response}
