from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.Client import Client


class Game:
    def __init__(self, code: str, host: Client):
        self.code: str = code
        self.host: Client = host
        self.guests: list[Client] = []

    def join(self, client: Client) -> bool:
        self.guests.append(client)
        client.current_game = self
        return True

    @property
    def num_clients(self) -> int:
        if self.host is not None:
            return len(self.guests) + 1
        return len(self.guests)
