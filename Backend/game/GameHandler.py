from __future__ import annotations

from typing import Union, TYPE_CHECKING
from game.QuestionHandler import QuestionHandler

from game.RoomCodeHandler import RoomCodeHandler

if TYPE_CHECKING:
    from game.Game import Game
    from client.Client import Client


class GameHandler:
    def __init__(self):
        self.games: dict[str, Game] = {}
        self.room_code_handler: RoomCodeHandler = RoomCodeHandler()
        self.question_handler: QuestionHandler = QuestionHandler()

    def add_game(self, game: Game):
        self.games[game.code] = game

    def remove_game(self, game: Union[Game, str]):
        if isinstance(game, Game):
            game = game.code
        del self.games[game]

    def get_game_with_code(self, code: str) -> Union[Game, None]:
        return self.games.get(code, None)

    async def join_game(self, client: Client, game: Union[Game, str]) -> bool:
        if isinstance(game, str):
            game = self.get_game_with_code(game)
            if game is None:
                return False
        return game.join(client)

    async def host_disconnect(self, client: Client):
        game = client.current_game
        await game.host_disconnect()
        if game.num_clients == 0:
            self.tear_down_game(game)

    async def guest_disconnect(self, client: Client):
        await client.current_game.guest_disconnect(client)

    def tear_down_game(self, game: Game):
        del self.games[game.code]
        self.room_code_handler.free_room_code(game.code)
