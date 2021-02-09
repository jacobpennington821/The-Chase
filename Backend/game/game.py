from __future__ import annotations
import asyncio
from asyncio.events import TimerHandle

from typing import Optional, TYPE_CHECKING
from game.QuestionHandler import QuestionHandler
from client.states.LobbyState import HostingLobbyState
from game.RoundOneModule import RoundOneModule
from game.RoundTwoModule import RoundTwoModule

if TYPE_CHECKING:
    from client.Client import Client

# TODO Add usernames
class Game:

    def __init__(self, code: str, host: Client):
        self.code: str = code
        self.host: Optional[Client] = host
        self.guests: list[Client] = []
        self.in_lobby: bool = True
        self.question_handler: QuestionHandler = QuestionHandler()
        self.round_one_module: RoundOneModule = RoundOneModule(self)
        self.round_two_module: RoundTwoModule = RoundTwoModule(self)

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
        return len(self.clients)

    @property
    def clients(self) -> list[Client]:
        clients = []
        if self.host is not None:
            clients.append(self.host)
        clients.extend(self.guests)
        return clients

    async def send_to_all(self, msg):
        await asyncio.wait([client.send(msg) for client in self.clients])

    async def start(self) -> bool:
        # Does game need to be a state machine as well? Probably. Is it worth it? Maybe
        self.in_lobby = False
        self.round_one_module.start_round()
        return True
