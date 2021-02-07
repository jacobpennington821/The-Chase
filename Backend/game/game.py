from __future__ import annotations
import asyncio
from asyncio.events import TimerHandle

from typing import Optional, TYPE_CHECKING
from game.QuestionHandler import QuestionHandler
from client.states.LobbyState import HostingLobbyState

if TYPE_CHECKING:
    from client.Client import Client

# TODO Add usernames
class Game:

    ROUND_ONE_TIMER_LENGTH = 60

    def __init__(self, code: str, host: Client):
        self.code: str = code
        self.host: Optional[Client] = host
        self.guests: list[Client] = []
        self.in_lobby: bool = True
        self.round_1_timer: Optional[TimerHandle] = None
        self.question_handler: QuestionHandler = QuestionHandler()

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
        return True

    def reset_round_1_timer(self, callback, *args):
        if self.round_1_timer is not None:
            self.round_1_timer.cancel()
        self.round_1_timer = asyncio.get_event_loop().call_later(self.ROUND_ONE_TIMER_LENGTH, asyncio.create_task, callback(self, *args))
