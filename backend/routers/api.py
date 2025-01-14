import time

from fastapi import APIRouter, HTTPException, Path

from services.cti_service import CTIWrapper

cti_wrapper = CTIWrapper()

router = APIRouter()

CMD_TIMEOUT = 30
FEEDBACK_TIMEOUT = 30


@router.post("/login")
async def login(username="admin", password="000000", ipaddress="127.0.0.1", port=9031):
    try:
        login_cmd_sent = False
        start_time = time.time()
        while not login_cmd_sent and (time.time() - start_time) < CMD_TIMEOUT:
            login_cmd_sent = cti_wrapper.login(username, password, ipaddress, port)
            if not login_cmd_sent:
                time.sleep(0.1)

        if not login_cmd_sent:
            raise HTTPException(status_code=500, detail=f"Failed to send login command within {CMD_TIMEOUT} seconds")

        # after login, wait the login feedback
        login_feedback_received = False
        start_time = time.time()
        while not login_feedback_received and (time.time() - start_time) < FEEDBACK_TIMEOUT:
            login_feedback_received = cti_wrapper.login_feedback is not None
            if not login_feedback_received:
                time.sleep(0.1)

        if not login_feedback_received:
            return {
                "success": False,
                "message": "Login failed.",
                "error": "No login feedback received."
            }

        feedback = cti_wrapper.login_feedback
        cti_wrapper.login_feedback = None

        if feedback.result == feedback.ELoginResult.CTI_LOGIN_FAILED:
            return {
                "success": False,
                "message": "Login failed.",
                "error": "CTI Login failed."
            }
        else:
            return {
                "success": True,
                "message": "Login succeed.",
                "feedback": feedback
            }

    except Exception as e:
        return {
            "success": False,
            "message": "An unexpected error occurred.",
            "error": "An unexpected error occurred during login. " + str(e)
        }


@router.post("/logout")
async def logout():
    try:
        cti_wrapper.logout()
        start_time = time.time()
        while cti_wrapper.isConnected() and (time.time() - start_time) < CMD_TIMEOUT:
            time.sleep(0.1)

        if cti_wrapper.isConnected():
            return {"success": False,
                    "message": "Log out failed.",
                    "error": f"Failed to disconnect with the ${CMD_TIMEOUT} seconds."
                    }
        else:
            return {
                "success": True,
                "message": "Log out successfully."
            }

    except Exception as e:
        return {
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }


@router.get("/channels/status")
async def get_channels_status():
    try:
        cmd_send = False
        start_time = time.time()
        while not cmd_send and (time.time() - start_time) < CMD_TIMEOUT:
            cmd_send = cti_wrapper.get_channel_info()
            if not cmd_send:
                time.sleep(0.1)
        if not cmd_send:
            raise HTTPException(status_code=500,
                                detail=f"Failed to send get channel info command within {CMD_TIMEOUT} seconds.")

        feedback_received = False
        start_time = time.time()
        while not feedback_received and (time.time() - start_time) < FEEDBACK_TIMEOUT:
            feedback_received = cti_wrapper.get_channel_info_feedback is not None
            if not feedback_received:
                time.sleep(0.1)

        if not feedback_received:
            return {
                "success": False,
                "message": "Failed to get channel status.",
                "error": "Failed to get channel info"
            }
        else:
            feedback = cti_wrapper.get_channel_info_feedback
            cti_wrapper.get_channel_info_feedback = None
            return {
                "success": True,
                "message": "Get channel status successfully",
                # value will be used as index in the frontend
                "feedback": [{"value":data.channel_index, "status": data.status} for data in feedback.channel_data]
            }

    except Exception as e:
        return {
            "success": False,
            "message": "An unexpected error occurred.",
            "error": "Unexpected error when get channel status" + str(e)
        }


@router.get("/channels/data/{index}")
async def get_channel_data(index: int = Path(...)):
    try:
        cmd_sent = False
        start_time = time.time()
        while not cmd_sent and (time.time() - start_time) < CMD_TIMEOUT:
            cmd_sent = cti_wrapper.get_channel_info(index)
            if not cmd_sent:
                time.sleep(0.1)

        feedback_received = False
        start_time = time.time()
        while not feedback_received and (time.time() - start_time) < FEEDBACK_TIMEOUT:
            feedback_received = cti_wrapper.get_channel_info_feedback is not None
            if not feedback_received:
                time.sleep(0.1)

        if not feedback_received:
            raise HTTPException(status_code=500,
                                detail=f"Failed to get channel info feedback within {FEEDBACK_TIMEOUT} seconds.")
        feedback = cti_wrapper.get_channel_info_feedback
        message = {}
        for data in feedback.channel_data:
            message[data.channel_index] = {}
            message[data.channel_index]['test_time'] = data.test_time
            message[data.channel_index]['step_time'] = data.test_time
            message[data.channel_index]['voltage'] = data.voltage
            message[data.channel_index]['current'] = data.current
            message[data.channel_index]['aux'] = data.aux_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schedules")
async def get_schedules():
    try:
        cmd_sent = False
        start_time = time.time()
        while not cmd_sent and (time.time() - start_time) < CMD_TIMEOUT:
            cmd_sent = cti_wrapper.browse_schedule_file()
            if not cmd_sent:
                time.sleep(0.1)
        if not cmd_sent:
            raise HTTPException(status_code=500,
                                detail=f"Failed to send get schedules command within {CMD_TIMEOUT} seconds.")

        feedback_received = False
        start_time = time.time()
        while not feedback_received and (time.time() - start_time) < FEEDBACK_TIMEOUT:
            feedback_received = cti_wrapper.browse_schedule_file_feedback is not None
            if not feedback_received:
                time.sleep(0.1)

        if not feedback_received:
            return {
                "success": False,
                "message": "Failed to get schedule files.",
                "error": "Failed to get CTI feedback"
            }

        feedback = cti_wrapper.browse_schedule_file_feedback
        cti_wrapper.browse_schedule_file_feedback = None

        if feedback.result == feedback.EResult.CTI_BROWSE_DIRECTORY_FAILED:
            return {
                "success": False,
                "message": "Failed to get schedule files.",
                "error": "CTI internal failure."
            }

        files = [info.parent_dir_path for info in feedback.dir_file_info]
        return {
            "success": True,
            "message": "Schedules fetched successfully.",
            "files": files
        }

    except Exception as e:
        return {
            "success": False,
            "message": "An unexpected error occurred.",
            "error": "Unexpected error occurred, " + str(e)
        }


@router.post("/schedules/assign")
async def assign_schedule(schedule_name: str,
                          barcode: str,
                          capacity: float,
                          MVUD1: float,
                          MVUD2: float,
                          MVUD3: float,
                          MVUD4: float,
                          all_assign: bool = True,
                          channel_index: int = -1):
    try:
        cmd_sent = False
        start_time = time.time()
        while not cmd_sent and (time.time() - start_time) < CMD_TIMEOUT:
            cmd_sent = cti_wrapper.assign_schedule(schedule_name, barcode, capacity,
                                                   MVUD1, MVUD2, MVUD3, MVUD4,
                                                   all_assign, channel_index)
            if not cmd_sent:
                time.sleep(0.1)
        if not cmd_sent:
            raise HTTPException(status_code=500,
                                detail=f"Failed to send assign schedule command within {CMD_TIMEOUT} seconds.")

        feedback_received = False
        start_time = time.time()
        while not feedback_received and (time.time() - start_time) < FEEDBACK_TIMEOUT:
            feedback_received = cti_wrapper.assign_schedule_feedback is not None
            if not feedback_received:
                time.sleep(0.1)

        feedback = cti_wrapper.assign_schedule_feedback
        cti_wrapper.assign_schedule_feedback = None

        if feedback.result == feedback.EAssignToken.CTI_ASSIGN_SUCCESS:
            return {
                "success": True,
                "message": "Assign schedule successfully.",
                "feedback": feedback
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_INDEX:
            return {
                "success": False,
                "message": "Failed to assign schedule.",
                "error": "Assign schedule: Channel index error."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_SCHEDULE_NAME_EMPTY_ERROR:
            return {
                "success": False,
                "message": "Failed to assign schedule",
                "error": "Assign schedule: schedule "
            }
        else:
            return {
                "success": False,
                "message": "Failed to assign the schedule.",
                "error": feedback
            }

    except Exception as e:
        return {
            "success": False,
            "message": "An unexpected error occurred.",
            "error": "Unexpected error occurred, " + str(e)
        }


@router.post("/channels/start")
async def start_channel(test_name: str, channels: list[int]):
    try:
        cmd_sent = False
        start_time = time.time()
        while not cmd_sent and (time.time() - start_time) < CMD_TIMEOUT:
            cmd_sent = cti_wrapper.start_channel(test_name, channels)
            if not cmd_sent:
                time.sleep(0.1)
        if not cmd_sent:
            raise HTTPException(status_code=500,
                                detail=f"Failed to send start channel command within {CMD_TIMEOUT} seconds.")

        feedback_received = False
        start_time = time.time()
        while not feedback_received and (time.time() - start_time) < FEEDBACK_TIMEOUT:
            feedback_received = cti_wrapper.start_channel_feedback is not None
            if not feedback_received:
                time.sleep(0.1)

        feedback = cti_wrapper.start_channel_feedback
        if feedback.result == feedback.EStartToken.CTI_START_SUCCESS:
            return {
                "success": True,
                "message": "Channel started successfully.",
                "feedback": feedback
            }
        elif feedback.result == feedback.EStartToken.CTI_START_INDEX:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": "Channel Index Error."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_ERROR:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": "Channel Execution Error."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_CHANNEL_RUNNING:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": "Channel is running."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_CHANNEL_NOT_CONNECT:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": "Channel not connected."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_SCHEDULE_VALID:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": "Schedule is not valid."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_NO_SCHEDULE_ASSIGNED:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": "No Assigned Schedules."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_AUX_CHANNEL_MAP:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": "Aux Mapping error."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_TESTNAME_TOO_LONG:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": "Test name is too long."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_CSV_WAIT_TIME:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": "Please wait 45s util csv file finished writing."
            }
        else:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": f"Error occurs, feedback: {feedback.result}"
            }

    except Exception as e:
        return {
            "success": False,
            "message": "Failed to start channels. An unexpected error occurred.",
            "error": str(e)
        }


@router.post("/channels/stop")
async def stop_channel(channel: int, is_stop_all: bool = False):
    try:
        cmd_sent = False
        start_time = time.time()
        while not cmd_sent and (time.time() - start_time) < CMD_TIMEOUT:
            cmd_sent = cti_wrapper.stop_channel(channel, is_stop_all)
            if not cmd_sent:
                time.sleep(0.1)
        if not cmd_sent:
            raise HTTPException(status_code=500,
                                detail=f"Failed to send stop channel command within {CMD_TIMEOUT} seconds.")

        feedback_received = False
        start_time = time.time()
        while not feedback_received and (time.time() - start_time) < FEEDBACK_TIMEOUT:
            feedback_received = cti_wrapper.stop_channel_feedback is not None
            if not feedback_received:
                time.sleep(0.1)

        feedback = cti_wrapper.stop_channel_feedback
        cti_wrapper.stop_channel_feedback = None
        if feedback == feedback.EStopToken.SUCCESS:
            return {
                "success": True,
                "message": "Channel stopped successfully.",
                "feedback": feedback
            }
        else:
            return {
                "success": False,
                "message": "Failed to stop channel.",
                "error": f"Failed to stop channel, feedback is {feedback.result}"
            }

    except Exception as e:
        return {
            "success": False,
            "message": "Failed to stop channels. An unexpected error occurred.",
            "error": str(e)
        }
