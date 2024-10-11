# Socket Chat App
## Overview
This project is a simple multi-client chat server built using Python's `socket` and `threading` modules. The server allows clients to connect, send messages to each other, view the list of currently connected users, and retrieve chat history. Each client is assigned a unique user ID upon connecting to the server, which is used to identify and route messages to other users. The server also stores chat history between users, which can be accessed by specifying a command.

## Usage
To use the app, you need to first ensure the server is running. You can start the server using the following command:
```bash
python server.py <host> <port>
```
To start a new client, run the command below. Replace the host and port with which the server is running on.
```bash
python client.py <host> <port>
```

## Client Commands
- __Send Message to a Specific__
Syntax: `recipientID:message`
Example: `abc123:Hello!`

- __List Connected Users__
Command: `ls`

- __Retrieve Chat History__
Syntax: `hs:recipientID`
Example: `hs:abc123`

- __Disconnect__
Command: `exit`