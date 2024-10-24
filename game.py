# Packages
import socket, threading, os, random, pickle

# Variables
localHostname = socket.gethostname()
socket.gethostbyname(localHostname)
itemList = ['beer', 'burner phone', 'cigaratte', 'medicine', 'saw', 'inverter', 'magnifying glass']
connectedUsers = []

# Functions
def getIPAddress():
    temporarySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temporarySocket.connect(('8.8.8.8', 80))
    ipAddress = temporarySocket.getsockname()[0]
    temporarySocket.close()
    return ipAddress

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def startHosting(server):
    server.listen()
    print(f"Server hosted on [{getIPAddress()}].\nYou will need to open another terminal instance to join this server.")
    while True:
        con, addr = server.accept()
        if (threading.active_count() - 1) >= 2:
            disconnectThread = threading.Thread(target=disconnectClient, args=(con, addr))
            disconnectThread.start()
        else:
            thread = threading.Thread(target=handleClient, args=(con, addr))
            thread.start()
            print(f"{threading.active_count() - 1} active connection(s).")
        if (threading.active_count() - 1) == 2: buckshotRoulette()

def disconnectClient(connection, addr):
    connection.send("/DISCONNECT".encode('utf-8'))
    connection.close()

def handleClient(connection, addr):
    connectedUsers.append(connection)
    print(f"[{addr[0]}] has joined the server.")

    connected = True

    while connected:
        msg_length = connection.recv(2048).decode('utf-8')
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode('utf-8')
            print(f"[{addr[0]}:{addr[1]}]: {msg}")

    connection.close()

def sendMessage(computer, content):
    message = content.encode('utf-8')
    msg_length = len(message)
    send_length = str(msg_length).encode('utf-8')
    send_length += b' ' * (2048 - len(send_length))
    client.send(send_length)
    client.send(message)

# Game
def buckshotRoulette(client=None):
    match mode:
        case 'host':
            for user in connectedUsers:
                items = []
                for __ in range(4):
                    item = random.choice(itemList)
                    items.append(item)
                print(items)
                user.send(pickle.dumps(items))
        case 'join':
            while True:
                message = client.recv(2048)
                if message == b'': pass
                print(pickle.loads(message))


# Main Menu
while True:
    clearScreen()
    mode = str.lower(input("Would you like to join or host a game? "))
    if mode in ['join', 'host']:
        break

match mode:
    case 'join':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((input("Enter the IP address of the server: "), 5050))
        sendMessage(client, "Hello")
        buckshotRoulette(client)
        while True:
            message = client.recv(2048)
            if message == b'/DISCONNECT':
                break
        print("The requested server is full.")
    case 'host':
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((getIPAddress(), 5050))
        startHosting(server)
        buckshotRoulette()
