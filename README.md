

# ***plain Garmin Running Data Connector

A ***plain implementation of a Garmin connector, that connects Garmin data to an LLM an lets you talk to your data.


## Garmin Running ata Connector Description

A Python application that connects to Garmin Connect to fetch your running activity data and provides an AI-powered chat interface to analyze your running performance using Google's Gemini AI.

## Overview

The Garmin Running Analyst allows you to:
- Fetch running activities and lap data from Garmin Connect
- Store activity data locally for offline analysis
- Chat with an AI assistant about your running performance, trends, and insights

## Prerequisites

- Python 3.x
- A Garmin Connect account
- A Google API key for Gemini AI

## Installation

1. Navigate to the `garmin_app` directory:
   ```bash
   cd garmin_app
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Before running the application, you must set the following environment variables:

### Required Environment Variables

1. **`GARMIN_EMAIL`** - Your Garmin Connect email address
   ```bash
   export GARMIN_EMAIL="your.email@example.com"
   ```

2. **`GARMIN_PASSWORD`** - Your Garmin Connect password
   ```bash
   export GARMIN_PASSWORD="your_password"
   ```

3. **`GOOGLE_API_KEY`** - Your Google API key for Gemini AI
   ```bash
   export GOOGLE_API_KEY="your_google_api_key"
   ```

### Setting Environment Variables

You can set these variables in several ways:

**Option 1: Export in your shell session**
```bash
export GARMIN_EMAIL="your.email@example.com"
export GARMIN_PASSWORD="your_password"
export GOOGLE_API_KEY="your_google_api_key"
```

**Option 2: Create a `.env` file (requires python-dotenv package)**
```bash
GARMIN_EMAIL=your.email@example.com
GARMIN_PASSWORD=your_password
GOOGLE_API_KEY=your_google_api_key
```

**Option 3: Set inline when running the script**
```bash
GARMIN_EMAIL="your.email@example.com" GARMIN_PASSWORD="your_password" GOOGLE_API_KEY="your_google_api_key" python garmin_chat.py
```

## Usage

The application is run using `garmin_chat.py` with the following commands:

### Fetch Running Data

Retrieve running activities from Garmin Connect (last 180 days by default) and save them to a local JSON file:

```bash
python garmin_chat.py fetch
```

This command will:
- Authenticate with Garmin Connect (using stored tokens if available, or prompting for MFA if needed)
- Fetch all running activities from the last 180 days
- Retrieve lap/split data for each activity
- Save the data to `garmin_data.json` in the `garmin_app` directory

### Start Chat Session

Start an interactive chat session to analyze your stored running data:

```bash
python garmin_chat.py chat
```

This command will:
- Load previously fetched activity data from `garmin_data.json`
- Initialize a chat session with Google Gemini AI
- Provide an interactive interface to ask questions about your running data

**Note:** You must run `fetch` at least once before using `chat` to ensure data is available.

### Run Both Workflows

If you don't specify a command, the application will run both fetch and chat workflows sequentially:

```bash
python garmin_chat.py
```

This is equivalent to running `fetch` followed by `chat`.

## Authentication

The application uses token-based authentication with Garmin Connect. On first login:
- You'll be prompted for your Garmin credentials (from environment variables)
- If MFA (Multi-Factor Authentication) is enabled, you'll be prompted to enter your MFA code
- Authentication tokens are stored in `~/.garminconnect` for future use
- Subsequent runs will use stored tokens automatically

## Data Storage

- Activity data is stored in `garmin_data.json` in the `garmin_app` directory
- Authentication tokens are stored in `~/.garminconnect`
- You can delete `garmin_data.json` to force a fresh fetch on the next run

## Example Chat Interactions

Once in the chat session, you can ask questions like:
- "What was my average pace last month?"
- "Show me my longest run in the last 180 days"
- "What's my average heart rate during runs?"
- "Which run had the most laps?"
- "How many miles did I run last week?"

Type `exit` or `quit` to end the chat session.

## Troubleshooting

### Authentication Errors
- Verify your `GARMIN_EMAIL` and `GARMIN_PASSWORD` are correct
- If MFA is enabled, ensure you enter the code when prompted
- Delete `~/.garminconnect` to force a fresh login

### Missing Data
- Ensure you've run `fetch` before using `chat`
- Check that `garmin_data.json` exists and contains data
- Verify you have running activities in your Garmin Connect account

### API Errors
- Verify your `GOOGLE_API_KEY` is valid and has access to Gemini API
- Check your internet connection
- Ensure you haven't exceeded API rate limits

## Project Structure

```
garmin_app/
├── garmin_chat.py          # Main CLI entry point
├── requirements.txt        # Python dependencies
├── garmin_data.json        # Stored activity data (generated)
└── src/
    ├── app.py              # Main application logic
    ├── garmin/
    │   ├── client.py       # Garmin Connect API client
    │   ├── models.py       # Data models
    │   └── storage.py      # File storage utilities
    └── llm/
        ├── client.py       # Google Gemini API client
        └── chat.py         # Chat session management
```

## License

[Add your license information here]

