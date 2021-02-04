from __future__ import annotations

from client.states.AbstractState import AbstractState

class RoundOneState(AbstractState):
    pass

class RoundOneStateNotSpotlit(RoundOneState):
    pass

class RoundOneStateSpotlit(RoundOneState):
    pass

class RoundOneStateGettingReady(RoundOneStateSpotlit):
    pass

class RoundOneStateAnswering(RoundOneStateSpotlit):
    pass

class RoundOneStateAnswered(RoundOneStateSpotlit):
    pass
