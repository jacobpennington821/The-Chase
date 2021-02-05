from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from client.Client import Client

from client.states.AbstractState import AbstractState

class RoundOneState(AbstractState):
    pass

class RoundOneStateNotSpotlit(RoundOneState):

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState):
        await super().enter_state(client, old_state)
        await client.send({"action": "game_started_not_spotlit"})
        return None

class RoundOneStateSpotlit(RoundOneState):

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState):
        await super().enter_state(client, old_state)
        await client.send({"action": "game_started_spotlit"})
        return None

    @classmethod
    async def action_notify_ready(cls, msg, client: Client):
        return RoundOneStateAnswering()

RoundOneStateSpotlit.actions = {
    "notify_ready": RoundOneStateSpotlit.action_notify_ready,
}

class RoundOneStateAnswering(RoundOneState):

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState):
        await super().enter_state(client, old_state)
        await client.game_handler.question_handler.get_next_question()

class RoundOneStateAnswered(RoundOneState):
    pass
