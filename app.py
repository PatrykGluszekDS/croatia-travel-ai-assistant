import os

import gradio as gr
from dotenv import load_dotenv

from database import get_packages_by_destination, initialize_database
from image_generation import generate_destination_image
from route_planner import generate_route_briefing
from llm_clients import chat_with_openai, chat_with_ollama


load_dotenv()
initialize_database()


SYSTEM_PROMPT = """
You are Croatia Travel AI Assistant.

You help users plan trips to Croatia.
You can suggest places, itineraries, activities, local tips, and practical travel advice.

You have access to a local SQLite travel packages database through tools.
When the user asks about available packages, prices, duration, or travel styles for a destination, use the tool.
When tool results are available, use them as the main source of truth.
Do not invent exact package prices if they are not provided by the tool.
If you are unsure, say that you are not sure instead of inventing details.
Keep answers friendly, practical, and clear.
"""


def extract_text_from_gradio_content(content):
    """
    Extract plain text from Gradio message content.
    """

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)

            elif isinstance(block, dict):
                if block.get("type") == "text" and isinstance(block.get("text"), str):
                    text_parts.append(block["text"])
                elif isinstance(block.get("content"), str):
                    text_parts.append(block["content"])

        return "\n".join(text_parts).strip()

    if isinstance(content, dict):
        if isinstance(content.get("text"), str):
            return content["text"]
        if isinstance(content.get("content"), str):
            return content["content"]

    return ""


def convert_history_to_openai_messages(history):
    """
    Convert Gradio 6 chat history into OpenAI-style messages.
    """

    messages = []

    for item in history:
        if isinstance(item, dict):
            role = item.get("role")
            content = extract_text_from_gradio_content(item.get("content"))

            if role in ["user", "assistant"] and content:
                messages.append({"role": role, "content": content})

        elif hasattr(item, "role") and hasattr(item, "content"):
            role = getattr(item, "role")
            content = extract_text_from_gradio_content(getattr(item, "content"))

            if role in ["user", "assistant"] and content:
                messages.append({"role": role, "content": content})

        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user_msg, assistant_msg = item

            user_text = extract_text_from_gradio_content(user_msg)
            assistant_text = extract_text_from_gradio_content(assistant_msg)

            if user_text:
                messages.append({"role": "user", "content": user_text})

            if assistant_text:
                messages.append({"role": "assistant", "content": assistant_text})

    return messages


def chat(message, history, model_provider):
    """
    Chatbot function used by Gradio.

    The user can choose between:
    - OpenAI: stronger model with SQLite tool calling
    - Ollama: local model without tool calling
    """

    messages = convert_history_to_openai_messages(history)
    messages.append({"role": "user", "content": message})

    if model_provider == "OpenAI":
        return chat_with_openai(messages, SYSTEM_PROMPT)

    if model_provider == "Ollama":
        return chat_with_ollama(
            messages=messages,
            system_prompt=SYSTEM_PROMPT,
            model="llama3.2:1b",
        )

    return "Unknown model provider selected."


model_provider_input = gr.Dropdown(
    label="Model provider",
    choices=["OpenAI", "Ollama"],
    value="OpenAI",
)

chat_demo = gr.ChatInterface(
    fn=chat,
    title="Croatia Travel AI Assistant",
    description=(
        "Ask for Croatia travel ideas, itineraries, and practical tips. "
        "OpenAI mode supports SQLite tool calling. Ollama mode runs locally."
    ),
    examples=[
        ["Plan me a 3-day trip to Split.", "OpenAI"],
        ["What should I do on Krk island?", "OpenAI"],
        ["Suggest a romantic weekend in Croatia.", "OpenAI"],
        ["I want hidden gems near Zadar.", "OpenAI"],
        ["Plan me a simple 2-day trip to Split using local Ollama.", "Ollama"],
    ],
    additional_inputs=[model_provider_input],
    additional_inputs_accordion=gr.Accordion(
        label="Model settings",
        open=True,
    )
)


with gr.Blocks(title="Croatia Travel AI Assistant") as demo:
    gr.Markdown("# Croatia Travel AI Assistant")

    if os.getenv("DEMO_MODE", "false").lower() == "true":
        gr.Markdown(
        "⚠️ Public demo mode is enabled. Some expensive features, such as image or audio generation, may be limited to control API usage."
    )

    with gr.Tab("Chat assistant"):
        chat_demo.render()

    with gr.Tab("Image generator"):
        gr.Markdown(
            "Generate a destination-style image for a Croatian travel idea."
        )

        destination_input = gr.Textbox(
            label="Destination",
            placeholder="Example: Split, Dubrovnik, Krk, Zadar, Istria",
        )

        style_input = gr.Dropdown(
            label="Visual style",
            choices=[
                "realistic travel photography",
                "vintage travel poster",
                "watercolor illustration",
                "cinematic tourism campaign",
            ],
            value="vintage travel poster",
        )

        mood_input = gr.Dropdown(
            label="Mood",
            choices=[
                "romantic",
                "relaxed",
                "adventurous",
                "luxury",
                "family-friendly",
            ],
            value="relaxed",
        )

        generate_button = gr.Button("Generate image")

        image_output = gr.Image(
            label="Generated image",
            type="filepath",
        )

        generate_button.click(
            fn=generate_destination_image,
            inputs=[destination_input, style_input, mood_input],
            outputs=image_output,
        )

    with gr.Tab("Getting to Croatia"):
        gr.Markdown(
            """Generate a practical route briefing and audio explanation for getting to Croatia.
            In public demo mode, audio generation may be disabled to control API usage."""
        )

        origin_input = gr.Textbox(
            label="Origin city or country",
            placeholder="Example: Warsaw, Poland",
        )

        destination_route_input = gr.Textbox(
            label="Destination in Croatia",
            placeholder="Example: Split, Dubrovnik, Krk, Zadar, Istria",
        )

        transport_preference_input = gr.Dropdown(
            label="Transport preference",
            choices=[
                "flexible / best overall option",
                "car",
                "flight",
                "bus",
                "train",
                "budget-friendly",
                "comfortable",
                "scenic route",
            ],
            value="flexible / best overall option",
        )

        travel_style_input = gr.Dropdown(
            label="Travel style",
            choices=[
                "cheapest possible",
                "fastest possible",
                "comfortable and simple",
                "family-friendly",
                "scenic and relaxed",
                "balanced",
            ],
            value="balanced",
        )

        route_voice_input = gr.Dropdown(
            label="Voice",
            choices=[
                "alloy",
                "ash",
                "ballad",
                "coral",
                "echo",
                "fable",
                "nova",
                "onyx",
                "sage",
                "shimmer",
                "verse",
            ],
            value="coral",
        )

        route_tone_input = gr.Dropdown(
            label="Audio tone",
            choices=[
                "warm and friendly",
                "calm and relaxing",
                "enthusiastic and energetic",
                "luxury travel consultant",
                "clear and informative",
            ],
            value="clear and informative",
        )

        route_button = gr.Button("Generate route briefing")

        route_text_output = gr.Textbox(
            label="Route briefing",
            lines=12,
        )

        route_audio_output = gr.Audio(
            label="Audio route briefing",
            type="filepath",
        )

        route_button.click(
            fn=generate_route_briefing,
            inputs=[
                origin_input,
                destination_route_input,
                transport_preference_input,
                travel_style_input,
                route_voice_input,
                route_tone_input,
            ],
            outputs=[route_text_output, route_audio_output],
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
    )