from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

class ChatClient:
    def __init__(self, host, port):
        """Initialize the chat client with the server's host and port."""
        self.host = host
        self.port = port
        self.client_socket = socket(AF_INET, SOCK_STREAM)  # Create a socket
        self.client_socket.connect((self.host, self.port))  # Connect to the server
        
        self.bufsiz = 1024  # Buffer size for receiving messages

        # Setup the GUI
        self.setup_gui()
        
        # Start the receive thread
        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()
        
        tkinter.mainloop()  # Start the GUI event loop

    def setup_gui(self):
        """Set up the graphical user interface for the chat client."""
        self.top = tkinter.Tk()
        self.top.title("Chatter")  # Set window title
        self.top.geometry("1200x1000")  # Set window size (width x height)
        self.top.configure(bg="black")  # Set background color
        self.top.resizable(True, True)  # Allow resizing
        
        self.messages_frame = tkinter.Frame(self.top, bg="black")

        # Setup scrollbar for the messages
        self.scrollbar = tkinter.Scrollbar(self.messages_frame, bg="black")

        # Text widget for displaying messages
        self.msg_display = tkinter.Text(
            self.messages_frame,
            height=15,  # Height for visibility
            width=100,   # Width for messages
            bg="black",
            fg="white",
            wrap=tkinter.WORD,  # Wrap text at word boundaries
            font=("Helvetica", 18, "bold")  # Font settings
        )
        self.msg_display.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)  # Text widget expands
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)  # Place scrollbar
        self.scrollbar.config(command=self.msg_display.yview)  # Link scrollbar to text widget
        self.msg_display.config(yscrollcommand=self.scrollbar.set)  # Link text widget to scrollbar
        self.messages_frame.pack(expand=True, fill=tkinter.BOTH)

        # Input field for sending messages (using Text widget for multiline)
        self.entry_field = tkinter.Text(self.top, height=5, bg="white", fg="black", font=("Helvetica", 18))
        self.entry_field.pack(pady=20, padx=20, fill=tkinter.X)

        # Bind Enter key to add a new line, and Shift + Enter to send message
        self.entry_field.bind("<Return>", self.add_newline)
        self.entry_field.bind("<Shift-Return>", self.send)

        # Send button to send messages
        send_button = tkinter.Button(self.top, text="Send", command=self.send, bg="black", fg="white")
        send_button.pack(pady=10)

        # Fullscreen toggle functionality
        self.top.bind("<F11>", self.toggle_fullscreen)  # Bind F11 to toggle fullscreen
        self.top.bind("<Escape>", self.exit_fullscreen)  # Bind Escape to exit fullscreen

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close event

    def receive(self):
        """Handles receiving of messages from the server."""
        while True:
            try:
                msg = self.client_socket.recv(self.bufsiz).decode("utf8")  # Receive message
                if msg:
                    # Insert the received message into the text display
                    self.msg_display.insert(tkinter.END, msg + "\n")  # Add newline for separation
                    self.msg_display.see(tkinter.END)  # Auto-scroll to the bottom
            except OSError:  # If an error occurs (like disconnection)
                break

    def send(self, event=None):
        """Handles sending of messages to the server."""
        msg = self.entry_field.get("1.0", tkinter.END).strip()  # Get all text from the Text widget
        self.entry_field.delete("1.0", tkinter.END)  # Clear the input field

        if msg == "{clear}":
            self.msg_display.delete("1.0", tkinter.END)  # Clear message display locally
        else:
            self.client_socket.send(bytes(msg, "utf8"))  # Send message to server
            if msg == "{quit}":
                self.client_socket.close()  # Close the socket
                self.top.quit()  # Close the GUI

    def add_newline(self, event=None):
        """Adds a newline to the Text widget without sending the message."""
        self.entry_field.insert(tkinter.END, "\n")  # Add newline
        return "break"  # Prevent the default behavior of the Return key

    def on_closing(self, event=None):
        """Called when the window is closed."""
        self.client_socket.send(bytes("{quit}", "utf8"))  # Send the quit message
        self.top.quit()  # Close the GUI

    def toggle_fullscreen(self, event=None):
        """Toggle the application to fullscreen mode."""
        self.top.attributes("-fullscreen", True)

    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode."""
        self.top.attributes("-fullscreen", False)

if __name__ == "__main__":
    # Get server connection details from user
    HOST = input('Enter host: ')
    PORT = input('Enter port (default 6000): ')
    PORT = int(PORT) if PORT else 6000  # Set default port if not provided

    # Create an instance of ChatClient
    chat_client = ChatClient(HOST, PORT)
