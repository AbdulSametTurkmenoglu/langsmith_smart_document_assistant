# Intelligent Document Assistant with LangSmith (RAG)

This project creates a RAG (Retrieval-Augmented Generation) system using LangChain, OpenAI, and ChromaDB, and utilizes **LangSmith** to trace, debug, and evaluate the entire process.

The assistant reads text files from the `data/` folder, converts them into vectors, and answers user questions based on these documents.

## Features

* **RAG Architecture:** System that generates answers by retrieving context from documents.
* **LangSmith Integration:**
    * All steps (document loading, chain setup, question asking) are traced with `@traceable` decorators.
    * Token usage, cost, and latency are automatically tracked.
    * **Feedback Collection:** Rating each question-answer pair with `user_rating` (0 or 1) and viewing these scores in the LangSmith interface.
* **Modular Structure:** Data, configuration, prompts, and main logic are separated in the `src/` folder.
* **Two Execution Modes:**
    1. `run_demo.py`: Runs a demo with predefined questions and sends automatic (simulated) feedback.
    2. `chat.py`: Allows you to interactively chat with the assistant and manually provide feedback (y/n) for each answer.

## Installation

1. **Clone the Repository:**
```bash
    git clone https://github.com/AbdulSametTurkmenoglu/langsmith_smart_document_assistant.git
    cd langsmith_smart_document_assistant
```

2. **Virtual Environment (Recommended):**
```bash
    python -m venv .venv
    # Windows: .\.venv\Scripts\activate
    # macOS/Linux: source .venv/bin/activate
```

3. **Install Required Libraries:**
```bash
    pip install -r requirements.txt
```

4. **Create .env File:**
    Copy the `.env.example` file, rename it to `.env`, and fill it with your own API keys:
```bash
    # Windows
    copy .env.example .env
    
    # macOS / Linux
    cp .env.example .env
```
    
    Contents of the `.env` file:
```
    OPENAI_API_KEY="sk-..."
    LANGSMITH_API_KEY="..."
    LANGSMITH_PROJECT="Intelligent Document Assistant" # Project name to appear in LangSmith
```

## Usage

You can run it in two different modes:

### 1. Demo Mode (`run_demo.py`)

This script loads documents from the `data/` folder, asks questions from the `questions` list sequentially, and automatically sends a (simulated) score (0 or 1) to LangSmith for each answer.
```bash
python run_demo.py
```

After running this mode, you can go to the LangSmith interface to see the "Ask Question" runs under your project and their associated "user_rating" scores.

### 2. Interactive Chat Mode (`chat.py`)

This script allows you to chat with the assistant in real-time. After each answer, it asks you "Was this helpful? (y/n)" and saves the score (1.0 or 0.0) to LangSmith based on your response.
```bash
python chat.py
```
```
 Assistant is ready. You can ask your questions.
------------------------------------------------------------
 Question: What is LangSmith?
 Answer: LangSmith is a tool used to trace and debug LangChain applications. Every chain call, token usage, and errors can be viewed in LangSmith.
  Duration: 1.23s
  3 sources used
   Was the answer helpful? (y/n/enter=skip): y
   LangSmith Feedback added (Score: 1.0)
 Question: 
```
