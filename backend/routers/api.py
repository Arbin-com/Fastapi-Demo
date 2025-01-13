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
                "data": {"feedback": feedback.result}
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/logout")
async def logout():
    try:
        cti_wrapper.logout()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
            raise HTTPException(status_code=500,
                                detail=f"Failed to get channel info feedback within {FEEDBACK_TIMEOUT} seconds.")

        feedback = cti_wrapper.get_channel_info_feedback
        message = {}
        for data in feedback.channel_data:
            message[data.channel_index] = data.status

        cti_wrapper.get_channel_info_feedback = None

        return message

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        feedback = cti_wrapper.browse_schedule_file_feedback
        message = {"files": []}
        if feedback.result == feedback.result.CTI_BROWSE_DIRECTORY_FAILED:
            raise HTTPException(status_code=500, detail=f"Failed to get schedule file.")
        else:
            # import json
            # message = json.dumps(feedback.to_dict())
            for info in feedback.dir_file_info:
                message["files"].append(info.parent_dir_path)
        cti_wrapper.browse_schedule_file_feedback = None
        return message

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        if feedback.result == feedback.result.CTI_ASSIGN_SCHEDULE_FAILED:
            raise HTTPException(status_code=500, detail="Failed to assign schedule.")

        # clean
        cti_wrapper.assign_schedule_feedback = None
        return {"message": "Schedule assigned successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        if feedback.result == feedback.result.CTI_START_CHANNEL_FAILED:
            raise HTTPException(status_code=500, detail="Failed to start channel.")

        cti_wrapper.start_channel_feedback = None
        return {"feedback": feedback}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        if feedback.result == feedback.result.CTI_STOP_CHANNEL_FAILED:
            raise HTTPException(status_code=500, detail="Failed to stop channel.")

        cti_wrapper.stop_channel_feedback = None
        return {"feedback": feedback}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
