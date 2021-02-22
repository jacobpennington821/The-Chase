from __future__ import annotations
import logging

from typing import Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from client.Client import Client

from client.states.AbstractState import AbstractState
from client.states.LobbyState import GuestLobbyState, HostingLobbyState
from game.Game import Game


class InvalidLobbyJoinRequest(Exception):
    pass


class UnnamedState(AbstractState):
    @classmethod
    async def action_set_name(cls, msg, client: Client) -> Optional[AbstractState]:
        try:
            name: str = cls.extract_received_name(msg)
            client.display_name = name
            return HomeState()
        except InvalidLobbyJoinRequest as inv_name:
            logging.error(inv_name)
            return None

    @staticmethod
    def extract_received_name(msg) -> str:
        if "name" not in msg:
            raise InvalidLobbyJoinRequest("Request did not contain a name.")
        if not isinstance(msg["name"], str):
            raise InvalidLobbyJoinRequest("Request's name is not a string.")
        return msg["name"]


UnnamedState.actions = {"set_name": UnnamedState.action_set_name}


class HomeState(AbstractState):

    @classmethod
    async def enter_state(cls, client: Client, _old_state: AbstractState) -> Optional[AbstractState]:
        await client.send({"action": "ack_name", "name": client.display_name})

    @classmethod
    async def action_create_lobby(cls, _msg, client: Client) -> Optional[AbstractState]:
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
        except InvalidLobbyJoinRequest as inv_lobby:
            logging.error(inv_lobby)
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
