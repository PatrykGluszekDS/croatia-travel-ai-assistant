import os

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

from database import get_packages_by_destination, initialize_database
from tools import TOOLS, call_tool


load_dotenv()

client = OpenAI()

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


def chat(message, history):
    """
    Chatbot function used by Gradio.

    The assistant receives previous conversation history and the current user message.
    If needed, the model can call a SQLite-backed tool to get travel package data.
    """

    messages = convert_history_to_openai_messages(history)
    messages.append({"role": "user", "content": message})

    response = client.responses.create(
        model="gpt-5.5",
        instructions=SYSTEM_PROMPT,
        input=messages,
        tools=TOOLS,
    )

    messages += response.output

    tool_calls = [item for item in response.output if item.type == "function_call"]

    if not tool_calls:
        return response.output_text

    for tool_call in tool_calls:
        tool_result = call_tool(tool_call.name, tool_call.arguments)

        messages.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": tool_result,
            }
        )

    final_response = client.responses.create(
        model="gpt-5.5",
        instructions=SYSTEM_PROMPT,
        input=messages,
        tools=TOOLS,
    )

    return final_response.output_text


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