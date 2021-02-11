from __future__ import annotations

import logging
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
        self.selected_offers: dict[Client, int] = {}
        self._generated_offers: dict[Client, Tuple[int, int, int]] = {}

    def generate_offer(self, client: Client) -> Tuple[int, int, int]:
        if client in self._generated_offers:
            return self._generated_offers[client]
        # Low offer has to be < half
        score = self._round_one_module.get_client_score(client)
        if score == 0:
            score = 100
        low_offer = int(random.randrange(score // 4, score // 2) - random.randrange(score // 2))
        high_offer = random.randrange(int((score * 1.5)), int(score * 2.5))
        self._generated_offers[client] = low_offer, score, high_offer
        return low_offer, score, high_offer

    def pick_offer(self, client: Client, offer: int) -> bool:
        if offer not in self._generated_offers[client]:
            return False
        self.selected_offers[client] = offer
        return True

    @property
    def all_clients_submitted(self) -> bool:
        logging.info(str(set(self._game.clients)))
        logging.info(str(set(self.selected_offers.keys())))
        return set(self._game.clients) == set(self.selected_offers.keys())
