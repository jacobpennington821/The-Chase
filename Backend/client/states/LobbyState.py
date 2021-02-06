from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Optional

from client.states.RoundOneState import RoundOneStateNotSpotlit, RoundOneStateSpotlit

if TYPE_CHECKING:
    from client.Client import Client

from client.states.AbstractState import AbstractState


class LobbyState(AbstractState):
    pass


class HostingLobbyState(LobbyState):
    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState):
        await super().enter_state(client, old_state)
        await client.send({"action": "lobby_hosted", "code": client.current_game.code})

    @classmethod
    async def action_start_game(cls, msg, client: Client) -> Optional[AbstractState]:
        success = await client.current_game.start()
        if success:
            for guest in client.current_game.guests:
                await guest.change_state(RoundOneStateNotSpotlit())
            return RoundOneStateSpotlit()
        else:
            logging.error("Can't start game")
            return None

    @classmethod
    async def handle_disconnect(cls, client: Client):
        await super().handle_disconnect(client)
        await client.game_handler.host_disconnect(client)

HostingLobbyState.actions = {
    "start_game": HostingLobbyState.action_start_game
}

class GuestLobbyState(LobbyState):
    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState):
        await super().enter_state(client, old_state)
        await client.send({"action": "lobby_joined", "code": client.current_game.code})

    @classmethod
    async def handle_disconnect(cls, client: Client):
        await super().handle_disconnect(client)
        await client.game_handler.guest_disconnect(client)
