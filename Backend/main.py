import asyncio
import logging
import websockets

from client.Client import Client
from game.GameHandler import GameHandler
from game.RoomCodeHandler import RoomCodeHandler


logging.basicConfig(level=logging.INFO)


class ChaseServer:
    def __init__(self):
        self.game_handler = GameHandler()
        self.games = {}
        self.sockets_to_clients = {}

    def register_new_socket(self, socket):
        self.sockets_to_clients[socket] = Client(
            socket, self.game_handler
        )

    async def serve(self, socket, _path):
        self.register_new_socket(socket)
        try:
            async for message in socket:
                await self.sockets_to_clients[socket].handle_string(message)
        finally:
            await self.sockets_to_clients[socket].handle_disconnect()
            del self.sockets_to_clients[socket]

    def start_server(self):
        start_server = websockets.serve(self.serve, "0.0.0.0", 8484)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    server = ChaseServer()
    server.start_server()
