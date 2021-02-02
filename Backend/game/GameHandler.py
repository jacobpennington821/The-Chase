from __future__ import annotations

from typing import Union, TYPE_CHECKING
if TYPE_CHECKING:
    from game.Game import Game

class GameHandler:

    def __init__(self):
        self.games = {}

    def add_game(self, game: Game):
        self.games[game.code] = game

    def remove_game(self, game: Union[Game, str]):
        if isinstance(game, Game):
            game = game.code
        del self.games[game]

    def get_game_with_code(self, code: str) -> Game:
        return self.games.get(code, None)
