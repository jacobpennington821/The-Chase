from __future__ import annotations
import asyncio
import logging
from typing import TYPE_CHECKING, Optional

from client.states.RoundOneState import (
    RoundOneStateGuestStarting,
    RoundOneStateHostStarting,
)
from client.states.AbstractState import AbstractState

if TYPE_CHECKING:
    from client.Client import Client


class LobbyState(AbstractState):
    pass


class HostingLobbyState(LobbyState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await super().enter_state(client, old_state)
        await client.send({"action": "lobby_hosted", "code": client.current_game.code})

    @classmethod
    async def action_start_game(cls, _msg, client: Client) -> Optional[AbstractState]:
        success = await client.current_game.start()
        if success:
            # TODO Move this into game to handle all of this at once / prevent races
            if client.current_game.guests:
                await asyncio.wait(
                    [
                        guest.change_state(RoundOneStateGuestStarting())
                        for guest in client.current_game.guests
                    ]
                )
            return RoundOneStateHostStarting()
        else:
            logging.error("Can't start game")
            await client.send({"action": "start_game", "status": "failed"})
            return None

    @classmethod
    async def handle_disconnect(cls, client: Client):
        await super().handle_disconnect(client)
        await client.game_handler.host_disconnect(client)


HostingLobbyState.actions = {"start_game": HostingLobbyState.action_start_game}


class GuestLobbyState(LobbyState):
    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState):
        await super().enter_state(client, old_state)
        await client.send({"action": "lobby_joined", "code": client.current_game.code})

    @classmethod
    async def handle_disconnect(cls, client: Client):
        await super().handle_disconnect(client)
        await client.game_handler.guest_disconnect(client)
