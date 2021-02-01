from game.GameHandler import GameHandler
from game.RoomCodeHandler import RoomCodeHandler
import asyncio
import logging
import json
import random
import string
import websockets

from game.Game import Game
from states.HomeState import HomeState

logging.basicConfig(level=logging.DEBUG)

class ChaseServer:

    LOBBY_CODE_LENGTH = 6

    def __init__(self):
        self.room_code_handler = RoomCodeHandler()
        self.game_handler = GameHandler()
        self.games = {}
        self.sockets_to_games = {}
        self.sockets_to_state = {}


    def register_new_socket(self, socket):
        self.sockets_to_games[socket] = None
        self.sockets_to_state[socket] = HomeState(socket, self.room_code_handler)

    async def serve(self, socket, path):
        self.register_new_socket(socket)
        try:
            async for message in socket:
                await self.sockets_to_state[socket].handle_string(message)
        finally:
            del self.sockets_to_games[socket]

    def start_server(self):
        start_server = websockets.serve(self.serve, "0.0.0.0", 8484)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    server = ChaseServer()
    server.start_server()
