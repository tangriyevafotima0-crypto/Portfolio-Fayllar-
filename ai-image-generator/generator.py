"""Image Generator module with DALL-E API integration."""

from datetime import datetime
from openai import OpenAI, OpenAIError
from utils import save_image_from_url


class ImageGeneratorError(Exception):
    """Custom exception for image generation errors."""

    pass


class ImageGenerator:
    """AI-powered image generator using OpenAI's DALL-E API.

    Manages image generation requests, history tracking,
    and image download functionality.

    Attributes:
        client: OpenAI API client instance.
    """

    def __init__(self, api_key: str) -> None:
        """Initialize the ImageGenerator with API credentials.

        Args:
            api_key: OpenAI API key for authentication.

        Raises:
            ImageGeneratorError: If the API key is empty.
        """
        if not api_key:
            raise ImageGeneratorError("API key cannot be empty")

        self.client = OpenAI(api_key=api_key)
        self._history: list[dict[str, str]] = []

    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """Generate an image from a text prompt using DALL-E.

        Args:
            prompt: Text description of the desired image.
            size: Image dimensions. One of '1024x1024', '1024x1792', '1792x1024'.

        Returns:
            URL of the generated image.

        Raises:
            ImageGeneratorError: If prompt is empty or API call fails.
        """
        if not prompt.strip():
            raise ImageGeneratorError("Prompt cannot be empty")

        valid_sizes = ["1024x1024", "1024x1792", "1792x1024"]
        if size not in valid_sizes:
            raise ImageGeneratorError(
                f"Invalid size. Must be one of: {', '.join(valid_sizes)}"
            )

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1
            )

            image_url = response.data[0].url

            self._history.append({
                "prompt": prompt,
                "url": image_url,
                "size": size,
                "timestamp": datetime.now().isoformat()
            })

            return image_url

        except OpenAIError as e:
            raise ImageGeneratorError(f"DALL-E API error: {str(e)}") from e
        except Exception as e:
            raise ImageGeneratorError(f"Unexpected error: {str(e)}") from e

    def get_history(self) -> list[dict]:
        """Retrieve the image generation history.

        Returns:
            List of dictionaries with prompt, url, size, and timestamp.
        """
        return self._history.copy()

    def save_image(self, url: str, filename: str) -> str:
        """Download and save an image from a URL.

        Args:
            url: URL of the image to download.
            filename: Desired filename for the saved image.

        Returns:
            Path to the saved image file.

        Raises:
            ImageGeneratorError: If download or save fails.
        """
        try:
            return save_image_from_url(url, filename)
        except Exception as e:
            raise ImageGeneratorError(f"Failed to save image: {str(e)}") from e

    def clear_history(self) -> None:
        """Clear the generation history."""
        self._history = []
