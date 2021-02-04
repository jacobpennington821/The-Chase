from __future__ import annotations

from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from game.Game import Game
    from client.Client import Client


class GameHandler:
    def __init__(self):
        self.games: dict[str, Game] = {}

    def add_game(self, game: Game):
        self.games[game.code] = game

    def remove_game(self, game: Union[Game, str]):
        if isinstance(game, Game):
            game = game.code
        del self.games[game]

    def get_game_with_code(self, code: str) -> Union[Game, None]:
        return self.games.get(code, None)

    def join_game(self, client: Client, game: Union[Game, str]):
        if isinstance(game, str):
            game_to_join = self.get_game_with_code(game)
            if game_to_join is None:
                return
        game.join(client)
