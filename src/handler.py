import requests
from utils import required_headers, format_message, BASE_URL


# Entrypoint of your application. Do not change this function's signature (args and return types)
def handler(session: requests.Session, kwargs: dict) -> dict:
    # E.g Retrieve all threads
    # threads = session.get(f"{BASE_URL}/threads/").json()

    # Return a dict to be printed to the console, if needed
    return {}

"""
Examples

Below are some examples of interacting with the API to get you started
"""

# Retrieve a reference by it's id and the contents of it's file
def get_reference(session: requests.Session, id: int):
    response = session.get(f"{BASE_URL}/references/{id}")

    # A reference can either be a URL, or a file. File references contain multiple versions:
    versions = response.json()["file_versions"]

    # We can download the first version of the file
    file_response = session.get(versions[0]["file"])

    # Now we have the file data!
    file = file_response.text

# Upload a new reference (with file) to a thread
def upload_new_reference(session: requests.Session, thread_id: int, name: str, filename: str):
    # Open up the file
    with open(filename, "rb") as f:
        session.post(
            # POST requests must end in a forward slash
            f"{BASE_URL}/references/", 
            # Uploading references uses multipart form content types
            files={'file': f},
            data={"name": name, "thread": thread_id, "reference_type": "FILE"}, 
            # See below
            headers={**required_headers(session)}
        )

# Upload a new version of a reference to a thread
def upload_reference_version(session: requests.Session, reference_id: int, name: str, filename: str):
    with open(filename, "rb") as f:
        session.patch(
            # POST requests must end in a forward slash
            f"{BASE_URL}/references/{reference_id}/", 
            # Uploading references uses multipart form content types
            files={'file': f},
            data={"name": name, "id": reference_id}, 
            # See below
            headers={**required_headers(session)}
        )

# Post a message to a thread
def post_message(session: requests.Session, thread_id: int, message: str):
    session.post(
        # POST requests must end in a forward slash
        f"{BASE_URL}/messages/", 
        json={"text": format_message(message), "thread": thread_id}, 
        # When sending POST requests, you must include the CSRF token in the header
        headers={**required_headers(session)}
    )

    # You've just posted a message! You can retrieve the thread's messages to verify
    get_messages(session, thread_id)


# Retrieve a thread's messages
def get_messages(session: requests.Session, thread_id: int):
    messages = session.get(
        f"{BASE_URL}/threads/{thread_id}/messages", 
    ).json()
