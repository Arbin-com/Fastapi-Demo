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
  | `ipaddress` | string | ✅       | ip address where the CTI service is running age                                                 | "127.0.0.1"   |
  | `port`      | int    | ❌       | IP Address used for CTI communication, <br> Do not modify unless you have specific requirements | 9031          |

- `POST /logout` - Logout
