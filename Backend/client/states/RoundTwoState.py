from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from client.Client import Client

from client.states.AbstractState import AbstractState

class RoundTwoState(AbstractState):
    pass

class RoundTwoStateSelectingOffer(RoundTwoState):

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState) -> Optional[AbstractState]:
        await super().enter_state(client, old_state)

class RoundTwoStateOfferSelected(RoundTwoState):
    pass
