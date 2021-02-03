from __future__ import annotations
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
        room_code_handler: RoomCodeHandler,
        game_handler: GameHandler,
    ):
        self.socket: WebSocketServerProtocol = socket
        self.state: AbstractState = HomeState()
        self.room_code_handler: RoomCodeHandler = room_code_handler
        self.game_handler: GameHandler = game_handler
        self.current_game: Union[Game, None] = None

    async def handle_string(self, string: str):
        self.state = await self.state.handle_string(string, self)

    @property
    def is_hosting_game(self) -> bool:
        return self.current_game is not None and self.current_game.host is self

    @property
    def is_in_game(self) -> bool:
        return self.current_game is not None
