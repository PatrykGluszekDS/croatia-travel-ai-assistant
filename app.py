import os

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are Croatia Travel AI Assistant.

You help users plan trips to Croatia.
You can suggest places, itineraries, activities, local tips, and practical travel advice.

For now, you do not have access to a database or booking system.
If you are unsure, say that you are not sure instead of inventing details.
Keep answers friendly, practical, and clear.
"""


def chat(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    response = client.responses.create(
        model="gpt-5.5",
        input=messages,
    )

    return response.output_text


demo = gr.ChatInterface(
    fn=chat,
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