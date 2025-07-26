import argparse
import requests
import json
import os

# You'll need to install the 'requests' library: pip install requests

def main():
    parser = argparse.ArgumentParser(description="Ask a question to the RAG pipeline.")
    parser.add_argument("query", type=str, help="The question to ask.")
    args = parser.parse_args()

    # Define the API endpoint URL
    API_URL = "http://127.0.0.1:8000/ask"

    # Create the payload for the POST request
    payload = {
        "user": "cli_user", # A dummy user for command line interface
        "query": args.query
    }

    print(f"DEBUG: Attempting to send POST request to {API_URL} with payload: {payload}") # Debug print

    try:
        # THIS IS THE CRITICAL LINE: Using requests.post()
        response = requests.post(API_URL, json=payload)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        result = response.json()

        # Print the result from the server
        print("\nAnswer:", result.get("answer"))
        print("\nRetrieved Chunks:")
        for i, chunk_text in enumerate(result.get("retrieved_chunks", [])):
            print(f"  Chunk {i+1}: {str(chunk_text)[:100]}...")
        print("\nChat History:", result.get("chat_history"))

    except requests.exceptions.ConnectionError as e:
        print(f"ERROR: Could not connect to the API server at {API_URL}.")
        print("Please ensure your FastAPI server is running in a separate terminal and is accessible.")
        print(f"Details: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP request failed with status code {response.status_code}.")
        print(f"Server Response Content: {response.text}") # Print full server response
        print(f"Details: {e}")
    except json.JSONDecodeError:
        print(f"ERROR: Failed to decode JSON response from server. Response text: {response.text}")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()