import base64
from datetime import datetime
from pathlib import Path

from openai import OpenAI


IMAGE_OUTPUT_DIR = Path("generated_images")


def generate_destination_image(destination, style, mood):
    """
    Generate a travel-style image for a Croatian destination.

    Parameters:
    - destination: place in Croatia, e.g. Split, Dubrovnik, Krk
    - style: visual style, e.g. realistic, watercolor, vintage poster
    - mood: atmosphere, e.g. romantic, adventurous, relaxed
    """

    IMAGE_OUTPUT_DIR.mkdir(exist_ok=True)

    client = OpenAI()

    prompt = f"""
    Create a beautiful travel image for {destination}, Croatia.

    Visual style: {style}
    Mood: {mood}

    The image should look attractive for a travel planning app.
    It should show Croatian coastal atmosphere, warm light, clear composition,
    and a professional tourism-poster feeling.

    Do not include text, logos, watermarks, or fake brand names.
    """

    result = client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        size="1024x1024",
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_destination = destination.lower().replace(" ", "_")
    output_path = IMAGE_OUTPUT_DIR / f"{safe_destination}_{timestamp}.png"

    with open(output_path, "wb") as file:
        file.write(image_bytes)

    return str(output_path)