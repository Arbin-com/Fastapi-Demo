import clr  # type: ignore
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(script_dir, "ArbinCTI.dll")
if not os.path.exists(dll_path):
    raise FileNotFoundError(f"Could not find DLL at {dll_path}")
clr.AddReference(dll_path)
from typing import Optional
from ArbinCTI.Core import ArbinClient  # type: ignore
from ArbinCTI.Core.Control import ArbinControl  # type: ignore
from ctitoolbox import LoginFeedback, AssignScheduleFeedback, BrowseDirectoryFeedback, GetChannelDataFeedback, \
    StartChannelFeedback, StopChannelFeedback


class CTIWrapper(ArbinControl):
    __namespace__ = "MyArbinControl"

    def __init__(self):
        super().__init__()
        self.client = None

        # for cmd feedback
        self.login_feedback: Optional[LoginFeedback] = None
        self.assign_schedule_feedback: Optional[AssignScheduleFeedback] = None
        self.browse_schedule_file_feedback: Optional[BrowseDirectoryFeedback] = None
        self.get_channel_info_feedback: Optional[GetChannelDataFeedback] = None
        self.start_channel_feedback: Optional[StartChannelFeedback] = None
        self.stop_channel_feedback: Optional[StopChannelFeedback] = None

    # region authentication

    def login(self, username, password, ipaddress, port):
        self.client = ArbinClient()
        self.client.ConnectAsync(ipaddress, int(port), 0, 0)

        self.Start()  # create thread to process the CTI packets
        self.ListenSocketRecv(self.client)

        # login
        self.PostLogicConnect(self.client, True)
        return self.PostUserLogin(self.client, username, password)

    def OnUserLoginFeedBack(self, feedback):
        self.login_feedback = LoginFeedback(feedback)

    def OnLogicConnectFeedBack(self, feedback):
        pass

    def logout(self):
        self.client.ShutDown()
        self.Exit()

    def isConnected(self):
        return self.client.Connected

    # endregion

    # region file operation
    def browse_schedule_file(self):
        return self.PostBrowseDirectory(self.client, r"SCHEDULE")

    def OnBrowseDirectoryBack(self, feedback):
        self.browse_schedule_file_feedback = BrowseDirectoryFeedback(feedback)

    # endregion

    # region test command
    def assign_schedule(self, schedule_name: str,
                        barcode: str, capacity: float,
                        MVUD1: float, MVUD2: float, MVUD3: float, MVUD4: float,
                        all_assign=True, channel_index=-1):
        return self.PostAssignSchedule(self.client, schedule_name, barcode, capacity, MVUD1, MVUD2, MVUD3, MVUD4,
                                       all_assign,
                                       channel_index)

    def OnAssignScheduleFeedBack(self, feedback):
        self.assign_schedule_feedback = AssignScheduleFeedback(feedback)

    # endregion

    # region channel operations
    def get_channel_info(self, channel_index: int = -1, data_type: int = 1792):
        """
        Use default channel type: All channel
        :param data_type:
        :param channel_index:
        :return:
        """
        return self.PostGetChannelsData(self.client, data_type, channel_index)

    def OnGetChannelsDataFeedBack(self, feedback):
        if feedback is None:
            self.get_channel_info_feedback = None
        self.get_channel_info_feedback = GetChannelDataFeedback(feedback)

    def start_channel(self, test_name: str, channels: list[int]):
        return self.PostStartChannel(self.client, test_name, channels)

    def OnStartChannelFeedBack(self, feedback):
        self.start_channel_feedback = StartChannelFeedback(feedback)

    def stop_channel(self, channel: int, is_stop_all: bool):
        return self.PostStopChannel(self.client, channel, is_stop_all)

    def OnStopChannelFeedBack(self, feedback):
        self.stop_channel_feedback = StopChannelFeedback(feedback)

    # endregion
