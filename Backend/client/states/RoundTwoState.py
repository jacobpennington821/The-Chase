from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import logging

if TYPE_CHECKING:
    from client.Client import Client

from client.states.AbstractState import AbstractState

class RoundTwoState(AbstractState):
    pass

class RoundTwoStateSelectingOffer(RoundTwoState):

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState) -> Optional[AbstractState]:
        await super().enter_state(client, old_state)
        round_two_module = client.current_game.round_two_module
        await client.send(
            {"action": "provide_offers", "offers": [*round_two_module.generate_offer(client)]})

    @classmethod
    async def action_pick_offer(cls, msg, client: Client) -> Optional[AbstractState]:
        if "offer" not in msg or not isinstance(msg["offer"], int):
            logging.error("Cannot pick an offer without an offer.")
            return None
        client.current_game.round_two_module.pick_offer(client, msg["offer"])
        if client.current_game.round_two_module.all_clients_submitted:
            return RoundTwoStateLastOfferSelected()
        return RoundTwoStateOfferSelected()

RoundTwoStateSelectingOffer.actions = {
    "pick_offer": RoundTwoStateSelectingOffer.action_pick_offer
}

class RoundTwoStateOfferSelected(RoundTwoState):

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState) -> Optional[AbstractState]:
        pass

class RoundTwoStateLastOfferSelected(RoundTwoState):

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState) -> Optional[AbstractState]:
        pass
