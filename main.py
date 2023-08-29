import os.path
from pprint import pprint

from environs import Env
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_credentials(credentials_path):
    credentials = None

    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    return credentials


def main():
    env = Env()
    env.read_env()

    credentials = get_credentials(env.str("GMAIL_CREDENTIALS"))

    try:
        service = build("gmail", "v1", credentials=credentials)
        response = service.users().messages().list(userId="me").execute()
        headers = ("Date", "From", "Subject")
        for message in response["messages"][:5]:
            msg = {}
            raw_message = service.users().messages().get(userId="me", id=message["id"]).execute()
            msg["snippet"] = raw_message["snippet"]
            for header in raw_message["payload"]["headers"]:
                if header["name"] in headers:
                    msg[header["name"].lower()] = header["value"]

            pprint(msg)
            print()

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
