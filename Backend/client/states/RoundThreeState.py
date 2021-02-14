from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.Client import Client

from .AbstractState import AbstractState


class RoundThreeState(AbstractState):
    pass


class RoundThreeStateSpectating(RoundThreeState):
    pass


class RoundThreeStateWaiting(RoundThreeState):
    @classmethod
    async def action_notify_ready(cls, _msg, client: Client) -> Optional[AbstractState]:
        client.current_game.round_three_module.ready_clients.add(client)
        if client.current_game.round_three_module.are_all_clients_ready:
            return RoundThreeStateReadyLast()
        return RoundThreeStateReady()


RoundThreeStateWaiting.actions = {
    "notify_ready": RoundThreeStateWaiting.action_notify_ready
}


class RoundThreeStateReady(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, _old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send({"action": "ack_notify"})


class RoundThreeStateReadyLast(RoundThreeStateReady):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await super().enter_state(client, old_state)
        # TODO Transition all ready to answering

class RoundThreeStateAnswering(RoundThreeState):
    pass


class RoundThreeStateAnswered(RoundThreeState):
    pass
