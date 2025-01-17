import clr  # type: ignore
import os
from System import Int16  # type: ignore
from System import UInt32  # type: ignore

script_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(script_dir, "ArbinCTI.dll")
if not os.path.exists(dll_path):
    raise FileNotFoundError(f"Could not find DLL at {dll_path}")
clr.AddReference(dll_path)
from typing import Optional
from ArbinCTI.Core import ArbinClient  # type: ignore
from ArbinCTI.Core.Control import ArbinControl  # type: ignore
from ArbinCTI.Core import ArbinCommandGetChannelDataFeed  # type: ignore

from ctitoolbox import LoginFeedback, AssignScheduleFeedback, BrowseDirectoryFeedback, GetChannelDataFeedback, \
    StartChannelFeedback, StopChannelFeedback, CSTypeConverter

from System import Double # type: ignore
from System import Single # type: ignore



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
        if self.client is None or not self.client.IsConnected():
            self.client = ArbinClient()
            self.client.ConnectAsync(ipaddress, int(port), 0, 0)

            self.Start()  # create thread to process the CTI packets
            self.ListenSocketRecv(self.client)

            # login
            self.PostLogicConnect(self.client, True)
        return self.PostUserLogin(self.client, username, password)

    def OnUserLoginFeedBack(self, feedback):
        try:
            # self.login_feedback = int(feedback.Result)
            self.login_feedback = LoginFeedback(feedback)
        except Exception as e:
            print("Error: login error", e)

    def OnLogicConnectFeedBack(self, feedback):
        pass

    def logout(self):
        self.client.ShutDown()
        self.Exit()

    def isConnected(self):
        return self.client.IsConnected()

    # endregion

    # region file operation
    def browse_schedule_file(self):
        return self.PostBrowseDirectory(self.client, r"SCHEDULE")

    def OnBrowseDirectoryBack(self, feedback):
        try:
            self.browse_schedule_file_feedback = BrowseDirectoryFeedback(feedback)
        except Exception as err:
            print("Convert browse directory feedback error: ", err)

    # endregion

    # region test command
    def assign_schedule(self, schedule_name: str,
                        barcode: str, capacity: float,
                        MVUD1: float, MVUD2: float, MVUD3: float, MVUD4: float,
                        all_assign=False, channel_index=-1):
        # return self.PostAssignSchedule(self.client, "test2.sdx", barcode, Single(capacity), Single(MVUD1), Single(MVUD2), Single(MVUD3), Single(MVUD4),
        #                                all_assign,
        #                                channel_index)
        return self.PostAssignSchedule(self.client, schedule_name, barcode, capacity, MVUD1, MVUD2, MVUD3, MVUD4,
                                       all_assign,
                                       channel_index)

    def OnAssignScheduleFeedBack(self, feedback):
        try:
            self.assign_schedule_feedback = AssignScheduleFeedback(feedback)
        except Exception as err:
            print("Convert assign schedule feedback error: ", err)

    # endregion

    # region channel operations

    def get_channel_info(self, data_type: int = 1792, channel_index: int = -1):
        """
        Use default channel type: All channel
        :param data_type:
        :param channel_index:
        :return:
        """
        converted_data_type = CSTypeConverter.to_uint(data_type)

        # return self.PostGetChannelsData(self.client, CSTypeConverter.to_uint(data_type), CSTypeConverter.to_short(-1),
        #                                 ArbinCommandGetChannelDataFeed.GET_CHANNEL_TYPE.ALLCHANNEL)
        return self.PostGetChannelsData(self.client, CSTypeConverter.to_uint(data_type), CSTypeConverter.to_short(-1), GetChannelDataFeedback.EChannelType.ALLCHANNEL.to_cs())

    def OnGetChannelsDataFeedBack(self, feedback):
        try:
            self.get_channel_info_feedback = GetChannelDataFeedback(feedback)
            # print(self.get_channel_info_feedback.channel_data[0].auxs)
            # for item in feedback.m_Channels[0].Auxs:
            #     print("aux", item[GetChannelDataFeedback.ChannelInfo.AuxType.T.value])
            #
            # for item in feedback.m_Channels[0].AuxeDatas:
            #     print("aux data",item[GetChannelDataFeedback.ChannelInfo.AuxType.T])

        except Exception as e:
            print("Convert channel data feedback error: ", e)

    def start_channel(self, test_name: str, channels: list[int]):
        converted_channels = CSTypeConverter.to_list(channels, CSTypeConverter.EDataType.USHORT)
        return self.PostStartChannel(self.client, test_name, converted_channels)

    def OnStartChannelFeedBack(self, feedback):
        try:
            self.start_channel_feedback = StartChannelFeedback(feedback)
        except Exception as e:
            print("Convert start channel feedback error: ", e)

    def stop_channel(self, channel: int, is_stop_all: bool):
        return self.PostStopChannel(self.client, channel, is_stop_all)

    def OnStopChannelFeedBack(self, feedback):
        try:
            self.stop_channel_feedback = StopChannelFeedback(feedback)
        except Exception as e:
            print("Convert stop channel feedback error: ", e)

    # endregion
