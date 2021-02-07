from __future__ import annotations
import asyncio
import logging

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from client.Client import Client
    from game.Game import Game
    from game.Question import Question

from client.states.AbstractState import AbstractState

class RoundOneState(AbstractState):
    pass

class RoundOneStateNotSpotlit(RoundOneState):

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState) -> Optional[AbstractState]:
        await super().enter_state(client, old_state)
        await client.send({"action": "game_started_not_spotlit"})

class RoundOneStateSpotlit(RoundOneState):

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState) -> Optional[AbstractState]:
        await super().enter_state(client, old_state)
        await client.send({"action": "game_started_spotlit"})

    @classmethod
    async def action_notify_ready(cls, msg, client: Client):
        return RoundOneStateAnswering()

RoundOneStateSpotlit.actions = {
    "notify_ready": RoundOneStateSpotlit.action_notify_ready,
}

class RoundOneStateAnswering(RoundOneState):

    @classmethod
    async def round_1_timer_expired(cls, game: Game):
        await asyncio.wait([client.send({"action": "timer_expired"}) for client in game.clients])
        # TODO Change participants state to round 1b + send offers

    @classmethod
    async def get_and_send_question(cls, game: Game):
        question: Question = await game.question_handler.get_next_question()
        await game.send_to_all({
            "action": "round_1_question",
            "question": question.question,
            "answers": question.shuffled_answers,
            })

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState) -> Optional[AbstractState]:
        await super().enter_state(client, old_state)
        if client.current_game is None:
            logging.error("Tried to enter %s state without being in a game???", cls.__name__)
            return
        await cls.get_and_send_question(client.current_game)
        if not isinstance(old_state, RoundOneStateAnswered):
            client.current_game.reset_round_1_timer(cls.round_1_timer_expired)

    @classmethod
    async def action_answer_question(cls, msg, client: Client) -> Optional[AbstractState]:
        if "answer_index" not in msg:
            return None
        if client.current_game is None:
            logging.error("Tried to enter %s state without being in a game???", cls.__name__)
            return
        current_question = client.current_game.question_handler.current_question
        if msg["answer_index"] == current_question.correct_index:
            client.current_game.add_correct_round_1_answer(client)
        client.current_answer_index = msg["answer_index"]
        return RoundOneStateAnswered()

RoundOneStateAnswering.actions = {
    "answer_question": RoundOneStateAnswering.action_answer_question
}

class RoundOneStateAnswered(RoundOneState):

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState) -> Optional[AbstractState]:
        await super().enter_state(client, old_state)
        current_game = client.current_game
        await current_game.send_to_all({
                "action": "question_answered",
                "correct_answer": current_game.question_handler.current_question.correct_index,
                "given_answer": client.current_answer_index,
                "round_1_score": current_game.get_client_round_1_score(client)})
        return RoundOneStateAnswering()
