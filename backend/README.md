# API Documentation

## 1. Overview

This api provides endpoints for Arbin CTI.

## 2. Endpoints

**:dart: Authentication Endpoints**

These endpoints handle user authentication.

- `POST /login` - Login
- `POST /logout` - Logout

**:dart: Channel Management**

These endpoints handle channel-related operations.

- `GET /channels/status` - Get Channels Status
- `GET /channels/data/{index}` - Get Specific Channel Data
- `POST /channels/start` - Start Channel
- `POST /channels/stop` - Stop Channel

**:dart: Schedule Management**

These endpoints manage schedules.

- `GET /schedules` - Get Schedules
- `POST /schedules/assign` - Assign Schedule

**:dart: Test Object Management**

These endpoints manage test objects.

- `GET /test_objects` - Get Test Objects
- `POST /test_objects/assign` - Assign Test Objects

## 3. API Reference

**3.1 Authentication**

- `POST /login` - Login

  Schemas

  | Field       | Type   | Required | Description                                                                                     | Example Value |
  | ----------- | ------ | -------- | ----------------------------------------------------------------------------------------------- | ------------- |
  | `username`  | string | ✅       | username                                                                                        | "admin"       |
  | `password`  | string | ✅       | password                                                                                        | "123456"      |
  | `ipaddress` | string | ✅       | ip address where the CTI service is running                                                     | "127.0.0.1"   |
  | `port`      | int    | ❌       | IP Address used for CTI communication, <br> Do not modify unless you have specific requirements | 9031          |

- `POST /logout` - Logout

<br>
<br>

**3.2 Channel Management**

- `POST /channels/start` - Start Channel

  _This endpoint starts test on one or multiple channels._

  | Field       | Type      | Required | Description                              | Example Value |
  | ----------- | --------- | -------- | ---------------------------------------- | ------------- |
  | `test_name` | string    | ✅       | test name                                | "test demo"   |
  | `channels`  | list[int] | ✅       | channels are zero-indexed (start from 0) | [0, 1]        |

<br>

- `POST /channels/stop` - Stop Channel

  _This endpoint stops a selected channel or all channels._

  | Field       | Type      | Required | Description                              | Example Value |
  | ----------- | --------- | -------- | ---------------------------------------- | ------------- |
  | `test_name` | string    | ✅       | test name                                | "test demo"   |
  | `channels`  | list[int] | ❌       | channels are zero-indexed (start from 0) | [0, 1]        |

<br>
<br>

**3.3 Schedule Management**

- `POST /schedules/assign` - Assign Schedule

  _This endpoint assigns schedule file to one or all channels._

  | Field           | Type    | Required | Description                          | Example Value    |
  | --------------- | ------- | -------- | ------------------------------------ | ---------------- |
  | `schedule_name` | string  | ✅       | schedule file name with suffix       | "schedule_1.sdx" |
  | `barcode`       | string  | ❌       | This paramter is only valid for Pro7 | ""               |
  | `MVUD1`         | float   | ❌       | This paramter is only valid for Pro7 | 0.0              |
  | `MVUD2`         | float   | ❌       | This paramter is only valid for Pro7 | 0.0              |
  | `MVUD3`         | float   | ❌       | This paramter is only valid for Pro7 | 0.0              |
  | `MVUD4`         | float   | ❌       | This paramter is only valid for Pro7 | 0.0              |
  | `all_assign`    | boolean |          |                                      |                  |
  | `channel_index` | int     |          |                                      |                  |

<br>
<br>

**3.4 Test Object Management**

- `POST /test_objects/assign` - Assign Schedule

  _This endpoint assigns schedule file to one or all channels._

  | Field        | Type      | Required | Description                    | Example Value    |
  | ------------ | --------- | -------- | ------------------------------ | ---------------- |
  | `file_name`  | string    | ✅       | schedule file name with suffix | "schedule_1.sdx" |
  | `all_assign` | boolean   | ✅       |                                | False            |
  | `file_type`  | int       | ✅       |                                |                  |
  | `channels`   | list[int] | ✅       |                                |                  |
