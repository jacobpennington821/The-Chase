from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.RoundOneModule import RoundOneModule
    from game.Game import Game

class RoundTwoModule:

    def __init__(self, game: Game):
        self._game = game
        self._round_one_module: RoundOneModule = game.round_one_module
