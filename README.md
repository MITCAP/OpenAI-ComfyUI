# ComfyUI OpenAI DALL-E 3 Node

This project provides custom nodes for ComfyUI that integrate with OpenAI's DALL-E 3 and GPT-4o models. The nodes allow users to generate images and describe images using OpenAI's API.

## Features

- **OpenAIDalle3Node**: Generates images using OpenAI's DALL-E 3 model based on a text prompt and optional input image.
- **OpenAIImageDescriptionNode**: Describes a person in an image using a text prompt and OpenAI's vision capabilities.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/ComfyUI_OpenAI_Dalle3.git
   cd ComfyUI_OpenAI_Dalle3
   ```

2. **Install Dependencies:**

   Ensure you have Python installed. Then, install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**

   Set your OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

   On Windows, use:

   ```cmd
   set OPENAI_API_KEY=your-api-key
   ```

4. **Run ComfyUI:**

   Follow the instructions for running ComfyUI, ensuring that this custom node directory is included in the `custom_nodes` path.

## Usage

### OpenAIDalle3Node

- **Inputs:**
  - `api_key`: Your OpenAI API key.
  - `prompt`: Text prompt for image generation.
  - `model`: Choose between `dall-e-3` and `dall-e-2`.
  - `quality`: Image quality (`standard` or `hd`).
  - `size`: Image size (`1024x1024`, `1792x1024`, `1024x1792`).
  - `input_image` (optional): An image to refine the prompt.
  - `vision_model` (optional): Vision model for prompt refinement (`gpt-4o` or `gpt-4-turbo`).
  - `style` (optional): Style for DALL-E 3 (`vivid` or `natural`).

- **Output:**
  - `generated_image`: The generated image as a tensor.

### OpenAIImageDescriptionNode

- **Inputs:**
  - `api_key`: Your OpenAI API key.
  - `image`: Image of the person to describe.
  - `prompt`: Text prompt to guide the description.
  - `model`: Choose between `gpt-4o` and `gpt-4-turbo`.

- **Output:**
  - `description`: Text description of the person in the image.

## Compatibility

These nodes are compatible with ComfyUI on both Windows and Linux (Ubuntu Docker).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for their powerful API and models.
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) for providing a flexible UI framework. 