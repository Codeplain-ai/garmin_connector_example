
# Setting up requirements:
You need to setup three environment variables
- `GOOGLE_API_KEY` - The API key for Gemini
- `GARMIN_EMAIL`, `GARMIN_PASSWORD` - The credentials for logging in with your Garmin Account.

These don't leave your computer.

## Google API Key
Get the API key by:
1. Go to https://aistudio.google.com/
2. Click on `Dashboard` on the right side panel
3. Click `API Keys`
4. Copy the API key if available or click `Create API Key` on the upper left.
5. Export the API key to the `GOOGLE_API_KEY` environment variable.

## Garmin credentials
Export the `GARMIN_EMAIL` and `GARMIN_PASSWORD` environment variables with your Garmin login credentials.

# Rendering the example

To start the rendering simply run:
```
codeplain garmin_cli.plain
```
Make sure that the `GARMIN_EMAIL`, `GARMIN_PASSWORD` and `GOOGLE_API_KEY` environment variables are set.


# Prerendered Code:

A ***plain implementation of a Garmin connector, that connects Garmin data to an LLM an lets you talk to your data.

The pre-rendered code is available in `./garmin_app/`
