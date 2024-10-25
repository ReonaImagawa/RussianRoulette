# Packages
import socket, threading, os, random, pickle, time

# Variables
localHostname = socket.gethostname()
socket.gethostbyname(localHostname)
itemList = ['Beer', 'Burner Phone', 'Cigaratte', 'Medicine', 'Saw', 'Inverter', 'Magnifying Glass']
connectedUsers, connectedAddrs = [], []

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
        if (threading.active_count() - 1) == 2: buckshotRoulette(server)

def disconnectClient(connection, addr):
    connection.send(pickle.dumps('/DISCONNECT'))
    connection.close()

def handleClient(connection, addr):
    connectedUsers.append(connection)
    connectedAddrs.append(f'{addr[0]}:{addr[1]}')
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
    client.sendall(pickle.dumps(content))

def showItems(items):
    prefix = "Your" if items.startswith(f'{client.getsockname()[0]}:{client.getsockname()[1]}') else "Your Opponent's"
    while '|items|' in items:
            items = items[1:]
    items = items.lstrip('|items|')
    print(f'{prefix} Items: ')
    for letter in items:
        print(letter, end='', flush=True)
        time.sleep(0.15)
    print('\n\n')

# Game
def buckshotRoulette(machine=None):
    match mode:
        case 'host':
            for userIndex in range(len(connectedUsers)):
                items = []
                for __ in range(4):
                    item = random.choice(itemList)
                    items.append(item)
                print(items)
                for user in connectedUsers:
                    user.send(pickle.dumps(f'{connectedAddrs[userIndex]}|items|{', '.join(items)}'))
                    time.sleep(1)
        case 'join':
            clearScreen()
            while True:
                while True:
                    break
                message = machine.recv(2048)
                if message == b'': pass
                if pickle.loads(message) == '/DISCONNECT':
                    break
                message = pickle.loads(message)
                if '|items|' in message:
                    showItems(message)
            print("The requested server is full.")


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
        buckshotRoulette(client)
    case 'host':
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((getIPAddress(), 5050))
        startHosting(server)
