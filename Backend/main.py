import asyncio
import logging
import json
import random
import string
import websockets

from game.game import Game
from states.HomeState import HomeState

logging.basicConfig(level=logging.DEBUG)

class ChaseServer:

    LOBBY_CODE_LENGTH = 6

    def __init__(self):
        self.games = {}
        self.used_game_codes = set()
        self.sockets_to_games = {}
        self.sockets_to_state = {}

    def register_new_socket(self, socket):
        self.sockets_to_games[socket] = None
        self.sockets_to_state[socket] = HomeState(socket)

    async def serve(self, socket, path):
        self.register_new_socket(socket)
        try:
            async for message in socket:
                await self.handle_message(socket, message)
        finally:
            del self.sockets_to_games[socket]

    def create_new_game_code(self):
        code_is_unique = False
        while not code_is_unique:
            code = "".join(random.choices(string.ascii_uppercase, k=self.LOBBY_CODE_LENGTH))
            code_is_unique = code not in self.used_game_codes

        return code

    async def handle_message(self, socket, msg):
        try:
            data = json.loads(msg)
            if "action" not in data:
                logging.error(f"Malformed event: {data}")

            if data["action"] == "create_lobby":
                code = self.create_new_game_code()
                self.used_game_codes.add(code)
                game = Game(code, socket)
                logging.info(f"Created new lobby, code: {game.code}")
                self.games[code] = game
            elif data["action"] == "join_lobby":
                pass
            else:
                logging.error(f"Unsupported event: {data}")
        except ValueError:
            logging.error(f"Non JSON data received: {msg}")

    def start_server(self):
        start_server = websockets.serve(self.serve, "0.0.0.0", 8484)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    server = ChaseServer()
    server.start_server()
