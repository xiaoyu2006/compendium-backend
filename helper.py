import io
import base64
import json

from fastapi import UploadFile
from openai import AsyncOpenAI
from PIL import Image


def process_upload(u: UploadFile) -> str:
    image = Image.open(io.BytesIO(u))
    original_size = image.size

    # Resize the image to max 512 px
    if original_size[0] > original_size[1]:
        new_size = (512, int(512 * original_size[1] / original_size[0]))
    else:
        new_size = (int(512 * original_size[0] / original_size[1]), 512)
    resized_image = image.resize(new_size)
    rgb_image = resized_image.convert("RGB")

    # Convert the resized image to base64
    buffered = io.BytesIO()
    rgb_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_str


# pylint: disable=line-too-long
PROMPT = """In the image:
1) Detect and classify one of the main objects in the image. If you recognize multiple objects, choose the most prominent one.
2) Report what you have found in the image using the following JSON format:
{
  "name": "Wikipedia entry name. Try to be as specific as possible, e.g. Tesla_Model_Y instead of Car",
  "x1": "Upper-left bounding box x coordinate",
  "y1": "Upper-left bounding box y coordinate",
  "x2": "Lower-right bounding box x coordinate",
  "y2": "Lower-right bounding box y coordinate",
}
With all coordinates start at the upper-left as the origin point and are represented as a proportion of the image width/height ranges from [0,1] that crops out the main object.
If you can't find any recognizable object, simply return {}"""


async def query_gpt(instance: AsyncOpenAI, base64_image: str) -> dict:
    response = await instance.chat.completions.create(
        model="gpt-4o",
        temperature=0.0,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )
    print(response)
    return json.loads(response.choices[0].message.content)
