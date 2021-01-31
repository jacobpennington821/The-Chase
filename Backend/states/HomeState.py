from states.AbstractState import AbstractState

class HomeState(AbstractState):

    def action_create_lobby(self, msg):
        pass

    def action_join_lobby(self, msg):
        pass

    actions = {
        "create_lobby": action_create_lobby,
        "join_lobby": action_join_lobby,
    }
