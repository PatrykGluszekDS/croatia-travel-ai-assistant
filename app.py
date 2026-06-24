import os

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()


SYSTEM_PROMPT = """
You are Croatia Travel AI Assistant.

You help users plan trips to Croatia.
You can suggest places, itineraries, activities, local tips, and practical travel advice.

For now, you do not have access to a database or booking system.
If you are unsure, say that you are not sure instead of inventing details.
Keep answers friendly, practical, and clear.
"""


def chat(message, history):
    messages = []

    for item in history:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content")

            if role in ["user", "assistant"] and isinstance(content, str):
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": message})

    response = client.responses.create(
        model="gpt-5.5",
        instructions=SYSTEM_PROMPT,
        input=messages,
    )

    return response.output_text


demo = gr.ChatInterface(
    fn=chat,
    type="messages",
    title="Croatia Travel AI Assistant",
    description="Ask for Croatia travel ideas, itineraries, and practical tips.",
    examples=[
        "Plan me a 3-day trip to Split.",
        "What should I do on Krk island?",
        "Suggest a romantic weekend in Croatia.",
        "I want hidden gems near Zadar.",
    ],
)


if __name__ == "__main__":
    demo.launch()