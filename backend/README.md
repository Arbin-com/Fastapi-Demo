# API Documentation

## Overview

This api provides endpoints for Arbin CTI.

## Endpoints

### :dart: Authentication Endpoints

These endpoints handle user authentication.

- `POST /login` - Login
- `POST /logout` - Logout

### :dart: Channel Management

These endpoints handle channel-related operations.

- `GET /channels/status` - Get Channels Status
- `GET /channels/data/{index}` - Get Specific Channel Data
- `POST /channels/start` - Start Channel
- `POST /channels/stop` - Stop Channel

### :dart: Schedule Management

These endpoints manage schedules.

- `GET /schedules` - Get Schedules
- `POST /schedules/assign` - Assign Schedule

### :dart: Test Object Management

These endpoints manage test objects.

- `GET /test_objects` - Get Test Objects
- `POST /test_objects/assign` - Assign Test Objects
