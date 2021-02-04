from __future__ import annotations
import logging

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from client.Client import Client

from client.states.AbstractState import AbstractState
from client.states.LobbyState import GuestLobbyState, HostingLobbyState
from game.Game import Game


class InvalidLobbyJoinRequest(Exception):
    pass


class HomeState(AbstractState):
    @classmethod
    async def action_create_lobby(cls, msg, client: Client) -> Optional[AbstractState]:
        code = client.game_handler.room_code_handler.create_new_game_code()
        game = Game(code, client)
        logging.info(f"Created new lobby, code: {game.code}")
        client.game_handler.add_game(game)
        client.current_game = game
        return HostingLobbyState()

    @classmethod
    async def action_join_lobby(cls, msg, client: Client) -> Optional[AbstractState]:
        try:
            code: str = cls.extract_received_code(msg)
            if client.is_in_game:
                logging.error(
                    "Client tried to join a game while already in a game. This shouldn't be possible, states are probably messed up."
                )
                return None
            success = await client.game_handler.join_game(client, code)
            if success:
                return GuestLobbyState()
            else:
                await client.send({"status": "failed"})
                return None
        except InvalidLobbyJoinRequest as e:
            logging.error(e)
            return None

    @staticmethod
    def extract_received_code(msg) -> str:
        if "code" not in msg:
            raise InvalidLobbyJoinRequest("Request did not contain a lobby code.")
        if not isinstance(msg["code"], str):
            raise InvalidLobbyJoinRequest("Request's lobby code isn't a string.")
        return msg["code"]


HomeState.actions = {
    "create_lobby": HomeState.action_create_lobby,
    "join_lobby": HomeState.action_join_lobby,
}
