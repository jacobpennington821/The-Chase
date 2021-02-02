from __future__ import annotations

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from game.Client import Client

class Game:

    def __init__(self, code: str, host: Client):
        self.code: str = code
        self.host: Client = host
        self.guests: List[Client] = []
