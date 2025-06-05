import socket
import json
import threading as td


# JSON Commands
join_cmd = {"command": "join"}
leave_cmd = {"command": "leave"}
register_cmd = {"command": "register", "handle": "handle"}
deregister_cmd = {"command": "deregister", "handle": "handle"}
message_cmd = {"command": "msg", "handle": "handle", "message": "this is my message"}
all_cmd = {"command": "all", "message": "<message>"}
emoji_cmd = {"command": "emoji", "emoji": "<emoji>"}
create_channel_cmd = {"command": "create", "name": "<name>"}
join_channel_cmd = {"command": "channel", "name": "<name>"}
message_channel_cmd = {"command": "msg_channel", "name": "<name>", "message": "<message>"}
leave_channel_cmd = {"command": "leave_channel", "name": "<name>"}

connected = False
registered = False
messaged = False
dest_port = ''
server_host = ''
commands = ['/join', '/leave', '/register', '/all', '/msg', '/emoji', '/joinC', '/channel', '/create', '/leaveC']


def socketResponse():
    global connected
    global messaged
    global registered
    while True:
        try:
            if connected:
                data, server = sock.recvfrom(1024)
                data = data.decode("utf-8")
                command = json.loads(data)

                if command['command'] == "register":
                    print(f"\nWelcome {command['handle']}!")
                    registered = True
                    connected = True

                elif command['command'] == "msg":
                    if messaged:
                        print(f"\n(To {command['handle']}): {command['message']}")
                        messaged = False
                    else:
                        print(f"\n\n(From {command['handle']}): {command['message']}")
                        print(f"\nInput: ", end='')

                    connected = True

                elif command['command'] == 'all':
                    if messaged:
                        print(f"\n{command['message']}")
                        messaged = False
                    else:
                        print(f"\n\n{command['message']}")
                        print(f"\nInput: ", end='')

                elif command['command'] == 'create':
                    print(f"\nSuccessfully created the '{command['name']}' channel!")

                elif command['command'] == 'channel':
                    print(f"\nSuccessfully joined the '{command['name']}' channel!")

                elif command['command'] == 'msg_channel':
                    if messaged:
                        print(f"\n(|{command['name']}| {command['message']}")
                        messaged = False
                    else:
                        print(f"\n(|{command['name']}| {command['message']}")
                        print(f"\nInput: ", end='')

                elif command['command'] == 'leave_channel':
                    print(f"\nSuccessfully left the '{command['name']}' channel.")

                elif command['command'] == 'emoji':
                    print(f"\n{command['emoji']}")

                elif command['command'] == 'error':
                    print(f"\n{command['message']}")

        except:
            None



def enterInput():
    global inputCommand
    t1.start()
    inputCommand = [str(inputCommand) for inputCommand in input("\nInput: ").split()]
    return inputCommand

def showCommands():
    print("\n/join <server_address> <server_port>: Join a server")
    print("\n/leave: Disconnect from the server")
    print("\n/register <handle>: Register to the server with an alias")
    print("\n/all <message>: Send a message to everyone in the server")
    print("\n/msg <handle> <message>: Send a message to a specific person")
    print("\n/<emojiName>: Select from /grin, /smile, /star, to display an emoji!")
    print("\nEmojis!: You can type ':star', ':smile', or ':grin', into your message to include an emoji in your message!")
    print("\n/create <channel_name>: Create a channel (You are automatically added to the channel)")
    print("\n/joinC <channel_name>: Join a channel")
    print("\n/channel <channel_name> <message>: Send a message to a specific channel")
    print("\n/leaveC <channel_name>: Leave a specific channel\n")

def closeClient():
    global connected
    global sock
    global registered
    connected = False
    registered = False
    print("Connection closed. Thank you!")
    sock.close()
    notConnected()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def notConnected():
    global connected
    global server_host
    global dest_port
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not connected:
        try:
            inputCommand = input("Input: ").split()
            if inputCommand[0] == "/join" and len(inputCommand) == 3:
                dest_port = int(inputCommand[2])
                server_host = inputCommand[1]
                join = json.dumps(join_cmd)

                if server_host == '127.0.0.1':
                    sock.sendto(bytes(join, "utf-8"), (server_host, dest_port))

                    data, server = sock.recvfrom(1024)
                    data = data.decode("utf-8")
                    command = json.loads(data)

                    if command['command'] == "join":
                        print(f"Connection to the Message Board Server is successful!")
                        connected = True
                else:
                    print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                    connected = False
            elif inputCommand[0] == "/leave":
                print("Error: Disconnection failed. Please connect to the server first.")
                connected = False

            elif inputCommand[0] == '/?':
                if len(inputCommand) == 1:
                    showCommands()
                    connected = False
                else:
                    print("Error: Command parameters do not match or is not allowed.")

            elif inputCommand[0] == '/join':
                    print("Error: Command parameters do not match or is not allowed.")

            elif inputCommand[0] in commands:
                if len(inputCommand) != 2 and inputCommand[0] == '/register':
                    print("Error: Command parameters do not match or is not allowed.")
                elif len(inputCommand) < 3 and inputCommand[0] == '/msg':
                    print("Error: Command parameters do not match or is not allowed.")
                elif len(inputCommand) < 2 and inputCommand[0] == '/all':
                    print("Error: Command parameters do not match or is not allowed.")
                else:
                    print("Error: You are not connected to the server.")
                connected = False

            else:
                print("Error: Command not found.")

        except:
            if inputCommand[0] == '/join':
                if len(inputCommand) < 2:
                    print("Error: Command parameters do not match or  is not allowed.")
                else:
                    print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
            else:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

            connected = False


notConnected()

while connected:

    t1 = td.Thread(target=socketResponse)

    try:
        inputCommand = enterInput()
        if not registered:
            if inputCommand[0] == '/register':
                if len(inputCommand) == 2:
                    register_cmd['handle'] = inputCommand[1]
                    register = json.dumps(register_cmd)
                    sock.sendto(bytes(register, "utf-8"), (server_host, dest_port))
                else:
                    print("Error: Command parameters do not match or  is not allowed.")
            elif inputCommand[0] == '/?':
                if len(inputCommand) == 1:
                    showCommands()
                    connected = True
                else:
                    print("Error: Command parameters do not match or  is not allowed.")

            elif inputCommand[0] == '/leave':
                if len(inputCommand) == 1:
                    leave = json.dumps(leave_cmd)
                    sock.sendto(bytes(leave, "utf-8"), (server_host, dest_port))
                    closeClient()
                else:
                    print("Error: Command parameters do not match or  is not allowed.")

            elif inputCommand[0] in commands:
                if len(inputCommand) != 2 and inputCommand[0] == '/register':
                    print("\nError: Command parameters do not match or is not allowed.")
                elif len(inputCommand) < 3 and inputCommand[0] == '/msg':
                    print("\nError: Command parameters do not match or is not allowed.")
                elif len(inputCommand) < 2 and inputCommand[0] == '/all':
                    print("\nError: Command parameters do not match or is not allowed.")
                elif inputCommand[0] == '/join':
                    print("\nError: You are already in a server!")
                else:
                    print("\nError: You are not registered!")
                connected = True
            else:
                print("\nError: Command not found.")

        elif registered:
            if inputCommand[0] == '/msg':
                if len(inputCommand) >= 3:
                    message_cmd['handle'] = inputCommand[1]
                    messageString = inputCommand[2:]
                    messageVar = ''

                    for x in messageString:
                        if x == ':grin':
                            x = "\U0001f600"
                        elif x == ':star':
                            x = "\U0001F929"
                        elif x == ':smile':
                            x = "\U0000263A"

                        messageVar += x + ' '

                    messaged = True
                    message_cmd['message'] = messageVar
                    message = json.dumps(message_cmd)
                    sock.sendto(bytes(message, "utf-8"), (server_host, dest_port))
                else:
                    print("\nError: Command parameters do not match or is not allowed.")

            elif inputCommand[0] == '/all':
                if len(inputCommand) >= 2:
                    messageString = inputCommand[1:]
                    messageVar = ''

                    for x in messageString:
                        messageVar += x + ' '

                    messaged = True
                    all_cmd['message'] = messageVar
                    message = json.dumps(all_cmd)
                    sock.sendto(bytes(message, "utf-8"), (server_host, dest_port))
                else:
                    print("\nError: Command parameters do not match or is not allowed.")

            elif inputCommand[0] == '/leave':
                if len(inputCommand) == 1:
                    leave = json.dumps(leave_cmd)
                    sock.sendto(bytes(leave, "utf-8"), (server_host, dest_port))
                    closeClient()
                else:
                    print("Error: Command parameters do not match or  is not allowed.")

            elif inputCommand[0] == '/?':
                if len(inputCommand) == 1:
                    showCommands()
                    connected = True
                else:
                    print("Error: Command parameters do not match or  is not allowed.")
            elif inputCommand[0] == '/register':
                if len(inputCommand) == 2:
                    print("\nError: You are already registered.")
                else:
                    print("\nError: Command parameters do not match or is not allowed.")

            elif inputCommand[0] == '/create':
                if len(inputCommand) == 2:
                    create_channel_cmd['name'] = inputCommand[1]
                    channel = json.dumps(create_channel_cmd)
                    sock.sendto(bytes(channel, "utf-8"), (server_host, dest_port))
                else:
                    print("\nError: Command parameters do not match or is not allowed.")

            elif inputCommand[0] == '/joinC':
                if len(inputCommand) == 2:
                    join_channel_cmd['name'] = inputCommand[1]
                    channel = json.dumps(join_channel_cmd)
                    sock.sendto(bytes(channel, "utf-8"), (server_host, dest_port))
                else:
                    print("\nError: Command parameters do not match or is not allowed.")

            elif inputCommand[0] == '/channel':
                if len(inputCommand) >= 3:
                    message_channel_cmd['name'] = inputCommand[1]
                    messageString = inputCommand[2:]
                    messageVar = ''

                    for x in messageString:
                        if x == ':grin':
                            x = "\U0001f600"
                        elif x == ':star':
                            x = "\U0001F929"
                        elif x == ':smile':
                            x = "\U0000263A"

                        messageVar += x + ' '

                    messaged = True
                    message_channel_cmd['message'] = messageVar
                    message = json.dumps(message_channel_cmd)
                    sock.sendto(bytes(message, "utf-8"), (server_host, dest_port))
                else:
                    print("\nError: Command parameters do not match or is not allowed.")

            elif inputCommand[0] == '/leaveC':
                if len(inputCommand) == 2:
                    leave_channel_cmd['name'] = inputCommand[1]
                    leave = json.dumps(leave_channel_cmd)
                    sock.sendto(bytes(leave, "utf-8"), (server_host, dest_port))
                else:
                    print("Error: Command parameters do not match or  is not allowed.")

            elif inputCommand[0] == '/grin' or inputCommand[0] == '/star' or inputCommand[0] == 'smile':
                if inputCommand[0] == '/grin':
                    emoji_cmd['emoji'] = 'grin'
                    emoji = json.dumps(emoji_cmd)
                    sock.sendto(bytes(emoji , "utf-8"), (server_host, dest_port))
                elif inputCommand[0] == '/star':
                    emoji_cmd['emoji'] = 'star'
                    emoji = json.dumps(emoji_cmd)
                    sock.sendto(bytes(emoji, "utf-8"), (server_host, dest_port))
                elif inputCommand[0] == '/smile':
                    emoji_cmd['emoji'] = 'smile'
                    emoji = json.dumps(emoji_cmd)
                    sock.sendto(bytes(emoji, "utf-8"), (server_host, dest_port))

            elif inputCommand[0] == '/join':
                print("\nError: You are already in a server!")

            elif inputCommand[0] not in commands:
                print("\nError: Command not found.")


    except:
        inputCommand = input("Input: ")







# close socket
sock.close()
