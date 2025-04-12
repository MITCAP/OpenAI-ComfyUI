# ComfyUI_Openalle3/__init__.py

# Import the node classes
from .openai_dalle3_node import OpenAIDalle3Node
from .openai_image_description_node import OpenAIImageDescriptionNode

# A dictionary that maps node attribute names to node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAIDalle3Node": "OpenAI DALL-E 3 Vision Guide",
    "OpenAIImageDescriptionNode": "OpenAI Image Description"
}

# A dictionary that maps Python class names to object names
NODE_CLASS_MAPPINGS = {
    "OpenAIDalle3Node": OpenAIDalle3Node,
    "OpenAIImageDescriptionNode": OpenAIImageDescriptionNode
}

# Optional: Add a message indicating the node loaded successfully
print("### Loading: OpenAI DALL-E 3 and Image Description Custom Nodes ###")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 