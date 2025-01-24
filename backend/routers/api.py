import time

from fastapi import APIRouter, HTTPException, Path

from services.cti_service import CTIWrapper
from services.cti_model import StartChannelRequest, AssignScheduleRequest, StopChannelRequest, StopChannelResponse, \
    AssignFileRequest

cti_wrapper = CTIWrapper()

router = APIRouter()

CMD_TIMEOUT = 3
FEEDBACK_TIMEOUT = 3


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
                "error": f"Failed to get channel info within {FEEDBACK_TIMEOUT} seconds"
            }
        else:
            feedback = cti_wrapper.get_channel_info_feedback
            cti_wrapper.get_channel_info_feedback = None
            return {
                "success": True,
                "message": "Get channel status successfully",
                # value will be used as index in the frontend
                "feedback": [{"value": data.channel_index, "status": data.status} for data in feedback.channel_data]
            }

    except Exception as e:
        return {
            "success": False,
            "message": "An unexpected error occurred.",
            "error": "Unexpected error when get channel status, " + str(e)
        }


# TODO:
@router.get("/channels/data/{index}")
async def get_channel_data(index: int = Path(...)):
    try:
        cmd_sent = False
        start_time = time.time()
        while not cmd_sent and (time.time() - start_time) < CMD_TIMEOUT:
            cmd_sent = cti_wrapper.get_channel_info(channel_index=index)
            if not cmd_sent:
                time.sleep(0.1)

        feedback_received = False
        start_time = time.time()
        while not feedback_received and (time.time() - start_time) < FEEDBACK_TIMEOUT:
            feedback_received = cti_wrapper.get_channel_info_feedback is not None
            if not feedback_received:
                time.sleep(0.1)

        if not feedback_received:
            return {
                "success": False,
                "message": "Failed to get channel data.",
                "error": f"Failed to load data within {FEEDBACK_TIMEOUT} seconds."
            }

        feedback = cti_wrapper.get_channel_info_feedback
        cti_wrapper.get_channel_info_feedback = None
        print("The fetch data feedback is: ",
              [{"channel_index": data.channel_index, "test_time": data.test_time, "step_time": data.step_time,
                "voltage": data.voltage, "current": data.current, "temp": data.auxs} for data in
               feedback.channel_data if data.channel_index == index])

        return {
            "success": True,
            "message": "Get channel data successfully.",
            "feedback": [{"channel_index": data.channel_index, "test_time": data.test_time, "step_time": data.step_time,
                          "voltage": data.voltage, "current": data.current,
                          "temp": data.auxs[1][0].value if data.auxs and len(data.auxs) > 1 and len(
                              data.auxs[1]) > 0 else None} for data in
                         feedback.channel_data if data.channel_index == index]
        }

    except Exception as e:
        return {
            "success": False,
            "message": "An unexpected error occurred.",
            "error": "Unexpected error when load data" + str(e)
        }


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
            feedback_received = cti_wrapper.browse_file_feedback is not None
            if not feedback_received:
                time.sleep(0.1)

        if not feedback_received:
            return {
                "success": False,
                "message": "Failed to get schedule files.",
                "error": "Failed to get CTI feedback"
            }

        feedback = cti_wrapper.browse_file_feedback
        cti_wrapper.browse_file_feedback = None

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
            "feedback": files
        }

    except Exception as e:
        return {
            "success": False,
            "message": "An unexpected error occurred.",
            "error": "Unexpected error occurred, " + str(e)
        }


@router.post("/schedules/assign")
async def assign_schedule(request: AssignScheduleRequest):
    try:
        schedule_name = request.schedule_name
        barcode = request.barcode
        capacity = request.capacity
        MVUD1 = request.MVUD1
        MVUD2 = request.MVUD2
        MVUD3 = request.MVUD3
        MVUD4 = request.MVUD4
        all_assign = request.all_assign
        channel_index = request.channel_index

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


@router.get("/test_objects")
async def get_test_objects():
    try:
        cmd_sent = False
        start_time = time.time()
        while not cmd_sent and (time.time() - start_time) < CMD_TIMEOUT:
            cmd_sent = cti_wrapper.browse_test_object_file()
            if not cmd_sent:
                time.sleep(0.1)
        if not cmd_sent:
            raise HTTPException(status_code=500,
                                detail=f"Failed to send get test object command within {CMD_TIMEOUT} seconds.")

        feedback_received = False
        start_time = time.time()
        while not feedback_received and (time.time() - start_time) < FEEDBACK_TIMEOUT:
            feedback_received = cti_wrapper.browse_file_feedback is not None
            if not feedback_received:
                time.sleep(0.1)

        if not feedback_received:
            return {
                "success": False,
                "message": "Failed to get test object files.",
                "error": "Failed to get CTI feedback when retrieving test objects."
            }

        feedback = cti_wrapper.browse_file_feedback
        cti_wrapper.browse_file_feedback = None

        if feedback.result == feedback.EResult.CTI_BROWSE_DIRECTORY_FAILED:
            return {
                "success": False,
                "message": "Failed to get schedule files.",
                "error": "CTI internal failure."
            }

        files = [info.parent_dir_path for info in feedback.dir_file_info]
        return {
            "success": True,
            "message": "Test objects fetched successfully.",
            "feedback": files
        }

    except Exception as e:
        return {
            "success": False,
            "message": "An unexpected error occurred.",
            "error": "Unexpected error occurred, " + str(e)
        }


@router.post("/test_objects/assign")
async def assign_test_objects(request: AssignFileRequest):
    try:
        file_name = request.file_name
        all_assign = request.all_assign
        file_type = request.file_type
        channels = request.channels
        print(f"In the api, file_type is ", file_type)
        print(f"In the api, channels are ", channels)

        cmd_sent = False
        start_time = time.time()
        while not cmd_sent and (time.time() - start_time) < CMD_TIMEOUT:
            cmd_sent = cti_wrapper.assign_file(file_name, all_assign, file_type, channels)
            if not cmd_sent:
                time.sleep(0.1)
        if not cmd_sent:
            raise HTTPException(status_code=500,
                                detail=f"Failed to send Assign Files command within {CMD_TIMEOUT} seconds.")

        feedback_received = False
        start_time = time.time()
        print(f"currently, feedback should be None, feedback is ", cti_wrapper.assign_file_feedback)
        while not feedback_received and (time.time() - start_time) < FEEDBACK_TIMEOUT:
            feedback_received = cti_wrapper.assign_file_feedback is not None
            if not feedback_received:
                time.sleep(0.1)

        if not feedback_received:
            return {
                "success": False,
                "message": "Failed to assign files.",
                "error": f"Failed to get CTI feedback when assign files, file type is: {file_type}"
            }

        feedback = cti_wrapper.assign_file_feedback
        cti_wrapper.assign_file_feedback = None

        if feedback.result == feedback.EAssignToken.CTI_ASSIGN_SUCCESS:
            return {
                "success": True,
                "message": "Assign files successfully",
                "feedback": feedback
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_FAILED:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "Failed to assign files."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_INDEX:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "Channel Index error."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_ERROR:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "Execution error."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_FILE_NAME_EMPTY_ERROR:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "File name is empty."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_FILE_NOT_FIND_ERROR:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "File not found."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_CHANNEL_RUNNING_ERROR:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "Channel is running."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_CHANNEL_DOWNLOAD_ERROR:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "Execution error."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_BACTH_FILE_OPENED:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "Batch File opened."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_FILE_CANNOT_ASSIGN:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "Error occurred during file assign."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_FILE_SAVE_FAILED:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "File saved error."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_FILE_UNSUPPORTED_FILE_TYPE:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "Unsupported file type."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_FILE_NOT_ASSIGN_SCHEDULE:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "Schedule is not assigned."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_FILE_SCHEDULE_NOT_AUX_REQUIREMENT:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "Schedule does not contain aux requirements"
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_FILE_SCHEDULE_IS_RUNNING:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "Schedule is running."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_SCHEDULE_MUID_NOT_SAME:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "MUID mismatch."
            }
        elif feedback.result == feedback.EAssignToken.CTI_ASSIGN_FILE_CLEAR:
            return {
                "success": False,
                "message": "Failed to assign files",
                "error": "file cleared."
            }

    except Exception as e:
        return {
            "success": False,
            "message": "An unexpected error occurred.",
            "error": "Unexpected error occurred, " + str(e)
        }


@router.post("/channels/start")
async def start_channel(request: StartChannelRequest):
    try:
        test_name = request.test_name
        channels = request.channels
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
                "message": "Failed to start channels. Channel is running.",
                "error": "Channel is running."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_CHANNEL_NOT_CONNECT:
            return {
                "success": False,
                "message": "Failed to start channels. Channel not connected.",
                "error": "Channel not connected."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_SCHEDULE_VALID:
            return {
                "success": False,
                "message": "Warning: Schedule is not valid.",
                "error": "Schedule is not valid."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_NO_SCHEDULE_ASSIGNED:
            return {
                "success": False,
                "message": "Failed to start channels. No Assigned Schedules.",
                "error": "No Assigned Schedules."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_SCHEDULE_VERSION:
            return {
                "success": False,
                "message": "Warning: Schedule version is not consistent",
                "error": "Schedule version not consistent"
            }

        elif feedback.result == feedback.EStartToken.CTI_START_POWER_PROTECTED:
            return {
                "success": False,
                "message": "Warning: Power is protected.",
                "error": "Power is protected."
            }

        elif feedback.result == feedback.EStartToken.CTI_START_RESULTS_FILE_SIZE_LIMIT:
            return {
                "success": False,
                "message": "Warning: The RESULTS file is too large to open.",
                "error": "The RESULTS file is too large to open"
            }
        elif feedback.result == feedback.EStartToken.CTI_START_STEP_NUMBER:
            return {
                "success": False,
                "message": "Warning: Step number Error.",
                "error": "Step number Error."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_NO_CAN_CONFIGURATON_ASSIGNED:
            return {
                "success": False,
                "message": "Warning: No CAN configuration assign error.",
                "error": "No CAN configuration assign error."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_AUX_CHANNEL_MAP:
            return {
                "success": False,
                "message": "Warning: Aux Mapping error.",
                "error": "Aux Mapping error."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_BUILD_AUX_COUNT:
            return {
                "success": False,
                "message": "Warning: In Schedule file, AUX channel Number error.",
                "error": "In Schedule file AUX channel Number error."
            }

        elif feedback.result == feedback.EStartToken.CTI_START_POWER_CLAMP_CHECK:
            return {
                "success": False,
                "message": "Warning: PowerClamp the difference between the highest and the lowest values is zero.",
                "error": "PowerClamp the difference between the highest and the lowest values is zero"
            }

        elif feedback.result == feedback.EStartToken.CTI_START_AI:
            return {
                "success": False,
                "message": "Warning: In Schedule file AUX AI Map IV error.",
                "error": "In Schedule file AUX AI Map IV error."
            }

        elif feedback.result == feedback.EStartToken.CTI_START_SAFOR_GROUPCHAN:
            return {
                "success": False,
                "message": "Warning: Safor Groupchan. ",
                "error": "Safor Groupchan."
            }

        elif feedback.result == feedback.EStartToken.CTI_START_BT6000RUNNINGGROUP:
            return {
                "success": False,
                "message": "Warning: Bt6000 running group.",
                "error": "Bt6000 running group."
            }

        elif feedback.result == feedback.EStartToken.CTI_START_CHANNEL_DOWNLOADING_SCHEDULE:
            return {
                "success": False,
                "message": "Warning: Downloading schedule.",
                "error": "Downloading schedule."
            }

        elif feedback.result == feedback.EStartToken.CTI_START_DATABASE_QUERY_TEST_NAME_ERROR:
            return {
                "success": False,
                "message": "Warning: Database query text name error",
                "error": "Database query text name error."
            }

        elif feedback.result == feedback.EStartToken.CTI_START_DATABASE_QUERY_TEST_NAME_ERROR:
            return {
                "success": False,
                "message": "Warning: Test name error",
                "error": "Test name error."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_GO_STEP:
            return {
                "success": False,
                "message": "Warning: Step Error",
                "error": "Step Error."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_INVALID_PARALLEL:
            return {
                "success": False,
                "message": "Warning: Parallel error",
                "error": "Parallel error."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_SAFETY:
            return {
                "success": False,
                "message": "Warning: Safety error",
                "error": "Safety error."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_SECHEDULE_NAME_DIFFERENT:
            return {
                "success": False,
                "message": "Warning: Schedule name different error",
                "error": "Schedule name different error."
            }

        elif feedback.result == feedback.EStartToken.CTI_START_BATTERYSIMULATION_NOT_PARALLEL:
            return {
                "success": False,
                "message": "Warning: Battery simulation not parallel error.",
                "error": "Battery simulation not parallel error."
            }

        elif feedback.result == feedback.EStartToken.CTI_START_CSV_WAIT_TIME:
            return {
                "success": False,
                "message": "Warning: Failed to start channels.",
                "error": "Please wait 45s util csv file finished writing."
            }
        elif feedback.result == feedback.EStartToken.CTI_START_CHANNEL_SUSPENT:
            return {
                "success": False,
                "message": "Warning: Channel suspend.",
                "error": "Channel suspend."
            }

        elif feedback.result == feedback.EStartToken.CTI_START_TESTNAME_TOO_LONG:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": "Test name is too long."
            }

        else:
            return {
                "success": False,
                "message": "Failed to start channels.",
                "error": f"Unknown Error occurs, feedback: {feedback.result}"
            }

    except Exception as e:
        return {
            "success": False,
            "message": "Failed to start channels. An unexpected error occurred.",
            "error": str(e)
        }


@router.post("/channels/stop")
async def stop_channel(request: StopChannelRequest):
    try:
        channel_index = request.channel_index
        is_stop_all = request.is_stop_all
        cmd_sent = False
        start_time = time.time()
        while not cmd_sent and (time.time() - start_time) < CMD_TIMEOUT:
            cmd_sent = cti_wrapper.stop_channel(channel_index, is_stop_all)
            if not cmd_sent:
                time.sleep(0.1)
        if not cmd_sent:
            return {
                "success": False,
                "message": "Failed to stop channel.",
                "error": f"Failed to send stop channel command within {CMD_TIMEOUT} seconds."
            }

        feedback_received = False
        start_time = time.time()
        while not feedback_received and (time.time() - start_time) < FEEDBACK_TIMEOUT:
            feedback_received = cti_wrapper.stop_channel_feedback is not None
            if not feedback_received:
                time.sleep(0.1)

        if not feedback_received:
            return {
                "success": False,
                "message": "Failed to stop channel.",
                "error": f"Failed to receive stop channel feedback within {FEEDBACK_TIMEOUT} seconds."
            }

        feedback = cti_wrapper.stop_channel_feedback
        cti_wrapper.stop_channel_feedback = None
        # print("IN my stop channel api, the result received is ", feedback)

        if feedback.result == feedback.EStopToken.SUCCESS:
            return {
                "success": True,
                "message": "Channel stopped successfully.",
                "feedback": feedback
            }
        elif feedback.result == feedback.EStopToken.STOP_INDEX:
            return {
                "success": False,
                "message": "Failed to stop channel,",
                "error": "Failed to stop channel because index error."
            }
        elif feedback.result == feedback.EStopToken.STOP_ERROR:
            return {
                "success": False,
                "message": "Failed to stop channel",
                "error": "Failed to stop channel. Execution error."
            }
        elif feedback.result == feedback.EStopToken.STOP_NOT_RUNNING:
            return {
                "success": False,
                "message": "Failed to stop channel",
                "error": "Failed to stop channel. Channel is not running."
            }
        elif feedback.result == feedback.EStopToken.STOP_CHANNEL_NOT_CONNECT:
            return {
                "success": False,
                "message": "Failed to stop channel",
                "error": "Failed to stop channel. Channel is not connected."
            }

    except Exception as e:
        return {
            "success": False,
            "message": "Failed to stop channels. An unexpected error occurred.",
            "error": str(e)
        }
