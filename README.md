# EmailAnalyser

## Overview

**EmailAnalyser** is an automation tool that reads incoming training/session request emails from a Gmail inbox, extracts structured information using an LLM (Mistral via Ollama), and automates responses and Google Form submissions. It is designed for HR or training teams to streamline the intake and processing of training session requests.

## Features
- Authenticates with Gmail API to read and send emails
- Extracts required fields from email content using a local LLM (Mistral via Ollama)
- Replies to the sender if information is missing
- Submits complete requests to a Google Form automatically
- Marks processed emails with a custom Gmail label

## Required Fields
The following fields are extracted from emails and required for a valid session request:
- Trainer Name
- Session Topic
- Date
- Time
- Duration
- Mode

## Setup

### 1. Clone the Repository
```bash
git clone <repo-url>
cd EmailAnalyser
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Google API Credentials
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a project and enable the Gmail API
- Create OAuth 2.0 credentials (Desktop or Web)
- Download the credentials file as `credentials.json` and place it in the project root

### 4. Environment Variables
Create a `.env` file in the project root with the following:
```
HR_EMAIL=your-hr-email@domain.com
# GOOGLE_FORM_ID=your-google-form-id (not currently used, see below)
```
- `HR_EMAIL`: The email address to monitor for incoming requests.
- `GOOGLE_FORM_ID`: (Optional) The Google Form ID. The form URL is currently hardcoded in `src/form_filler.py`.

### 5. Ollama & Mistral
- [Install Ollama](https://ollama.com/) and ensure the `ollama` CLI is available.
- Download the Mistral model for local inference (see Ollama docs).

### 6. First Run & Authentication
On first run, the app will open a browser window to authenticate with your Google account and create `token.json`.

## Usage

Run the main script:
```bash
python main.py
```

- The script will:
  1. Read the latest unprocessed training request email sent to the HR email.
  2. Extract required fields using Mistral (via Ollama).
  3. If any fields are missing, reply to the sender with a summary and request for missing info.
  4. If all fields are present, submit the data to a Google Form and notify the sender.
  5. Mark the email as processed with a Gmail label.

## File Structure
- `main.py` — Entry point, orchestrates the workflow
- `src/email_reader.py` — Gmail API integration, email fetching, and label management
- `src/email_responder.py` — Sending replies via Gmail API
- `src/ollama_wrapper.py` — LLM prompt and extraction logic (Mistral via Ollama)
- `src/form_filler.py` — Submits data to Google Form
- `config.py` — List of required fields

## Dependencies
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- python-dotenv
- openai (for compatibility, not directly used)
- requests

## Notes
- The Google Form URL is currently hardcoded in `src/form_filler.py`. To use a different form, update the URL and field entry IDs accordingly.
- Only emails with the subject "Training Request" are processed.
- Only the latest unprocessed email is handled per run.

## License
MIT (or specify your license) 