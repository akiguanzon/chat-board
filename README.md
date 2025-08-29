# chat-board

Simple UDP-based message board (server + CLI client) implemented in Python.

This repository contains a lightweight chat server (`server.py`) and a command-line client (`client.py`) that communicate using JSON messages over UDP. It's intended for local testing and learning about simple network protocols and message routing.

## Files

- `server.py` — UDP server that manages connected users and channels. Listens on `127.0.0.1:12345` by default. Supports register, direct messages, broadcast (all), emoji, channel create/join/leave, and simple error replies.
- `client.py` — CLI client that connects to the server, sends JSON commands, and prints received messages. Uses a simple slash-command interface (e.g. `/join`, `/register`, `/all`, `/msg`, `/create`, `/joinC`, `/channel`, `/leaveC`).

## Requirements

- Python 3 (tested with 3.8+). No external packages required — uses the standard library (`socket`, `json`, `threading`).

## Quick start (local)

Open two terminals.

Terminal 1 — start the server:

```bash
python3 server.py
```

Terminal 2 — start the client:

```bash
python3 client.py
```

Client usage (minimum):

1. Join the server (client only accepts connections to `127.0.0.1` in its current form):

```text
/join 127.0.0.1 12345
```

2. Register an alias:

```text
/register alice
```

3. Send a broadcast to everyone:

```text
/all Hello everyone!
```

4. Send a direct message to another user:

```text
/msg bob Hey Bob, how are you?
```

5. Create and use channels:

```text
/create mychannel
/joinC mychannel
/channel mychannel Hello channel members
/leaveC mychannel
```

6. Emojis

Use `/grin`, `/star`, `/smile` to post an emoji notification. You can also include emoji tokens inside messages using `:grin`, `:star`, `:smile` and the client translates them to unicode when sending.

## Protocol (JSON messages)

JSON commands sent between client and server follow this general shape (examples):

- Join request from client: {"command":"join"}
- Register: {"command":"register", "handle":"alice"}
- Direct message: {"command":"msg", "handle":"bob", "message":"Hi"}
- Broadcast: {"command":"all", "message":"Hello all"}
- Emoji: {"command":"emoji", "emoji":"grin"}
- Create channel: {"command":"create", "name":"channelName"}
- Join channel: {"command":"channel", "name":"channelName"}
- Channel message: {"command":"msg_channel", "name":"channelName", "message":"Hi channel"}
- Leave channel: {"command":"leave_channel", "name":"channelName"}

Server replies use the same `command` keys to indicate events, messages or errors.

## Notes, limitations & assumptions

- Uses UDP, so messages are connectionless and unreliable (packets may be lost or reordered).
- `client.py` currently only accepts a server host of `127.0.0.1` when initiating a `/join` — remote hosts are not supported by the client logic as written.
- No authentication, no persistence. All state (users, channels) is kept in memory on the server.
- Message size is limited by the `recvfrom(1024)` buffers in both client and server.
- Error handling is minimal and implemented via `{"command":"error","message":"..."}` responses.