import os
import io
import base64
import numpy as np
from PIL import Image
from openai import OpenAI, APIError, AuthenticationError

# Function to encode PIL image to Base64
def encode_pil_to_base64(pil_image):
    buffered = io.BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

class OpenAIImageDescriptionNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False, "default": os.environ.get('OPENAI_API_KEY', '')}),
                "image": ("IMAGE", ),
                "prompt": ("STRING", {"multiline": True, "default": "Describe the person in this image"}),
                "model": (["gpt-4o", "gpt-4-turbo"], {"default": "gpt-4o"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("description",)
    FUNCTION = "describe_image"
    CATEGORY = "OpenAI"

    def describe_image(self, api_key, image, prompt, model):
        if not api_key:
            raise ValueError("OpenAI API Key is required.")

        try:
            client = OpenAI(api_key=api_key)
            # Convert PyTorch tensor to NumPy array
            image_np = image.cpu().numpy()
            # Convert NumPy array to PIL Image
            pil_image = Image.fromarray((image_np * 255).astype(np.uint8).squeeze())
            base64_image = encode_pil_to_base64(pil_image)

            vision_prompt_content = [
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"},
                },
            ]

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": vision_prompt_content,
                    }
                ],
                max_tokens=300
            )

            if response.choices and response.choices[0].message.content:
                description = response.choices[0].message.content.strip()
                return (description,)
            else:
                raise ValueError("Vision model did not return a description.")

        except AuthenticationError:
            raise AuthenticationError("Invalid OpenAI API Key. Please check your key.")
        except APIError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}") from e 