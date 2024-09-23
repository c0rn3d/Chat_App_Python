# Chat Application

This is a simple chat application built using Python's `socket` and `tkinter` libraries. It allows multiple clients to connect to a server and exchange messages in real-time.

## Features

- **Real-time Messaging**: Connect to a server and chat with other users.
- **Multiline Input**: Use the input box for multiline messages.
- **User Commands**: Includes commands for listing users, help, and quitting.

## Usage

### Sending Messages

- **Send Button**: Click the "Send" button to send your message.
- **Shift + Return**: Press `Shift + Return` to send your message.
- **Return**: Press `Return` to add a new line in the input box.

### Commands

- `{help}`: Show available commands.
- `{users}`: List all online users.
- `{clear}`: Clear your chat window.
- `{quit}`: Leave the chat.

## Requirements

- Python 3.x
- Required libraries: `socket`, `tkinter`, `threading`

## How to Run

1. Start the server script to listen for incoming connections.
2. Run the client script to connect to the server.
3. Follow the instructions in the client interface to chat with others.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
