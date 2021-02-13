from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import asyncio
import logging

if TYPE_CHECKING:
    from client.Client import Client
    from game.Question import Question

from client.states.AbstractState import AbstractState


class RoundTwoState(AbstractState):
    pass


class RoundTwoStateSelectingOffer(RoundTwoState):
    @classmethod
    async def enter_state(
        cls, client: Client, _old_state: AbstractState
    ) -> Optional[AbstractState]:
        round_two_module = client.current_game.round_two_module
        await client.send(
            {
                "action": "provide_offers",
                "offers": [*round_two_module.generate_offer(client)],
            }
        )

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
    pass


class RoundTwoStateLastOfferSelected(RoundTwoState):
    @classmethod
    async def enter_state(
        cls, client: Client, _old_state: AbstractState
    ) -> Optional[AbstractState]:
        game = client.current_game
        other_client_state_changes = [
            c.change_state(RoundTwoStateAnswering())
            for c in game.clients
            if c is not client
        ]
        if other_client_state_changes:
            await asyncio.wait(other_client_state_changes)
        return RoundTwoStateAnswering()


class RoundTwoStateAnswering(RoundTwoState):
    @classmethod
    async def get_and_send_question(cls, client: Client):
        question: Question = (
            await client.current_game.round_two_module.get_next_question(client)
        )
        await client.send(
            {
                "action": "round_2_question",
                "question": question.question,
                "answers": question.shuffled_answers,
                "player_position": client.current_game.round_two_module.player_positions[
                    client
                ],
                "chaser_position": client.current_game.round_two_module.chaser_positions[
                    client
                ],
            }
        )

    @classmethod
    async def enter_state(
        cls, client: Client, _old_state: AbstractState
    ) -> Optional[AbstractState]:
        if client.current_game is None:
            logging.error(
                "Tried to enter %s state without being in a game???", cls.__name__
            )
            return
        await cls.get_and_send_question(client)

    @classmethod
    async def action_answer_question(
        cls, msg, client: Client
    ) -> Optional[AbstractState]:
        if "answer_index" not in msg:
            return None
        if client.current_game is None:
            logging.error(
                "Tried to enter %s state without being in a game???", cls.__name__
            )
            return
        current_question = client.current_game.round_two_module.client_question[client]
        if msg["answer_index"] == current_question.correct_index:
            client.current_game.round_two_module.add_correct_answer(client)
        else:
            client.current_game.round_two_module.add_incorrect_answer(client)
        client.current_answer_index = msg["answer_index"]
        return RoundTwoStateAnswered()


RoundTwoStateAnswering.actions = {
    "answer_question": RoundTwoStateAnswering.action_answer_question
}


class RoundTwoStateAnswered(RoundTwoState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        current_game = client.current_game
        current_question = current_game.round_two_module.client_question[client]
        await client.send(
            {
                "action": "question_answered",
                "correct_answer": current_question.correct_index,
                "given_answer": client.current_answer_index,
                "chaser_answer": current_game.round_two_module.current_chaser_answer_index[
                    client
                ],
                "player_position": client.current_game.round_two_module.player_positions[
                    client
                ],
                "chaser_position": client.current_game.round_two_module.chaser_positions[
                    client
                ],
            }
        )
        return RoundTwoStateAnswering()


class RoundTwoStateWon(RoundTwoState):
    @classmethod
    async def enter_state(
        cls, client: Client, _old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send({"action": "chase_won"})


class RoundTwoStateCaught(RoundTwoState):
    @classmethod
    async def enter_state(
        cls, client: Client, _old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send({"action": "chase_lost"})
