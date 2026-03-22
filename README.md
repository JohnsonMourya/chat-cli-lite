
# Gemini CLI Lite

A lightweight command-line interface for interacting with Gemini models, optimized for low-end systems and environments with limited resources. This CLI aims to provide essential Gemini functionality without the overhead of larger applications.

## Features

*   **Resource-Efficient:** Designed to run with minimal CPU and memory usage, making it ideal for older hardware or constrained environments.
*   **Simple Command Structure:** Easy-to-use commands for quick access and integration into scripts.
*   **Fast and Responsive:** Optimized for speed and low latency.

## Installation

To install Gemini CLI Lite, you can use pip if it's packaged, or clone the repository and run the script directly.

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd Gemini_cli_lite
    ```

1. Ensure you have the necessary Python dependencies installed (refer to `requirements.txt`).
    ```bash
    pip install -r requirements.txt
    ```
    OR Install the dependencies 
    ```bash
    pip install google-genai textual google-api-core python-dotenv
   ```

## Usage

The CLI can be invoked using the `gemini_cli_lite` command (or by running the main Python script directly, e.g., `python gemini.py`).

**Basic Prompting:**
Send a text prompt to the Gemini model.

```bash
python gemini_cli_lite
```

**Specifying Model and Prompt (Example):**
If you have different Gemini models available or want to be explicit.

```
/model
```


*(Note: The exact command name and options will depend on how `gemini.py` is implemented as very basic cli. This is a general template.)*

## Commands

*   `/model`: Change the active Gemini model.
*   `/exit` or `/quit`: Exit the CLI application.
*   `/session`: Load or switch between chat sessions.
*   `/save`: Manually save the current chat session (note: there is no autosave upon exit).
*   `/new`: Create a new chat session.

To change the default model, modify the `setting.json` file.

## Configuration

API keys and other settings can typically be managed via environment variables or a configuration file.

**Environment Variables:**
Set the `GEMINI_API_KEY` environment variable:
Create a file '.env' and add your key
```
GEMINI_API_KEY='YOUR_API_KEY'
```

## Contributing

We welcome contributions! Please refer to the `CONTRIBUTING.md` file for guidelines on how to submit pull requests, report bugs, and suggest features.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
