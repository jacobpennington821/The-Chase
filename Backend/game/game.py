from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from client.states.LobbyState import HostingLobbyState

if TYPE_CHECKING:
    from client.Client import Client


class Game:
    def __init__(self, code: str, host: Client):
        self.code: str = code
        self.host: Optional[Client] = host
        self.guests: list[Client] = []
        self.in_lobby: bool = True

    def join(self, client: Client) -> bool:
        if not self.in_lobby:
            return False

        self.guests.append(client)
        client.current_game = self
        return True

    async def host_disconnect(self):
        if len(self.guests) > 0:
            self.host = self.guests[0]
            self.guests = self.guests[1:]
            await self.host.change_state(HostingLobbyState())
        else:
            self.host = None

    async def guest_disconnect(self, client: Client):
        self.guests.remove(client)

    @property
    def num_clients(self) -> int:
        if self.host is not None:
            return len(self.guests) + 1
        return len(self.guests)

    async def start(self) -> bool:
        # Does game need to be a state machine as well? Probably. Is it worth it? Maybe
        self.in_lobby = False
        return True
