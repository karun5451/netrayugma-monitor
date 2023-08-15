import tkinter as tk
import asyncio
from threading import Thread
from communication import WebSocketClient
from plotter import DataPlotter

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('WebSocket Serial Plotter')
        
        self.uri_label = tk.Label(root, text="WebSocket URI:")
        self.uri_label.pack()

        self.uri_entry = tk.Entry(root)
        self.uri_entry.insert(0, "ws://localhost:8765")  # Sample URI
        self.uri_entry.pack()

        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_websocket)
        self.connect_button.pack()

        self.disconnect_button = tk.Button(root, text="Disconnect", command=self.disconnect_from_websocket, state=tk.DISABLED)
        self.disconnect_button.pack()

        self.plotter = DataPlotter()
        self.websocket_client = None

    def connect_to_websocket(self):
        uri = self.uri_entry.get()
        if not uri.startswith("ws://") and not uri.startswith("wss://"):
            self.display_error_message("Invalid WebSocket URI")
            return

        self.websocket_client = WebSocketClient(uri)

        # Start the WebSocket connection in a separate thread
        self.websocket_thread = Thread(target=self.connect_and_plot)
        self.websocket_thread.start()

        self.connect_button.config(state=tk.DISABLED)
        self.disconnect_button.config(state=tk.NORMAL)

    def connect_and_plot(self):
        if self.websocket_client:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.websocket_client.connect(self.update_plot))
            except asyncio.TimeoutError:
                self.display_error_message("Connection timeout: Unable to connect to the WebSocket server")

    def disconnect_from_websocket(self):
        if self.websocket_client:
            self.websocket_client.disconnect()
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)

    def update_plot(self, data):
        try:
            time, horizontal, vertical = map(float, data.split(','))
            self.plotter.update_plot(time, horizontal, vertical)
        except ValueError:
            pass

    def display_error_message(self, message):
        error_label = tk.Label(self.root, text=message, fg="red")
        error_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
