# Croatia Travel AI Assistant

Croatia Travel AI Assistant is a small portfolio project for practicing LLM application development with Python.

The app is being built step by step using:

- OpenAI API
- Gradio
- SQLite
- uv for project and dependency management

The goal is to create an AI assistant that helps users plan trips to Croatia. The assistant will later be able to use tools, search a local SQLite database, generate images, and provide audio responses.

## Current features

- Basic Gradio chatbot interface
- OpenAI-powered travel assistant
- SQLite database setup with sample Croatia travel packages
- Local database query function for finding packages by destination

## Project structure

```text
croatia-travel-ai-assistant/
├── app.py
├── database.py
├── README.md
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
└── data/
    └── croatia_travel.db   # generated locally, not committed
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

Create a `.env` file:

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

## Notes

The SQLite database file is generated locally and is not committed to GitHub. The database can be recreated by running `database.py`.

## Planned features

- Connect the SQLite database to the chatbot
- Add OpenAI tool/function calling
- Add image generation for destinations
- Add text-to-speech audio responses
- Add optional Ollama/local model support
- Improve the UI and README with screenshots

