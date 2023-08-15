import asyncio
import websockets

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.connected = False

    async def connect(self, callback):
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket
            self.connected = True
            await self._data_stream(callback)

    async def _data_stream(self, callback):
        while self.connected:
            try:
                data = await self.websocket.recv()
                callback(data)
            except websockets.ConnectionClosed:
                self.connected = False
                break

    def disconnect(self):
        self.connected = False
        if self.websocket:
            self.websocket.close()
