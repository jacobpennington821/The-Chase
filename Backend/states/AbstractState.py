import abc
import websockets
import json

import logging

class InvalidMessage(Exception):
    pass

class AbstractState(abc.ABC):

    actions = {}

    def __init__(self, socket: websockets.client):
        self.socket = socket
    
    async def handle_string(self, string: str):
        try:
            data = json.loads(string)
            await self.handle_message(data)
        except ValueError:
            logging.error(f"Non JSON data received: {string}")

    async def handle_message(self, msg):
        try:
            self.validate_message(msg)
            if msg["action"] not in self.actions:
                logging.error(f"Tried to perform non-existent action {msg['action']} in state {self.__class__.__name__}")
            
            logging.info(f"Running action {msg['action']} on state {self.__class__.__name__}")
            self.actions[msg["action"]](self, msg)
        except InvalidMessage:
            logging.error(f"Malformed event: {msg}")

    @staticmethod
    def validate_message(msg):
        if "action" not in msg:
            raise InvalidMessage()
