import unittest
import os
import sys
from unittest.mock import MagicMock, patch
from services.cti_service import CTIWrapper, LoginFeedback, AssignScheduleFeedback, BrowseDirectoryFeedback, \
    GetChannelDataFeedback, StartChannelFeedback, StopChannelFeedback

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
os.chdir(project_root)

sys.path.insert(0, project_root)


class TestCTIWrapper(unittest.TestCase):

    def setUp(self):
        """
        Set up the CTIWrapper instance and mock necessary methods.
        """
        self.cti_wrapper = CTIWrapper()

        # Mock the underlying ArbinClient and ArbinControl methods
        self.cti_wrapper.client = MagicMock()
        self.cti_wrapper.ConnectAsync = MagicMock()
        self.cti_wrapper.Start = MagicMock()
        self.cti_wrapper.ListenSocketRecv = MagicMock()
        self.cti_wrapper.PostUserLogin = MagicMock(return_value=True)
        self.cti_wrapper.PostLogicConnect = MagicMock()
        self.cti_wrapper.PostBrowseDirectory = MagicMock()
        self.cti_wrapper.PostAssignSchedule = MagicMock()
        self.cti_wrapper.PostGetChannelsData = MagicMock()
        self.cti_wrapper.PostStartChannel = MagicMock()
        self.cti_wrapper.PostStopChannel = MagicMock()

    # Test login functionality
    def test_login(self):
        result = self.cti_wrapper.login("admin", "000000", "127.0.0.1", 9031)

        # Verify that the necessary methods are called
        self.cti_wrapper.ConnectAsync.assert_called_with("127.0.0.1", 9031, 0, 0)
        self.cti_wrapper.Start.assert_called_once()
        self.cti_wrapper.ListenSocketRecv.assert_called_once()
        self.cti_wrapper.PostLogicConnect.assert_called_once_with(self.cti_wrapper.client, True)
        self.cti_wrapper.PostUserLogin.assert_called_once_with(self.cti_wrapper.client, "admin", "000000")

        # Verify the login result
        self.assertTrue(result)

    # Test browse_schedule_file
    def test_browse_schedule_file(self):
        self.cti_wrapper.PostBrowseDirectory.return_value = "test_directory"

        result = self.cti_wrapper.browse_schedule_file()

        # Verify that PostBrowseDirectory is called
        self.cti_wrapper.PostBrowseDirectory.assert_called_with(self.cti_wrapper.client, "SCHEDULE")
        self.assertEqual(result, "test_directory")

    # Test assign_schedule
    def test_assign_schedule(self):
        self.cti_wrapper.PostAssignSchedule.return_value = True

        result = self.cti_wrapper.assign_schedule(
            "test_schedule", "barcode123", 100.0, 1.0, 2.0, 3.0, 4.0, all_assign=True, channel_index=-1
        )

        # Verify that PostAssignSchedule is called
        self.cti_wrapper.PostAssignSchedule.assert_called_with(
            self.cti_wrapper.client,
            "test_schedule",
            "barcode123",
            100.0,
            1.0,
            2.0,
            3.0,
            4.0,
            True,
            -1,
        )
        self.assertTrue(result)

    # Test start_channel
    def test_start_channel(self):
        self.cti_wrapper.PostStartChannel.return_value = True

        result = self.cti_wrapper.start_channel("test_name", [1, 2, 3])

        # Verify that PostStartChannel is called
        self.cti_wrapper.PostStartChannel.assert_called_with(self.cti_wrapper.client, "test_name", [1, 2, 3])
        self.assertTrue(result)

    # Test stop_channel
    def test_stop_channel(self):
        self.cti_wrapper.PostStopChannel.return_value = True

        result = self.cti_wrapper.stop_channel(1, True)

        # Verify that PostStopChannel is called
        self.cti_wrapper.PostStopChannel.assert_called_with(self.cti_wrapper.client, 1, True)
        self.assertTrue(result)

    # Test feedback handlers
    def test_feedback_handlers(self):
        pass
        # login_feedback = MagicMock()
        # self.cti_wrapper.OnUserLoginFeedBack(login_feedback)
        # self.assertEqual(self.cti_wrapper.login_feedback, LoginFeedback(login_feedback))
        # print("Actual:", self.cti_wrapper.login_feedback)
        # print("Expected:", LoginFeedback(login_feedback))
        #
        # assign_feedback = MagicMock()
        # self.cti_wrapper.OnAssignScheduleFeedBack(assign_feedback)
        # self.assertEqual(self.cti_wrapper.assign_schedule_feedback, AssignScheduleFeedback(assign_feedback))
        #
        # browse_feedback = MagicMock()
        # self.cti_wrapper.OnBrowseDirectoryBack(browse_feedback)
        # self.assertEqual(self.cti_wrapper.browse_file_feedback, BrowseDirectoryFeedback(browse_feedback))
        #
        # channel_feedback = MagicMock()
        # self.cti_wrapper.OnGetChannelsDataFeedBack(channel_feedback)
        # self.assertEqual(self.cti_wrapper.get_channel_info_feedback, GetChannelDataFeedback(channel_feedback))
        #
        # start_feedback = MagicMock()
        # self.cti_wrapper.OnStartChannelFeedBack(start_feedback)
        # self.assertEqual(self.cti_wrapper.start_channel_feedback, StartChannelFeedback(start_feedback))
        #
        # stop_feedback = MagicMock()
        # self.cti_wrapper.OnStopChannelFeedBack(stop_feedback)
        # self.assertEqual(self.cti_wrapper.stop_channel_feedback, StopChannelFeedback(stop_feedback))


if __name__ == "__main__":
    unittest.main()
