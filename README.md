# Multi-Agent Research System with Autogen and Azure OpenAI

## Overview

This project leverages the power of Azure OpenAI and Autogen to create a multi-agent research system. The system is designed to automate complex research tasks, including web browsing, web scraping, and code generation, by orchestrating multiple intelligent agents.

## Features

- **Multi-Agent Architecture**: The system is built using Autogen, allowing for the coordination of multiple agents to perform specific tasks in parallel.
- **Web Browsing**: Agents can autonomously browse the web to gather information and perform research on specific topics.
- **Web Scraping**: Capable of extracting data from websites, the agents can scrape relevant information for analysis or further processing.
- **Code Generation**: The system can generate Python code based on the research findings, allowing for seamless automation and integration with other tools or workflows.
- **Azure OpenAI Integration**: Utilizes Azure OpenAI for natural language understanding and processing, enabling the agents to interpret and execute complex instructions.

## Prerequisites

- **Azure Subscription**: An active Azure account with access to Azure OpenAI services.
- **Python 3.12+**: The project is developed using Python, so you'll need a compatible Python environment.
- **Autogen**: The core of the multi-agent system, installable via pip.
- **Additional Libraries**: Required Python packages are listed in `requirements.txt`.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repository/multiagent-research-autogen.git
    cd multiagent-research-autogen
    ```

2. **Set Up Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Azure OpenAI**:
   - Set up your Azure OpenAI credentials in a `.env` file or export them as environment variables:
     ```bash
     export AZURE_OPENAI_KEY=your_openai_key
     export AZURE_OPENAI_ENDPOINT=your_openai_endpoint
     export APIFY_API_KEY=your_apify_api_key
     export SERP_API_KEY=your_serper_api_key
     ```

## Usage

### Running the System

To start the multi-agent system, use the following command:

```bash
python main.py
