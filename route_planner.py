from datetime import datetime
from pathlib import Path

from openai import OpenAI


AUDIO_OUTPUT_DIR = Path("generated_audio")


ROUTE_SYSTEM_PROMPT = """
You are a practical Croatia travel route assistant.

Your task is to help users understand how they could get from their origin city/country
to a destination in Croatia.

You can suggest transport options such as car, flight, bus, train, ferry, or mixed routes.

Important rules:
- Do not invent exact live timetables, current ticket prices, or real-time availability.
- If you mention prices or travel times, describe them as approximate and advise checking current sources.
- Give practical advice: border crossings, transfers, luggage, parking, ferries, seasonality, and comfort.
- Keep the route plan clear, useful, and beginner-friendly.
"""


def generate_route_briefing(
    origin,
    destination,
    transport_preference,
    travel_style,
    voice,
    tone,
):
    """
    Generate a written route briefing and an audio narration.

    Returns:
    - route plan text
    - path to generated audio file
    """

    if not origin or not origin.strip():
        raise ValueError("Please provide an origin city or country.")

    if not destination or not destination.strip():
        raise ValueError("Please provide a destination in Croatia.")

    AUDIO_OUTPUT_DIR.mkdir(exist_ok=True)

    client = OpenAI()

    user_prompt = f"""
    Create a practical route briefing for a traveler.

    Origin: {origin}
    Destination in Croatia: {destination}
    Transport preference: {transport_preference}
    Travel style: {travel_style}

    Structure the answer with:
    1. Best overall option
    2. Alternative options
    3. Practical things to check before booking
    4. Short recommendation
    """

    text_response = client.responses.create(
        model="gpt-5.5",
        instructions=ROUTE_SYSTEM_PROMPT,
        input=user_prompt,
    )

    route_text = text_response.output_text

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = AUDIO_OUTPUT_DIR / f"route_briefing_{timestamp}.mp3"

    speech_instructions = f"""
    Speak like a helpful Croatia travel consultant.
    Tone: {tone}.
    Use clear pronunciation and natural pace.
    Make the route advice sound practical and easy to follow.
    """

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=route_text,
        instructions=speech_instructions,
    ) as response:
        response.stream_to_file(output_path)

    return route_text, str(output_path)