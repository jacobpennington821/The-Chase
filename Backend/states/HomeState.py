from states.AbstractState import AbstractState
from game.RoomCodeHandler import RoomCodeHandler
from game.Game import Game

import websockets
import logging

class HomeState(AbstractState):

    def __init__(self, socket: websockets.client, room_code_handler: RoomCodeHandler):
        super().__init__(socket)
        self.room_code_handler = room_code_handler

    def action_create_lobby(self, msg):
        code = self.room_code_handler.create_new_game_code()
        game = Game(code, self.socket)
        logging.info(f"Created new lobby, code: {game.code}")

    def action_join_lobby(self, msg):
        pass

    actions = {
        "create_lobby": action_create_lobby,
        "join_lobby": action_join_lobby,
    }
