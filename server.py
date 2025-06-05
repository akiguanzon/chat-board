
import socket
import json

connected = True

join_cmd = {"command": "join"}
leave_cmd = {"command": "leave"}
register_cmd = {"command": "register", "handle": "handle"}
message_cmd = {"command": "msg", "handle": "handle", "message": "message"}
all_cmd = {"command": "all", "message": "<message>"}
error_cmd = {"command":"error", "message":"<error_message>"}
emoji_cmd = {"command": "emoji", "emoji": "<emoji>"}
create_channel_cmd = {"command": "create", "name": "<name>"}
join_channel_cmd = {"command": "channel", "name": "<name>"}
message_channel_cmd = {"command": "msg_channel", "name": "<name>", "message": "<message>"}
leave_channel_cmd = {"command": "leave_channel", "name": "<name>"}

users = []
channels = []

class User:
    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    def __repr__(self):
        return self.handle

class Channel:
    def __init__(self, name):
        self.name = name
        self.users = []

    def __repr__(self):
        return self.name

# Set variables for listening address and listening port
listening_address = '127.0.0.1'
listening_port = 12345

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
print("\nStarting up on %s port %d" % (listening_address, listening_port))
sock.bind((listening_address, listening_port))

print('\nWaiting Connection')
while connected:
    # waiting for data to arrive
    data, address = sock.recvfrom(1024)
    data = data.decode("utf-8")
    command = json.loads(data)

    if command['command'] == "join":
        print(f"Connection to the Message Board Server is successful!\n")
        join_command = json.dumps(join_cmd)
        sock.sendto(bytes(join_command, "utf-8"), address)
        connected = True

    elif command['command'] == "register":

        sender = next(
            (obj for obj in users if obj.handle == command['handle']),
            None
        )

        if not sender:
            print(f"{command['handle']} joined the message board!\n")
            newUser = User(command['handle'], address)
            users.append(newUser)
            print(f"Users in Message Board: {users}")
            register_cmd['handle'] = command['handle']
            register_command = json.dumps(register_cmd)
            sock.sendto(bytes(register_command, "utf-8"), address)
            connected = True

        elif sender:
            error_cmd['message'] = 'Error: Registration failed. Handle or alias already exists.'
            errorMsg = json.dumps(error_cmd)
            sock.sendto(bytes(errorMsg, "utf-8"), address)
            connected = True

    elif command['command'] == "leave":

        sender = next(
            (obj for obj in users if obj.address == address),
            None
        )

        if sender:
            for channel in channels:
                if sender in channel.users:
                    print(f"\n{sender.handle} left the '{channel.name}' channel!")
                    channel.users.remove(sender)

                if not channel.users:
                    print(f"\nThe '{channel.name}' channel has been disbanded.")
                    channels.remove(channel)

            print(f"\n{sender.handle} left the message board!")
            users.remove(sender)
            print(f"\nUsers in Message Board: {users}")
            connected = True

        else:
            print("A connection has been disconnected.")

        # server will disconnect if users are empty
        #if users == []:
            #print("Disconnecting Server")
            #connected = False

    elif command['command'] == "msg":

        sender = next(
            (obj for obj in users if obj.address == address),
            None
        )

        receiver = next(
            (obj for obj in users if obj.handle == command['handle']),
            None
        )

        if sender not in users:
            error_cmd['message'] = 'Error: You are not registered.'
            errorMsg = json.dumps(error_cmd)
            sock.sendto(bytes(errorMsg, "utf-8"), address)
            connected = True

        elif receiver not in users:
            error_cmd['message'] = 'Error: Handle or alias not found.'
            errorMsg = json.dumps(error_cmd)
            sock.sendto(bytes(errorMsg, "utf-8"), address)
            connected = True
        elif not command['message']:
            error_cmd['message'] = 'Error: Command parameters do not match or is not allowed.'
            errorMsg = json.dumps(error_cmd)
            sock.sendto(bytes(errorMsg, "utf-8"), address)
            connected = True
        else:
            message_cmd['handle'] = sender.handle
            message_cmd['message'] = command['message']
            message_command = json.dumps(message_cmd)

            sock.sendto(bytes(message_command, "utf-8"), receiver.address)

            message_cmd['handle'] = receiver.handle
            message_cmd['message'] = command['message']
            message_command = json.dumps(message_cmd)

            sock.sendto(bytes(message_command, "utf-8"), sender.address)

            connected = True

    elif command['command'] == "all":

        sender = next(
            (obj for obj in users if obj.address == address),
            None
        )

        if not command['message']:
            error_cmd['message'] = 'Error: Command parameters do not match or is not allowed.'
            errorMsg = json.dumps(error_cmd)
            sock.sendto(bytes(errorMsg, "utf-8"), address)
            connected = True
        else:
            all_cmd['message'] = f"{sender.handle}: {command['message']}"
            all_command = json.dumps(all_cmd)

            for user in users:
                sock.sendto(bytes(all_command, "utf-8"), user.address)

            connected = True

    elif command['command'] == "emoji":
        if command['emoji'] == 'grin':
            emoji_cmd['emoji'] = "\U0001f600"
        elif command['emoji'] == 'star':
            emoji_cmd['emoji'] = "\U0001F929"
        elif command['emoji'] == 'smile':
            emoji_cmd['emoji'] = "\U0000263A"

        emoji_command = json.dumps(emoji_cmd)
        sock.sendto(bytes(emoji_command, "utf-8"), address)

    elif command['command'] == "create":

        sender = next(
            (obj for obj in users if obj.address == address),
            None
        )
        channel = next(
            (obj for obj in channels if obj.name == command['name']),
            None
        )

        if not channel:
            new_channel = Channel(command['name'])
            channels.append(new_channel)
            new_channel.users.append(sender)
            print(f"\nCreated the '{new_channel.name}' channel!")
            print(f"\nUsers in {new_channel.name}: {new_channel.users}")
            create_channel_cmd['name'] = new_channel.name
            create_channel_command = json.dumps(create_channel_cmd)
            sock.sendto(bytes(create_channel_command, "utf-8"), address)
        else:
            error_cmd['message'] = 'Error: That channel already exists.'
            errorMsg = json.dumps(error_cmd)
            sock.sendto(bytes(errorMsg, "utf-8"), address)
            connected = True

    elif command['command'] == 'channel':
        sender = next(
            (obj for obj in users if obj.address == address),
            None
        )
        channel = next(
            (obj for obj in channels if obj.name == command['name']),
            None
        )

        if channel:
            channel.users.append(sender)
            print(f"\n{sender} successfully joined the '{command['name']}' channel!")
            print(f"\nUsers in {new_channel.name}: {new_channel.users}")

            join_channel_cmd['name'] = channel.name
            join_channel_command = json.dumps(join_channel_cmd)
            sock.sendto(bytes(join_channel_command, "utf-8"), address)
            connected = True
        else:
            error_cmd['message'] = 'Error: Channel does not exist.'
            errorMsg = json.dumps(error_cmd)
            sock.sendto(bytes(errorMsg, "utf-8"), address)
            connected = True

    elif command['command'] == 'msg_channel':
        sender = next(
            (obj for obj in users if obj.address == address),
            None
        )
        channel = next(
            (obj for obj in channels if obj.name == command['name']),
            None
        )

        if channel:
            if sender in channel.users:
                message_channel_cmd['name'] = channel.name
                message_channel_cmd['message'] = f"{sender.handle}): {command['message']}"
                message_channel_command = json.dumps(message_channel_cmd)

                for user in channel.users:
                    sock.sendto(bytes(message_channel_command, "utf-8"), user.address)
            else:
                error_cmd['message'] = 'Error: You are not in the channel.'
                errorMsg = json.dumps(error_cmd)
                sock.sendto(bytes(errorMsg, "utf-8"), address)
        else:
            error_cmd['message'] = 'Error: Channel does not exist.'
            errorMsg = json.dumps(error_cmd)
            sock.sendto(bytes(errorMsg, "utf-8"), address)

        connected = True

    elif command['command'] == 'leave_channel':

        sender = next(
            (obj for obj in users if obj.address == address),
            None
        )
        channel = next(
            (obj for obj in channels if obj.name == command['name']),
            None
        )

        if channel:
            if sender in channel.users:
                print(f"\n{sender.handle} left the {channel.name} channel!")
                channel.users.remove(sender)
                print(f"\nUsers in {channel.name}: {channel.users}")

                if not channel.users:
                    print(f"\nThe {channel.name} channel has been disbanded.")
                    channels.remove(channel)

                leave_channel_cmd['name'] = channel.name
                leave_channel_command = json.dumps(leave_channel_cmd)
                sock.sendto(bytes(leave_channel_command, "utf-8"), address)

                connected = True

            else:
                error_cmd['message'] = 'Error: You are not in the Channel.'
                errorMsg = json.dumps(error_cmd)
                sock.sendto(bytes(errorMsg, "utf-8"), address)

    else:
        error_cmd['message'] = 'Error: Command not found.'
        errorMsg = json.dumps(error_cmd)
        sock.sendto(bytes(errorMsg, "utf-8"), address)
        connected = True

print('Server Disconnected')
sock.close()

