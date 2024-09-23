from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        # Accept a new client connection
        client, client_address = SERVER.accept()
        print(f"{client_address[0]}:{client_address[1]} has connected.")
        
        # Send a greeting message to the newly connected client
        client.send(bytes("Greetings from the cave! Type your name and press enter!", "utf8"))
        
        # Store the client's address for reference
        addresses[client] = client_address
        
        # Start a new thread to handle this client
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    """Handles a single client connection."""
    
    # Receive the client's chosen name
    name = client.recv(BUFSIZ).decode("utf8")

    # Check for duplicate usernames
    while name in clients.values():
        # If the name is already taken, prompt the client to choose another
        client.send(bytes("Username already taken. Please choose another name:", "utf8"))
        name = client.recv(BUFSIZ).decode("utf8")

    # Welcome the client and notify others
    welcome = f'Welcome {name}! Type {{help}} for more info.'
    client.send(bytes(welcome, "utf8"))
    msg = f"{name} has joined the chat!"
    broadcast(bytes(msg, "utf8"))  # Notify all clients of the new joiner
    
    # Add the new client to the clients dictionary
    clients[client] = name

    while True:
        # Wait for a message from the client
        msg = client.recv(BUFSIZ)
        
        if msg == bytes("{users}", "utf8"):
            # List all online users when requested
            online_users = f"Online users: {', '.join(clients.values())}"
            client.send(bytes(online_users, "utf8"))
        elif msg == bytes("{help}", "utf8"):
            # Send the help message to the client
            help_text = [
                "Available commands:",
                "\n{help} - Show this help message.",
                "\n{users} - List all online users.",
                "\n{clear} - Clear your chat window.",
                "\n{quit} - Leave the chat."
            ]
            for line in help_text:
                client.send(bytes(line, "utf8"))  # Send each line of help text
        elif msg != bytes("{quit}", "utf8"):
            # Broadcast any other messages to all clients
            broadcast(msg, f"{name}: ")
        else:
            # Handle client quitting
            client.send(bytes("{quit}", "utf8"))
            client.close()  # Close the client connection
            del clients[client]  # Remove the client from the dictionary
            broadcast(bytes(f"{name} has left the chat.", "utf8"))  # Notify others
            break  # Exit the loop

def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""
    for sock in clients:
        # Send the message to each connected client
        sock.send(bytes(prefix, "utf8") + msg)

# Initialize dictionaries for connected clients and their addresses
clients = {}
addresses = {}

# Server settings
HOST = '127.0.0.1'  # Localhost
PORT = 6000         # Port number to listen on
BUFSIZ = 1024       # Buffer size for receiving messages
ADDR = (HOST, PORT) # Tuple containing host and port

# Create a TCP/IP socket
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)  # Bind the socket to the address

if __name__ == "__main__":
    # Start listening for incoming connections
    SERVER.listen(5)
    print("Waiting for connection...")
    
    # Start a thread to accept incoming connections
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    
    # Wait for the accept thread to finish
    ACCEPT_THREAD.join()
    
    # Close the server socket when done
    SERVER.close()
