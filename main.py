from dotenv import load_dotenv
from src.email_responder import send_email
from src.ollama_wrapper import extract_fields_with_mistral
from src.form_filler import submit_google_form
from config import REQUIRED_FIELDS
from src.email_reader import (
    get_email_service,
    get_latest_unprocessed_email,
    mark_as_processed,
    create_label_if_not_exists
)
import os


load_dotenv()

def format_summary(result, missing):
    received = []
    for field in REQUIRED_FIELDS:
        value = result.get(field)
        if value and field not in missing:
            received.append(f"- {field}: {value}")
    missing_lines = [f"- {field}" for field in missing]

    summary = f"""Hi {result.get('Trainer Name', '')},

    We received your session request, but a few details are missing. Here's a summary:

    Session Details Received:
    {chr(10).join(received) if received else "None"}

    Missing Fields:
    {chr(10).join(missing_lines)}

    Please resend the missing information so we can process your session request.

    Thanks!
    HR Team
    """
    return summary




def main():
    print("Starting Email Analyser...")
    service = get_email_service()
    print("Gmail service authenticated.")
    hr_email = os.getenv("HR_EMAIL")
    print(f"Reading latest email sent to HR ({hr_email})...")
    
    create_label_if_not_exists(service)
    from_email, body, thread_id, message_id, msg_id = get_latest_unprocessed_email(service, hr_email)



    if not body:
        print("No email found.")
        return

    print("Email content received. Passing to Mistral...")
    result = extract_fields_with_mistral(body)

    if not result:
        print("Mistral failed.")
        return

    missing = result.get("Missing Fields", [])
    # if missing and missing != ["None"]:
    #     print("Missing fields detected:", missing)
    #     msg = f"Hi,\n\nWe couldn't process your request because the following fields are missing:\n" + \
    #           "\n".join(missing) + "\n\nPlease resend the complete information.\n\nThanks!"
    #     send_email(service, from_email, "Missing Information", msg, thread_id, message_id)

    # then use:
    if missing and missing != ["None"]:
        msg = format_summary(result, missing)
        send_email(service, from_email, "Re: Training Request – Missing Info", msg, thread_id, message_id)
        mark_as_processed(service, msg_id)

    else:
        print("All required fields present. Pre-filling Google Form...")
        submit_google_form(result)
        send_email(service, from_email, "Session Recorded", "Your session request has been processed!", thread_id, message_id)
        mark_as_processed(service, msg_id)


    print("Email processing complete!")

if __name__ == "__main__":
    main()
