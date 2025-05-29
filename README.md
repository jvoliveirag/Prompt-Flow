# Weather-Based Activity Suggester

## Overview

This project is a flow-based application that suggests suitable activities based on weather conditions for a specified city and country. It uses Microsoft Prompt Flow features to orchestrate tools. It fetches weather data, analyzes the conditions, and uses an LLM (Large Language Model) to generate personalized activity recommendations.
With this project I aim to study and practice concepts like AI agents, LLM orchestration, toolings and best practices.

## How It Works

The application follows a simple flow:

1.  **Input**: The user specifies a city and country (defaults to Campinas, Brazil).
2.  **Weather Data**: The `get_weather.py` script retrieves current weather conditions for the specified location.
3.  **Activity Generation**: An LLM (GPT-3.5 Turbo) analyzes the weather data and generates activity suggestions.
4.  **Output Processing**: The `extract_llm_response_content.py` script processes the LLM output to provide clean, readable recommendations.

## Components

*   `flow.dag.yaml`: The main flow definition file.
*   `get_weather.py`: Python script to fetch weather data.
*   `GPT_Chat_Prompt.jinja2`: Prompt template for the LLM.
*   `extract_llm_response_content.py`: Script to process LLM responses.

## Setup and Running

### Prerequisites

*   Python 3.9+
*   PromptFlow (CLI)
*   OpenAI API key

### Setup Instructions

1.  Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

2.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Set up the OpenAI connection: Create a connection file named `connection.yaml` with your OpenAI API key:

    ```yaml
    name: <your_connection_name_here>
    type: azure_open_ai or open_ai
    api_key: <user-input> # do not change this! It will be prompted to you manualy input it in terminal when you save the file
    # Add other configuration as needed
    ```

    Then create the connection using the PromptFlow CLI:

    ```bash
    pf connection create --file connection.yaml
    ```
    To know more check the <a href="https://microsoft.github.io/promptflow/" target="_blank" rel="noopener noreferrer">official documentation</a>.

### Running the Flow

*   Run the flow with default inputs (Campinas, Brazil):

    ```bash
    pf flow test --flow .
    ```

*   Or specify a different city and country:

    ```bash
    pf flow test --flow . --inputs city_name=London country_name=UK
    ```

## Troubleshooting

If you encounter errors:

*   Ensure all required packages are installed (`promptflow-tools` is essential).
*   Verify your OpenAI connection is correctly set up.
*   Check that the Python files match the node definitions in `flow.dag.yaml`.

## Extending the Project

You can extend this project by:

*   Adding more detailed weather data.
*   Incorporating user preferences for activity types.
*   Expanding to include more contextual information (e.g., local attractions).
*   Building a web interface for easier interaction.