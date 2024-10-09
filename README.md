# Threads API 

This is the base repo for creating a Threads App. You should fork this repo, and upload your submission to Github.

## API Docs

You will interact with Threads via it's JSON API. See [the Swagger doc](https://api.threads.dev-auth2.com/swagger/) for a list of the available endpoints and their schemas

## Getting Started

### Pre-requisites

This walkthrough assumes you're using Unix, and already have `python` and [`poetry`](https://python-poetry.org/docs/#installation) installed.

You should already have your Threads credentials. If not, contact <EMAIL> for help.

Once you have those installed, fork this repo, and clone your forked copy.

### Project Structure

Source code is found in the `src` folder. 

Your entrypoint will be the function called `handler()` in `src/handler.py`. Please do not change this functions arguments, and make sure it returns a dict. Please do not edit the `src/main.py` and `src/utils.py` files.

You are free to add new files in the `src` directory and import them as needed. You can add new 

### Running the Application

Use poetry to run the script:
```bash
poetry run python3 src/main.py <email> <password> --kwargs arg1=value1 arg2=value2
```

Alternatively, you can spawn a virtual-env loaded shell via poetry:

```bash
poetry shell
(venv) python3 src/main.py ...
```

When you run the `src/main.py` script, a wrapper function will parse command line args, and authenticate with the Threads API, and call your handler function.


### Command Line Args

You need to supply your username and password as command line args to be able to authenticate with the API. If you'd like to pass in additional information from the command line, you can supply key-value pairs like so:

```bash
... --kwargs arg1=value1 arg2=value
```

## Code Examples

You can find these examples in the `src/handler.py` file.

### References

References are files or links that can be uploaded to a thread. Here's an example of retrieving a reference and downloading it's file:

```python
# Retrieves a reference
def get_reference(id: int):
    response = session.get(f"{BASE_URL}/references/{id}")

    # A reference can either be a URL, or a file. File references contain multiple versions:
    versions = response.json()["file_versions"]

    # We can download the first version of the file
    file_response = session.get(versions[0]["file"])

    # Now we have the file data!
    file = file_response.text
```

You can either upload a file to a thread as a new reference, or upload it as a new version to an existing reference:

```python
def upload_new_reference(thread_id: int, name: str, filename: str):
    # Open up the file
    with open(filename, "rb") as f:
        session.post(
            # POST requests must end in a forward slash
            f"{BASE_URL}/references/", 
            # Uploading references uses multipart form content types
            files={'file': f},
            data={"name": name, "thread": thread_id, "reference_type": "FILE"}, 
            # See below
            headers={**_required_headers()}
        )

def upload_reference_version(reference_id: int, name: str, filename: str):
    with open(filename, "rb") as f:
        session.patch(
            # POST requests must end in a forward slash
            f"{BASE_URL}/references/{reference_id}/", 
            # Uploading references uses multipart form content types
            files={'file': f},
            data={"name": name, "id": reference_id}, 
            # See below
            headers={**_required_headers()}
        )

# Required when performing non-GET requests
def _required_headers() -> dict:
    return {"x-csrftoken": session.cookies.get("csrftoken")}
```

### Messages

Messages can be uploaded to a thread:

```python
def post_message(thread_id: int, message: str):
    session.post(
        # POST requests must end in a forward slash
        f"{BASE_URL}/messages/", 
        json={"text": _format_message(message), "thread": thread_id}, 
        # When sending POST requests, you must include the CSRF token in the header
        headers={**_required_headers()}
    )

    # You've just posted a message! You can retrieve the thread's messages to verify
    get_messages(thread_id)

def get_messages(thread_id: int):
    messages = session.get(
        f"{BASE_URL}/threads/{thread_id}/messages", 
    ).json()

# Messages must be formatted in this way before uploading
def _format_message(message: str) -> str:
    return '{"blocks":[{"key":"1blqq","text":"' + message + '","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{}}'
```

