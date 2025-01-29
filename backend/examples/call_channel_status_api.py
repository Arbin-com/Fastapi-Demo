import requests


# ============================================================
# # IMPORTANT: Ensure FastAPI is running and the user is logged in before executing this code!
# ============================================================

def get_channel_status(base_url):
    """
    Retrieve the channel status from the FastAPI application using its IP address.
    :param base_url: The base URL of the FastAPI application
    :return Print the channel status
    """

    url = f"{base_url}/channels/status"
    try:
        response = requests.get(url=url)
        response_data = response.json()

        if response_data["success"]:
            print("Get channel status successfully")
        else:
            print(f"Failed to get channel status, {response_data['error']}", )

        print(response_data)
    except Exception as e:
        print("An Unexpected Error Occurred: ", e)


if __name__ == "__main__":
    get_channel_status("http://127.0.0.1:8000")