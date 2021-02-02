from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.Client import Client

from states.AbstractState import AbstractState
from game.Game import Game

import logging

from states.LobbyState import HostingLobbyState

class HomeState(AbstractState):

    @classmethod
    async def action_create_lobby(cls, msg, client: Client) -> AbstractState:
        code = client.room_code_handler.create_new_game_code()
        game = Game(code, client)
        logging.info(f"Created new lobby, code: {game.code}")
        client.game_handler.add_game(game)
        client.current_game = game
        return HostingLobbyState()

    @classmethod
    async def action_join_lobby(cls, msg, client: Client) -> AbstractState:
        pass

HomeState.actions = {
    "create_lobby": HomeState.action_create_lobby,
    "join_lobby": HomeState.action_join_lobby,
}
