import requests


# ============================================================
# IMPORTANT: Ensure that FastAPI is running before executing this code!
# ============================================================

def login(request_payload):
    """
    Perform user login.
    :param request_payload: A dictionary containing the login credentials.
                            Expected keys: "username", "password", "ipaddress" and "port"(optional).

    :return: print the feedback login.
    """
    ip_address = request_payload.get("ipaddress", "127.0.0.1")
    port = 8000  # Must match the port where FastAPI is running
    base_url = f"http://{ip_address}:{port}"
    login_url = f"{base_url}/login"

    try:
        response = requests.post(login_url, json=request_payload)
        response_data = response.json()

        if response_data["success"]:
            print("Login successfully.")
        else:
            print(f"Login failed. Error: {response_data['error']}")

        print(response_data)
    except Exception as e:
        print("An Unexpected Error Occurred: ", e)


if __name__ == "__main__":
    payload = {
        "username": "admin",
        "password": "000000",
        "ipaddress": "127.0.0.1"
    }
    login(payload)
