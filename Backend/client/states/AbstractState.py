from __future__ import annotations
import abc
import json
import logging
from typing import Any, Awaitable, Callable, Dict, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from client.Client import Client


class InvalidMessage(Exception):
    pass


class AbstractState(abc.ABC):

    actions: Dict[str, Callable[[Any, Client], Awaitable[Optional[AbstractState]]]] = {}

    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        pass

    @classmethod
    async def exit_state(cls, client: Client):
        pass

    @classmethod
    async def handle_string(
        cls, string: str, client: Client
    ) -> Optional[AbstractState]:
        try:
            data = json.loads(string)
            return await cls.handle_message(data, client)
        except ValueError:
            logging.error(f"Non JSON data received: {string}")

    @classmethod
    async def handle_message(cls, msg, client: Client) -> Optional[AbstractState]:
        try:
            cls.validate_message(msg)
            if msg["action"] not in cls.actions:
                logging.error(
                    f"Tried to perform non-existent action {msg['action']} in state {cls.__name__}"
                )
                return None

            logging.info(f"Running action {msg['action']} on state {cls.__name__}")
            return await cls.actions[msg["action"]](msg, client)
        except InvalidMessage:
            logging.error(f"Malformed event: {msg}")

    @classmethod
    async def handle_disconnect(cls, client: Client):
        pass

    @staticmethod
    def validate_message(msg):
        if "action" not in msg:
            raise InvalidMessage()
