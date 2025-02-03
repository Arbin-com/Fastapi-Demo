# API Documentation

<a id="readme-top"></a>

<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#1-overview">Overview</a>
    </li>
    <li>
      <a href="#2-endpoints">Endpoints</a>
    </li>
    <li>
      <a href="#3-api-reference">API Reference</a>
      <ul>
        <li><a href="#31-authentication">Authentication</a></li>
        <li><a href="#32-channel-management">Channel Management</a></li>
        <li><a href="#33-schedule-management">Schedule Management</a></li>
        <li><a href="#34-test-object-management">Test Object Management</a></li>
      </ul>
    </li>
  </ol>
</details>

## 1. Overview

This api provides sample endpoints for Arbin CTI.

## 2. Endpoints

**:dart: Authentication Endpoints**

These endpoints handle user authentication.

- [`POST /login` - Login](#post-login---login)
- [`POST /logout` - Logout](#post-logout---logout)

**:dart: Channel Management**

These endpoints handle channel-related operations.

- [`GET /channels/status` - Get Channels Status](#get-channelsstatus---get-channel-status)
- [`GET /channels/data/{index}` - Get Specific Channel Data](#get-channelsdataindex---get-specific-channel-data)
- [`POST /channels/start` - Start Channel](#post-channelsstart---start-channel)
- [`POST /channels/stop` - Stop Channel](#post-channelsstop---stop-channel)

**:dart: Schedule Management**

These endpoints manage schedules.

- [`GET /schedules` - Get Schedules](#get-schedules---get-schedules)
- [`POST /schedules/assign` - Assign Schedule](#post-schedulesassign---assign-schedule)

**:dart: Test Object Management**

These endpoints manage test objects.

- [`GET /test_objects` - Get Test Objects](#get-test_objects---get-test-objects)
- [`POST /test_objects/assign` - Assign Test Objects](#post-test_objectsassign---assign-test-objects)

## 3. API Reference

### 3.1 Authentication

- #### `POST /login` - Login <span style="float: right;">(<a href="#readme-top">back to top</a>)</span>

  _This endpoint handles user login._

  **Schemas**

  | Field       | Type   | Required | Description                                                                                     | Example Value |
  | ----------- | ------ | -------- | ----------------------------------------------------------------------------------------------- | ------------- |
  | `username`  | string | ✅       | username                                                                                        | "admin"       |
  | `password`  | string | ✅       | password                                                                                        | "123456"      |
  | `ipaddress` | string | ✅       | ip address where the CTI service is running                                                     | "127.0.0.1"   |
  | `port`      | int    | ⭕       | IP Address used for CTI communication, <br> Do not modify unless you have specific requirements | 9031          |

  **Sample Request**

  ```
  POST /login
  Content-Type: application/json

  {
  "username": "admin",
  "password": "000000",
  "ipaddress": "127.0.0.1",
  "port": 9031
  }
  ```

  **Sample Response (successful)**

  ```
  {
    "success": true,
    "message": "CTI_LOGIN_SUCCESS",
    "feedback": {
      "result": 1,
      "user_type": 0,
      "serial_number": "",
      "note": "",
      "nickname": "admin",
      "location": "",
      "emergency_contact": "",
      "other_comments": "",
      "email": "",
      "itac": 0,
      "call": "",
      "is_allow_to_control": 1,
      "channel_count": 8,
      "version": 16777223,
      "server_info": null
    }
  }
  ```

  **Sample Response (error)**

  ```
  {
    "success": false,
    "message": "Login failed.",
    "error": "CTI Login failed."
  }
  ```

<br>

- #### `POST /logout` - Logout <span style="float: right;">(<a href="#readme-top">back to top</a>)</span>

  _This endpoint handles user logout._

  **Schemas**

  | Field | Type | Required | Description                               | Example Value |
  | ----- | ---- | -------- | ----------------------------------------- | ------------- |
  | -     | -    | -        | No input required to execute this command | -             |

  **Sample Request**

  ```
  POST /login
  Content-Type: application/json
  {}
  ```

  **Sample Response(successful)**

  ```
  {
  "success": true,
  "message": "Log out successfully."
  }
  ```

  **Sample Response(error)**

  ```
  {
    "success": False,
    "message": "An unexpected error occurred.",
    "error": "error message"
  }
  ```

<br>
<br>

### 3.2 Channel Management

- #### `GET /channels/status` - Get Channel Status <span style="float: right;">(<a href="#readme-top">back to top</a>)</span>

  _This endpoint returns the status of all channels._

  **Query Paramters**

  | Field | Type | Required | Description                                           | Example Value |
  | ----- | ---- | -------- | ----------------------------------------------------- | ------------- |
  | -     | -    | -        | No query paramter is required to execute this command | -             |

  **Sample Request**

  ```
  GET /channels/status
  ```

  **Sample Response (successful)**

  _Detailed Channel Status Code can be found in `EChannelStatus` Class within [Arbin CTI Toolbox](https://github.com/shoufang-w-arbin/Arbin-Toolbox-Python/blob/main/arbintoolbox/src/arbincti/feedback/request_info.py)_

  ```
  {
    "success": true,
    "message": "Get channel status successfully",
    "feedback": [
      {
        "value": 0,
        "status": 15
      },
      {
        "value": 1,
        "status": 15
      },
      {
        "value": 2,
        "status": 15
      },
      {
        "value": 3,
        "status": 0
      },
      {
        "value": 4,
        "status": 0
      },
      {
        "value": 5,
        "status": 0
      },
      {
        "value": 6,
        "status": 0
      },
      {
        "value": 7,
        "status": 0
      }
    ]
  }
  ```

  **Sample Response (Error)**

  ```
  { "success": False,
    "message": "Failed to get channel status.",
    "error": "Failed to get channel info within 3 seconds"
  }
  ```

  <br>

- #### `GET /channels/data/{index}` - Get Specific Channel Data <span style="float: right;">(<a href="#readme-top">back to top</a>)</span>

  _This endpoint returns the status of a specific channel._

  **Path Paramters**

  | Field | Type | Required | Description                                            | Example Value |
  | ----- | ---- | -------- | ------------------------------------------------------ | ------------- |
  | index | int  | ✅       | The channel index from which to fetch data.(0-indexed) | 0             |

  **Sample Request**

  ```
  GET /channels/data/2
  ```

  **Sample Response(successful)**

  ```
  {
  "success": true,
  "message": "Get channel data successfully.",
  "feedback": [
    {
      "channel_index": 0,
      "test_time": 120.0278,
      "step_time": 60.0032,
      "voltage": 2.651676654815674,
      "current": 0,
      "temp": 22.247360229492188
    }
  ]
  }
  ```

  **Sample Response(Error)**

  ```
  {
    "success": False,
    "message": "Failed to get channel data.",
    "error": f"Failed to load data within 3 seconds."
  }
  ```

<br>

- #### `POST /channels/start` - Start Channel <span style="float: right;">(<a href="#readme-top">back to top</a>)</span>

  _This endpoint starts test on one or multiple channels._

  **Schemas**

  | Field       | Type      | Required | Description                              | Example Value |
  | ----------- | --------- | -------- | ---------------------------------------- | ------------- |
  | `test_name` | string    | ✅       | test name                                | "test demo"   |
  | `channels`  | list[int] | ✅       | channels are zero-indexed (start from 0) | [0, 1]        |

  **Sample Request**

  ```
  POST /login
  Content-Type: application/json

  {
  "test_name": "charge-discharge.sdx",
  "channels": [0]
  }
  ```

  **Sample Response (successful)**

  ```
  {
  "success": true,
  "message": "Channel started successfully.",
  "feedback": {
    "result": "CTI_START_SUCCESS"
  }
  }
  ```

  **Sample Response (error)**

  ```
  {
  "success": false,
  "message": "Failed to start channels. Channel is running.",
  "error": "Channel is running."
  }
  ```

<br>

- #### `POST /channels/stop` - Stop Channel <span style="float: right;">(<a href="#readme-top">back to top</a>)</span>

  _This endpoint stops a selected channel or all channels._

  **Schema**

  | Field           | Type    | Required | Description                                 | Example Value |
  | --------------- | ------- | -------- | ------------------------------------------- | ------------- |
  | `channel_index` | int     | ✅       | List of channel indices to stop (0-indexed) | 0             |
  | `is_stop_all`   | boolean | ✅       | Set to `True` to stop all channels          | False         |

  **Sample Request**

  ```
  POST /channels/stop
  Content-Type: application/json

  {
  "channel_index": 0,
  "is_stop_all": false
  }
  ```

  **Sample Response (successful)**

  ```
  {
  "success": true,
  "message": "Channel stopped successfully.",
  "feedback": {
    "result": "SUCCESS"
  }
  }
  ```

  **Sample Response (error)**

  ```
  {
  "success": false,
  "message": "Failed to stop channel",
  "error": "Failed to stop channel. Channel is not running."
  }
  ```

<br>
<br>

### 3.3 Schedule Management

- #### `GET /schedules` - Get Schedules <span style="float: right;">(<a href="#readme-top">back to top</a>)</span>

  _This endpoint returns the names of all schedule files._

  **Query Paramters**

  | Field | Type | Required | Description                                           | Example Value |
  | ----- | ---- | -------- | ----------------------------------------------------- | ------------- |
  | -     | -    | -        | No query paramter is required to execute this command | -             |

  **Sample Request**

  ```
  GET /schedules
  ```

  **Sample Response (successful)**

  ```
  {
  "success": true,
  "message": "Schedules fetched successfully.",
  "feedback": [
    "Schedule_1.sdx",
    "Schedule_2.sdx",
  ]
  }
  ```

  **Sample Response (error)**

  ```
  {
  "success": false,
  "message": "An unexpected error occurred.",
  "error": "Unexpected error occurred, 500: Failed to send get schedules command within 3 seconds."
  }
  ```

  <br>

- #### `POST /schedules/assign` - Assign Schedule <span style="float: right;">(<a href="#readme-top">back to top</a>)</span>

  _This endpoint assigns schedule file to one or all channels._

  **Schemas**

  | Field           | Type    | Required | Description                           | Example Value    |
  | --------------- | ------- | -------- | ------------------------------------- | ---------------- |
  | `schedule_name` | string  | ✅       | schedule file name with suffix        | "schedule_1.sdx" |
  | `barcode`       | string  | ⭕       | This paramter is only valid for Pro7  | ""               |
  | `MVUD1`         | float   | ⭕       | This paramter is only valid for Pro7  | 0.0              |
  | `MVUD2`         | float   | ⭕       | This paramter is only valid for Pro7  | 0.0              |
  | `MVUD3`         | float   | ⭕       | This paramter is only valid for Pro7  | 0.0              |
  | `MVUD4`         | float   | ⭕       | This paramter is only valid for Pro7  | 0.0              |
  | `all_assign`    | boolean | ✅       | set to True to assign to all channels | False            |
  | `channel_index` | int     | ✅       | Set to -1 to assign to all channels   | 0                |

  **Sample Request**

  ```
  {
    "schedule_name": "schedule_1.sdx",
    "barcode": "",
    "capacity": 0,
    "MVUD1": 0,
    "MVUD2": 0,
    "MVUD3": 0,
    "MVUD4": 0,
    "all_assign": false,
    "channel_index": 1
  }
  ```

  **Sample Response(successful)**

  ```
  {
  "success": true,
  "message": "Assign schedule successfully.",
  "feedback": {
    "result": "CTI_ASSIGN_SUCCESS"
  }
  }
  ```

  **Sample Response(Error)**

  ```
  {
  "success": false,
  "message": "Failed to assign the schedule.",
  "error": {
    "result": "CTI_ASSIGN_ERROR"
  }
  }
  ```

<br>
<br>

### 3.4 Test Object Management

- #### `GET /test_objects` - Get Test Objects <span style="float: right;">(<a href="#readme-top">back to top</a>)</span>

  _This endpoint returns the name of all test objects._

  **Query Paramters**

  | Field | Type | Required | Description                                           | Example Value |
  | ----- | ---- | -------- | ----------------------------------------------------- | ------------- |
  | -     | -    | -        | No query paramter is required to execute this command | -             |

  **Sample Request**

  ```
  GET /test_objects
  ```

  **Sample Response(Successful)**

  ```
  {
    "success": true,
    "message": "Test objects fetched successfully.",
    "feedback": [
      "TestObject.to",
      "TestObject_1.to",
      "TestObject_2.to",
    ]
  }
  ```

  **Sample Response(Error)**

  ```
  {
    "success": false,
    "message": "Failed to get Test Object files.",
    "error": "CTI internal failure."
  }

  ```

  <br>

- #### `POST /test_objects/assign` - Assign Test Objects <span style="float: right;">(<a href="#readme-top">back to top</a>)</span>

  _This endpoint assigns test object file to one or all channels._
  _CTI Bug: The feedback result may indicate success even if the file assignment fails. We will resolve it as soon as possible._

  **Schemas**

  | Field        | Type      | Required | Description                                               | Example Value    |
  | ------------ | --------- | -------- | --------------------------------------------------------- | ---------------- |
  | `file_name`  | string    | ✅       | schedule file name with suffix                            | "schedule_1.sdx" |
  | `all_assign` | boolean   | ✅       | if you want to assgin test objects to all channels        | False            |
  | `file_type`  | int       | ✅       | Set to `5` when assigning test objects                    | 5                |
  | `channels`   | list[int] | ✅       | List of channel indices to assign the file to (0-indexed) | [1, 2]           |

  **Sample Request**

  ```
  {
  "file_name": "TestObject.to",
  "all_assign": false,
  "file_type": 5,
  "channels": [
    0
  ]
  }
  ```

  **Sample Response (Successful)**

  ```
  {
  "success": true,
  "message": "Assign files successfully",
  "feedback": {
    "result": "CTI_ASSIGN_SUCCESS",
    "channel_list_result": {
      ""CTI_ASSIGN_SUCCESS"": [
        0
      ]
    }
  }
  }
  ```

  **Sample Response (Error)**

  ```
  "success": False,
  "message": "Failed to assign files",
  "error": "File not found."
  ```
