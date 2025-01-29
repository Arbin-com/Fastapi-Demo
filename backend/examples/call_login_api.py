import requests

BASE_URL = "http://127.0.0.1:8000"


def login():
    url = f"{BASE_URL}/login"
    payload = {
        "username": "admin",
        "password": "000000",
        "ipadress": "127.0.0.1",
    }
    try:
        response = requests.post(url, json=payload)
        response_data = response.json()

        if response_data["success"]:
            print("Login successfully.")
        else:
            print("Login failed.")

        print(response_data)
    except requests.exceptions.RequestException as e:
        print("API Request Error:", e)


if __name__ == "__main__":
    login()
