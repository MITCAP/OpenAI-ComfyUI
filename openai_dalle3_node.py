import os
import torch
import numpy as np
from PIL import Image
import io
import base64
from openai import OpenAI, APIError, AuthenticationError

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

# Function to encode PIL image to Base64
def encode_pil_to_base64(pil_image):
    buffered = io.BytesIO()
    # Ensure PNG format for transparency support, though OpenAI also accepts JPEG/WEBP
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

class OpenAIDalle3Node:
    def __init__(self):
        pass # No specific initialization needed for the node itself

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False, "default": os.environ.get('OPENAI_API_KEY', '')}),
                "prompt": ("STRING", {"multiline": True, "default": "A cute cat astronaut floating in space"}),
                "model": (["dall-e-3", "dall-e-2"], {"default": "dall-e-3"}),
                "quality": (["standard", "hd"], {"default": "standard"}), # Only for DALL-E 3
                "size": (["1024x1024", "1792x1024", "1024x1792"], {"default": "1024x1024"}), # Sizes vary by model
            },
            "optional": {
                 "input_image": ("IMAGE", ),
                 "vision_model": (["gpt-4o", "gpt-4-turbo"], {"default": "gpt-4o"}), # For generating dalle prompt
                 "style": (["vivid", "natural"], {"default": "vivid"}), # Only for DALL-E 3
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("generated_image",)
    FUNCTION = "generate_image"
    CATEGORY = "OpenAI"

    def generate_image(self, api_key, prompt, model, quality, size, input_image=None, vision_model="gpt-4o", style="vivid"):
        if not api_key:
             raise ValueError("OpenAI API Key is required.")

        try:
            client = OpenAI(api_key=api_key)
            final_prompt = prompt

            # --- Step 1: (Optional) Refine prompt using Vision model if image provided ---
            if input_image is not None:
                print("Input image provided. Using vision model to generate Funko Pop style prompt...")
                pil_image = tensor2pil(input_image)
                base64_image = encode_pil_to_base64(pil_image)

                try:
                    # New meta-prompt specifically asking for a Funko Pop description
                    funko_meta_prompt = (
                        f"Analyze the provided image and the user's text hint ('{prompt}'). "
                        "Based *primarily* on the visual content of the image, create a detailed DALL-E prompt "
                        "describing a stylized Funko Pop vinyl figure version of the main subject in the image. "
                        "The figure should have Funko Pop characteristics: large oversized head, small body, "
                        "matte plastic texture, black beady eyes, simplified cartoon-like features, and typically no mouth. "
                        "Describe the figure's pose, clothing, and key features based on the image. "
                        "The final prompt should focus on the figure itself and suggest a simple background like a product shot (e.g., plain white background)."
                    )

                    vision_prompt_content = [
                        {
                            "type": "text",
                            "text": funko_meta_prompt, # Use the new Funko-specific prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"}, # Use high detail for better analysis
                        },
                    ]

                    response = client.chat.completions.create(
                        model=vision_model,
                        messages=[
                            {
                                "role": "user",
                                "content": vision_prompt_content,
                            }
                        ],
                        max_tokens=300 # Limit token usage for the generated prompt
                    )

                    if response.choices and response.choices[0].message.content:
                       final_prompt = response.choices[0].message.content.strip()
                       print(f"Refined Prompt from {vision_model}: {final_prompt}")
                    else:
                       print(f"Warning: Vision model ({vision_model}) did not return a refined prompt. Using original prompt.")

                except APIError as e:
                    print(f"OpenAI API Error (Vision): {e}. Falling back to original prompt.")
                except AuthenticationError:
                     raise AuthenticationError("Invalid OpenAI API Key provided.")
                except Exception as e:
                    print(f"Error during vision model processing: {e}. Falling back to original prompt.")


            # --- Step 2: Generate image using DALL-E ---
            print(f"Generating image with {model} using prompt: {final_prompt[:100]}...") # Log truncated prompt

            # DALL-E 3 specific parameters
            dalle3_params = {}
            if model == "dall-e-3":
                dalle3_params["quality"] = quality
                dalle3_params["style"] = style
                # DALL-E 3 only supports n=1
            else: # DALL-E 2 specific validation/params if needed
                 if size not in ["1024x1024", "512x512", "256x256"]:
                      print(f"Warning: Size {size} not standard for DALL-E 2. Defaulting to 1024x1024.")
                      size = "1024x1024"


            image_response = client.images.generate(
                model=model,
                prompt=final_prompt,
                size=size,
                response_format="b64_json",
                n=1, # DALL-E 3 only supports 1 image at a time via API
                **dalle3_params
            )

            if not image_response.data or not image_response.data[0].b64_json:
                 raise ValueError("OpenAI API did not return image data.")

            # Decode the Base64 string
            img_data = base64.b64decode(image_response.data[0].b64_json)

            # Convert to PIL Image
            generated_image_pil = Image.open(io.BytesIO(img_data))

            # Convert PIL Image to Tensor
            generated_image_tensor = pil2tensor(generated_image_pil)

            return (generated_image_tensor,)

        except AuthenticationError:
             # Re-raise specifically for ComfyUI feedback
             raise AuthenticationError("Invalid OpenAI API Key. Please check your key.")
        except APIError as e:
            # Handle API errors (e.g., rate limits, server issues)
            # Re-raise the original error to preserve details
            raise e
        except Exception as e:
            # Handle other potential errors (network, library issues, etc.)
            raise RuntimeError(f"An unexpected error occurred: {e}") from e


# Add the node to ComfyUI's mapping (needed if not using __init__.py, but good practice)
# NODE_CLASS_MAPPINGS = {
#     "OpenAIDalle3Node": OpenAIDalle3Node
# }
# NODE_DISPLAY_NAME_MAPPINGS = {
#     "OpenAIDalle3Node": "OpenAI DALL-E 3 Vision Guide"
# } 