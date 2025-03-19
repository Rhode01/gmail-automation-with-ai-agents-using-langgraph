from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import List
BASE_DIR = os.path.dirname(__file__)
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")

class GmailAuth(BaseSettings):
    CLIENT_SECRET_FILE: str
    API_SERVICE_NAME: str
    API_VERSION: str
    SCOPES: List[str]
    PREFIX: str  
    model_config = SettingsConfigDict(env_file=ENV_PATH)
    def create_service(self):
        working_dir = os.getcwd()
        token_dir = "token_files"
        token_file = f"token_{self.API_SERVICE_NAME}_{self.API_VERSION}{self.PREFIX}.json"
        token_path = os.path.join(working_dir, token_dir, token_file)
        os.makedirs(os.path.join(working_dir, token_dir), exist_ok=True)

        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_SECRET_FILE, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
                with open(token_path, "w") as token:
                    token.write(creds.to_json())

        try:
            service = build(
                self.API_SERVICE_NAME,
                self.API_VERSION,
                credentials=creds,
                static_discovery=False
            )
            print("Authentication successful")
            return service
        except HttpError as error:
            if os.path.exists(token_path):
                os.remove(token_path)
            print(f"An error occurred: {error}")
            return None
