#!/usr/bin/env python
import os
import re
import gzip
from typing import List, Dict
from uuid import uuid4

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def tarball(file_name: str, output_path: str = "") -> Dict:
    if not output_path:
        output_path: str = re.sub(r"^./", "", file_name).rstrip("/").replace("/", "_")

    tar_ball: str = f"{output_path}_news_middle_east_regions_{str(uuid4())}.tar.gz"

    joined_contents = None
    current_content = None

    if os.path.isdir(file_name):
        contents: List = []
        for root, dirs, content_files in os.walk(file_name):
            for csv_file in content_files:
                current_file_path: str = os.path.join(root, csv_file)
                if os.path.getsize(current_file_path) > 0:
                    contents.append(open(current_file_path, 'r').read())

        joined_contents = '\n'.join(contents).encode('utf-8')

    if os.path.isfile(file_name):
        try:
            current_content = open(file_name, 'r').read().encode('utf-8')

        except IOError as e:
            raise IOError(f"Unable to open {file_name}") from e

    with gzip.open(tar_ball, 'w') as f:
        f.write(joined_contents if joined_contents else current_content)
    f.close()

    return {'file': tar_ball,
            'status': "created" if os.path.exists(tar_ball) else "failed"
           }


def upload_to_drive(cred_file: str,
                   file_name: str,
                   api_scope: str = "https://www.googleapis.com/auth/drive",
                   mimetype: str = 'application/gzip') -> Dict:

    if not os.path.exists(cred_file):
        raise FileNotFoundError(f"Unable to find the following file {cred_file}")

    if not os.path.exists(file_name):
        raise FileNotFoundError(f"Unable to find the following file {file_name}")

    creds = None
    try:
        creds = Credentials.from_authorized_user_file(cred_file)
    except:
        pass

    if not creds and not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_file, api_scope)
            creds = flow.run_local_server(port=58887)

        with open(os.path.join(os.path.expanduser("~/"), cred_file)) as f:
            f.write(creds.to_json())

    google_drive = build('drive', 'v3', credentials=creds)
    media = MediaFileUpload(file_name, mimetype=mimetype, resumable=True)
    file_metadata: Dict = {'name': file_name,
                           'mimeType': 'application/gzip'
                           }
    response = google_drive.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return response