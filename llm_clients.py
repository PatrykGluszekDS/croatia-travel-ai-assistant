from openai import OpenAI
from ollama import chat as ollama_chat
from dotenv import load_dotenv

from tools import TOOLS, call_tool


def chat_with_openai(messages, system_prompt):
    """
    Chat with OpenAI.

    This version supports tool calling, so the model can call SQLite-backed tools.
    """

    load_dotenv()
    openai_client = OpenAI()

    response = openai_client.responses.create(
        model="gpt-5.5",
        instructions=system_prompt,
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

    final_response = openai_client.responses.create(
        model="gpt-5.5",
        instructions=system_prompt,
        input=messages,
        tools=TOOLS,
    )

    return final_response.output_text


def chat_with_ollama(messages, system_prompt, model="llama3.2:1b"):
    """
    Chat with a local Ollama model.

    This version uses local text generation only.
    It does not use our SQLite tools.
    """

    ollama_messages = [{"role": "system", "content": system_prompt}]

    for message in messages:
        role = message.get("role")
        content = message.get("content")

        if role in ["user", "assistant"] and isinstance(content, str):
            ollama_messages.append({"role": role, "content": content})

    response = ollama_chat(
        model=model,
        messages=ollama_messages,
        stream=False,
    )

    return response["message"]["content"]