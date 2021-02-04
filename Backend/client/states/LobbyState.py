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
        await client.send({"action": "lobby_hosted", "code": client.current_game.code})

    @classmethod
    async def action_start_game(cls, msg, client: Client) -> Optional[AbstractState]:
        success = await client.current_game.start()

    @classmethod
    async def handle_disconnect(cls, client: Client):
        await super().handle_disconnect(client)
        await client.game_handler.host_disconnect(client)

HostingLobbyState.actions = {
    "start_game": HostingLobbyState.action_start_game
}

class GuestLobbyState(LobbyState):
    @classmethod
    async def enter_state(cls, client: Client):
        await super().enter_state(client)
        await client.send({"action": "lobby_joined", "code": client.current_game.code})

    @classmethod
    async def handle_disconnect(cls, client: Client):
        await super().handle_disconnect(client)
        await client.game_handler.guest_disconnect(client)
