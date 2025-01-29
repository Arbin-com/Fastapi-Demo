import requests


# ============================================================
# # IMPORTANT: Ensure FastAPI is running and the user is logged in before executing this code!
# ============================================================

def assign_schedule(base_url, schedule_name, channel_index):
    """
    Assign a schedule to a specific channel.
    :param base_url: The base URL of the FastAPI application
    :param schedule_name: The name of the schedule, including its suffix.
    :param channel_index: The index of the target channel (starting from 0).
    :return: print an error message or feedback.
    """
    url = f"{base_url}/schedules/assign"
    payload = {
        "schedule_name": schedule_name,
        "channel_index": channel_index
    }

    try:
        response = requests.post(url=url, json=payload)
        response_data = response.json()

        if response_data["success"]:
            print("Assign schedule successfully.")
        else:
            print(f"Failed to assign schedule. Error: {response_data["error"]}")

        print(response_data)
    except Exception as e:
        print("An Unexpected Error Occurred: ", e)


if __name__ == "__main__":
    assign_schedule("http://127.0.0.1:8000", "Schedule_1.sdx", 0)