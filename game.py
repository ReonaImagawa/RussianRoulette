# Packages
import socket, threading, os, random, pickle, time

# Variables
localHostname = socket.gethostname()
socket.gethostbyname(localHostname)
itemList = ['Beer', 'Burner Phone', 'Cigarette', 'Medicine', 'Saw', 'Inverter', 'Magnifying Glass']
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
        msg = pickle.loads(connection.recv(2048))
        print(msg if 'requestItemUse' in msg else "")

    connection.close()

def sendMessage(content):
    client.sendall(pickle.dumps(content))

def removePrefixFromMessage(message, header):
    while f'|{header}|' in message:
            message = message[1:]
    message = message.lstrip(f'|{header}|')
    return message

def showItems(items):
    prefix = "Your" if items.startswith(f'{client.getsockname()[0]}:{client.getsockname()[1]}') else "Your Opponent's"
    items = f'{prefix} Items: ' + removePrefixFromMessage(items, 'items')
    print(items)
    print('\n')

def handleInput(message):
    prefix = "your" if message.startswith(f'{client.getsockname()[0]}:{client.getsockname()[1]}') else "your opponent's"
    timeLimit = removePrefixFromMessage(message, 'turn')
    print(f"It is {prefix} turn.")
    if prefix == 'your':
        while True:
            userInput = str.title(input("Type 'shoot' to shoot, or type the name of an item to use it.\n\n"))
            if round(time.time()) > int(timeLimit):
                print("You took too long to choose an option!")
                break
            match userInput:
                case 'Shoot':
                    pass
                case userInput if userInput in itemList:
                    sendMessage(f'server|requestItemUse|{userInput}')
    print('\n')

# Game
def buckshotRoulette(machine=None):
    match mode:
        case 'host':
            # Items

            userItems = []
            for userIndex in range(len(connectedUsers)):
                items = []
                for __ in range(4):
                    item = random.choice(itemList)
                    items.append(item)
                print(items)
                userItems.append(items)
                for user in connectedUsers:
                    user.send(pickle.dumps(f'{connectedAddrs[userIndex]}|items|{', '.join(items)}'))
                    time.sleep(0.5)

            # Game Loop

            recievedInput = True
            while True and recievedInput:
                recievedInput = False
                turn = 0
                for user in connectedUsers:
                    user.send(pickle.dumps(f'{connectedAddrs[turn]}|turn|{round(time.time()) + 30}'))


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
                elif '|turn|' in message:
                    handleInput(message)
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
