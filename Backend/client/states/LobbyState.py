from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from client.Client import Client

from client.states.AbstractState import AbstractState

class LobbyState(AbstractState):
    pass

class HostingLobbyState(LobbyState):

    @classmethod
    async def enter_state(cls, client: Client):
        await super().enter_state(client)
        await client.send({
                "action": "lobby_created",
                "code": client.current_game.code
            })

class GuestLobbyState(LobbyState):

    @classmethod
    async def enter_state(cls, client: Client):
        await super().enter_state(client)
        await client.send({
                "action": "lobby_joined",
                "code": client.current_game.code
            })
