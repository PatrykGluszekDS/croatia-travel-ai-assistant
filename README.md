# Croatia Travel AI Assistant

Croatia Travel AI Assistant is a portfolio project for practicing LLM application development with Python.

The app helps users plan trips to Croatia using an AI assistant, a local SQLite database, OpenAI tool calling, image generation, and audio route briefings.

## Features

### Chat assistant

The main chatbot helps users with Croatia travel planning. It can suggest destinations, itineraries, travel styles, and practical tips.

The chat supports conversation history, so the assistant can remember previous messages during the current session.

### SQLite travel package database

The project includes a local SQLite database with sample Croatia travel packages.

The database contains example packages for destinations such as:

- Split
- Dubrovnik
- Krk
- Zadar
- Istria

The assistant can search the database by destination, region, travel style, duration, and maximum price.

### OpenAI tool calling

The assistant uses OpenAI tool calling to decide when it should access the SQLite database.

For example, when the user asks:

```text
Do you have anything romantic?
```

the model can call a Python tool that searches the local database for romantic travel packages.

This demonstrates how an LLM can work together with external structured data.

### Image generation

The app includes a destination image generation tab.

The user can choose:

- destination
- visual style
- mood

The app then generates a travel-style image for the selected Croatian destination.

### Getting to Croatia route briefing

The app includes a route briefing feature that helps users understand how they could travel from their origin city or country to a destination in Croatia.

The user can provide:

- origin city or country
- destination in Croatia
- transport preference
- travel style
- voice
- audio tone

The app generates:

- a written route briefing
- an audio version of the briefing

The route briefing is intended as general travel guidance and does not provide live timetables, ticket prices, or real-time availability.

## Tech stack

- Python
- OpenAI API
- Gradio
- SQLite
- uv
- python-dotenv

## Project structure

```text
croatia-travel-ai-assistant/
├── app.py
├── database.py
├── tools.py
├── image_generation.py
├── route_planner.py
├── README.md
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
├── data/
│   └── croatia_travel.db        # generated locally, not committed
├── generated_images/            # generated locally, not committed
└── generated_audio/             # generated locally, not committed
```

## Setup

Clone the repository:

```bash
git clone https://github.com/PatrykGluszekDS/croatia-travel-ai-assistant.git
cd croatia-travel-ai-assistant
```

Install dependencies with uv:

```bash
uv sync
```

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Initialize the SQLite database:

```bash
uv run database.py
```

Run the Gradio app:

```bash
uv run app.py
```

Then open the local Gradio URL shown in the terminal.

## Environment and dependency management

This project uses `uv` for Python environment and dependency management.

Important files:

- `pyproject.toml` contains project metadata and dependencies.
- `uv.lock` stores exact resolved package versions.
- `.venv/` is the local virtual environment and is not committed.
- `.env` stores private API keys and is not committed.
- `.env.example` shows which environment variables are required.

## Generated files

The following outputs are generated locally and are not committed to GitHub:

- SQLite database file: `data/croatia_travel.db`
- generated images: `generated_images/`
- generated audio files: `generated_audio/`

They are ignored because they are generated outputs, can grow large, and may contain private or temporary data.

## Example use cases

The assistant can answer questions such as:

```text
Do you have a package for Split?
```

```text
Show me packages under 500 euro.
```

```text
Do you have anything romantic?
```

```text
I want something in Dalmatia for 3 days.
```

The image generator can create travel-style visuals such as:

```text
Destination: Dubrovnik
Style: vintage travel poster
Mood: romantic
```

The route briefing tab can generate advice such as:

```text
Origin: Warsaw, Poland
Destination: Split
Transport preference: flexible / best overall option
Travel style: balanced
```

## Current limitations

- The database contains sample travel packages, not real commercial offers.
- The route planner does not use live flight, train, bus, ferry, or traffic APIs.
- Prices and travel times should be treated as approximate unless verified with current sources.
- Generated images and audio are stored locally and ignored by Git.

## Possible improvements

- Add screenshots to the README
- Add more realistic sample travel packages
- Improve the database schema
- Add saved user preferences
- Add optional Ollama/local model support
- Add tests for database and tool functions
- Add deployment instructions

