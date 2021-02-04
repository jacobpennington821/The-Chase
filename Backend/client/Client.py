from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Union
from client.states.HomeState import HomeState

if TYPE_CHECKING:
    from websockets.server import WebSocketServerProtocol
    from client.states.AbstractState import AbstractState
    from game.GameHandler import GameHandler
    from game.Game import Game
    from game.RoomCodeHandler import RoomCodeHandler


class Client:
    def __init__(
        self,
        socket: WebSocketServerProtocol,
        game_handler: GameHandler,
    ):
        self.socket: WebSocketServerProtocol = socket
        self.state: AbstractState = HomeState()
        self.game_handler: GameHandler = game_handler
        self.current_game: Union[Game, None] = None

    async def handle_string(self, string: str):
        state = await self.state.handle_string(string, self)
        # If there has been a state transition then do it
        if state is not None:
            await self.change_state(state)

    async def change_state(self, state: AbstractState):
        await self.state.exit_state(self)
        self.state = state
        await self.state.enter_state(self)

    async def handle_disconnect(self):
        print("Disconnected " + str(self.socket))
        await self.state.handle_disconnect(self)

    async def send(self, obj):
        try:
            msg = json.dumps(obj)
            await self.socket.send(msg)
        except ValueError as e:
            logging.error("Can't serialise %s" % e)

    @property
    def is_hosting_game(self) -> bool:
        return self.current_game is not None and self.current_game.host is self

    @property
    def is_in_game(self) -> bool:
        return self.current_game is not None
