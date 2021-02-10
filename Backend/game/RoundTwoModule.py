from __future__ import annotations

import random

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from game.RoundOneModule import RoundOneModule
    from game.Game import Game
    from client.Client import Client

class RoundTwoModule:

    def __init__(self, game: Game):
        self._game = game
        self._round_one_module: RoundOneModule = game.round_one_module

    def generate_offer(self, client: Client) -> Tuple[int, int, int]:
        # Low offer has to be < half
        score = self._round_one_module.get_client_score(client)

        low_offer = int(random.randrange(score // 4, score // 2) - (random.randrange(score // 2) * 0.75))
        high_offer = random.randrange(int((score * 1.5)), int(score * 2.5))
        return low_offer, score, high_offer
