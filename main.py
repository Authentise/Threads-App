#!/usr/bin/env python3

import requests
import sys

BASE_URL = "https://api.threads.dev-auth2.com/v1"

# Request session for API calls
session = requests.session()

def login(username: str, password: str) -> bool:
    # Log in, and save cookie in the session
    response = session.post(f"{BASE_URL}/auth/login/", json={"email": username, "password": password})
    return response.status_code == 200

def main():
    # Retrieve email and password from command line args
    if len(sys.argv) != 3:
        print("Usage: python3 <filename.py> <email> <password>")
        sys.exit(1)
    email = sys.argv[1]
    password = sys.argv[2]

    # Authenticate
    login(email, password)

    # Ready to start using the API!

    # Retrieve your threads
    threads = session.get(f"{BASE_URL}/threads").json()


def get_reference(id: int):
    response = session.get(f"{BASE_URL}/references/{id}")

    # A reference can either be a URL, or a file. File references contain multiple versions:
    versions = response.json()["file_versions"]

    # We can download the first version of the file
    file_response = session.get(versions[0]["file"])

    # Now we have the file data!
    file = file_response.text

def post_comment(thread_id: int, message: str):
    session.post(
        # POST requests must end in a forward slash
        f"{BASE_URL}/messages/", 
        json={"text": _format_message(message), "thread": thread_id}, 
        # When sending POST requests, you must include the CSRF token in the header
        headers={**_required_headers()}
    )

    # You've just posted a comment! You can retrieve the thread's messages to verify
    messages = session.get(
        # POST requests must end in a forward slash
        f"{BASE_URL}/threads/{thread_id}/messages", 
    ).json()

def upload_new_reference(thread_id: int, name: str, filename: str):
    # Open up the file
    with open(filename, "rb") as f:
        session.post(
            f"{BASE_URL}/references/", 
            # Uploading references uses multipart form content types
            files={'file': f},
            data={"name": name, "thread": thread_id, "reference_type": "FILE"}, 
            headers={**_required_headers()}
        )

def upload_reference_version(reference_id: int, name: str, filename: str):
    with open(filename, "rb") as f:
        session.patch(
            f"{BASE_URL}/references/{reference_id}/", 
            # Uploading references uses multipart form content types
            files={'file': f},
            data={"name": name, "id": reference_id}, 
            headers={**_required_headers()}
        )


def _required_headers() -> dict:
    return {"x-csrftoken": session.cookies.get("csrftoken")}

def _format_message(message: str) -> str:
    return '{"blocks":[{"key":"1blqq","text":"' + message + '","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{}}'
    

if __name__ == "__main__":
    main()
