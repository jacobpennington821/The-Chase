from __future__ import annotations
import asyncio
import logging

from typing import Optional, TYPE_CHECKING

from client.states.AbstractState import AbstractState
from client.states.RoundTwoState import RoundTwoStateSelectingOffer

if TYPE_CHECKING:
    from client.Client import Client
    from game.Game import Game
    from game.Question import Question


class RoundOneState(AbstractState):
    pass

# CHANGE OF PLAN
# Everyone will receive the same question at the same time, answer will be revealed at the same time
# Same goes for round 2 but each person can pick their own offer


class RoundOneStateAnswering(RoundOneState):

    @classmethod
    async def get_and_send_question(cls, client: Client):
        question: Question = await client.current_game.round_one_module.get_next_question(client)
        await client.send({
            "action": "round_1_question",
            "question": question.question,
            "answers": question.shuffled_answers,
            "time_remaining": client.current_game.round_one_module.time_remaining,
            })

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState) -> Optional[AbstractState]:
        await super().enter_state(client, old_state)
        if client.current_game is None:
            logging.error("Tried to enter %s state without being in a game???", cls.__name__)
            return
        await cls.get_and_send_question(client)

    @classmethod
    async def action_answer_question(cls, msg, client: Client) -> Optional[AbstractState]:
        if "answer_index" not in msg:
            return None
        if client.current_game is None:
            logging.error("Tried to enter %s state without being in a game???", cls.__name__)
            return
        current_question = client.current_game.round_one_module.client_question[client]
        if msg["answer_index"] == current_question.correct_index:
            client.current_game.round_one_module.add_correct_answer(client)
        client.current_answer_index = msg["answer_index"]
        return RoundOneStateAnswered()

RoundOneStateAnswering.actions = {
    "answer_question": RoundOneStateAnswering.action_answer_question
}

class RoundOneStateHostStarting(RoundOneState):

    @classmethod
    async def round_1_timer_expired(cls, game: Game):
        await game.send_to_all({"action": "timer_expired"})
        if game.guests:
            await asyncio.wait([guest.change_state(RoundTwoStateSelectingOffer()) for guest in game.guests])
        await game.host.change_state(RoundTwoStateSelectingOffer())

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState) -> Optional[AbstractState]:
        client.current_game.round_one_module.reset_timer(cls.round_1_timer_expired)
        await asyncio.wait(
            [guest.change_state(RoundOneStateAnswering()) for guest in client.current_game.guests])
        return RoundOneStateAnswering()

class RoundOneStateGuestStarting(RoundOneState):
    pass

class RoundOneStateAnswered(RoundOneState):

    @classmethod
    async def enter_state(cls, client: Client, old_state: AbstractState) -> Optional[AbstractState]:
        await super().enter_state(client, old_state)
        current_game = client.current_game
        await client.send({
                "action": "question_answered",
                "correct_answer": current_game.question_handler.current_question.correct_index,
                "given_answer": client.current_answer_index,
                "round_1_score": current_game.round_one_module.get_client_score(client)})
        return RoundOneStateAnswering()
