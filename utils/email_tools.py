import os
import pickle

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# from encode the message in base64
from base64 import urlsafe_b64encode

# for dealying with attachement MIME types
from email.message import EmailMessage


def gmail_authenticate():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.valid and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Send messages only. No read or modify privileges on mailbox.
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", ["https://www.googleapis.com/auth/gmail.send"]
            )
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("gmail", "v1", credentials=creds)


def build_message(our_email, kindle_email, subject, body, article_filename):
    message = EmailMessage()
    message["subject"] = subject
    message["to"] = kindle_email
    message["from"] = our_email
    message.set_content(body)
    with open(article_filename, "rb") as content_file:
        content = content_file.read()
        message.add_attachment(
            content,
            maintype="application",
            subtype="epub",
            filename=article_filename.split("/")[-1],
        )
    return {"raw": urlsafe_b64encode(message.as_bytes()).decode()}


def send_article(service, our_email, destination, obj, body, article_filename=""):
    return (
        service.users()
        .messages()
        .send(
            userId="me",
            body=build_message(our_email, destination, obj, body, article_filename),
        )
        .execute()
    )
