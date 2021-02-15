from __future__ import annotations

import asyncio
import logging

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from client.Client import Client
    from game.Question import Question
    from game.Game import Game

from .AbstractState import AbstractState


class RoundThreeState(AbstractState):
    pass


class RoundThreeStateSpectatingWaiting(RoundThreeState):
    pass


class RoundThreeStateSpectatingAnswering(RoundThreeState):
    pass


class RoundThreeStateChasedWaiting(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send({"action": "round_three_chased_waiting"})

    @classmethod
    async def action_notify_ready(cls, _msg, client: Client) -> Optional[AbstractState]:
        client.current_game.round_three_module.ready_chased.add(client)
        if client.current_game.round_three_module.are_all_chased_clients_ready:
            return RoundThreeStateChasedReadyLast()
        return RoundThreeStateChasedReady()


RoundThreeStateChasedWaiting.actions = {
    "notify_ready": RoundThreeStateChasedWaiting.action_notify_ready
}


class RoundThreeStateChasedReady(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send({"action": "ack_round_three_chased_ready"})


class RoundThreeStateChasedReadyLast(RoundThreeState):

    @classmethod
    async def round_3_timer_expired(cls, game: Game):
        await game.send_to_all({"action": "timer_expired"})
        # TODO I get the horrible feeling this is racy as well

        # Move everyone to the right state
        # Chased to spectating
        # Chasers to waiting
        # Spectators to something idk
        # state_changes = [
        #     guest.change_state(RoundThreeStateSelectingOffer()) for guest in game.guests
        # ]
        # state_changes.append(game.host.change_state(RoundTwoStateSelectingOffer()))
        # if state_changes:
        #     await asyncio.wait(state_changes)

    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send({"action": "ack_round_three_chased_ready"})

        state_transitions = [
            c.change_state(RoundThreeStateChasedAnswering())
            for c in client.current_game.round_three_module.chased_clients
            if c is not client
        ]
        await client.current_game.round_three_module.get_next_question()
        client.current_game.round_three_module.reset_timer(cls.round_3_timer_expired)
        await asyncio.wait(state_transitions)
        return RoundThreeStateChasedAnswering()


class RoundThreeStateChasedAnswering(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await cls.get_and_send_question(client)

    @classmethod
    async def action_answer_question(
        cls, msg, client: Client
    ) -> Optional[AbstractState]:
        if "answer_index" not in msg or not isinstance(msg["answer_index"], int):
            return None
        if client.current_game is None:
            logging.error(
                "Tried to enter %s state without being in a game???", cls.__name__
            )
            return
        current_question = client.current_game.round_three_module.current_question
        if msg["answer_index"] == current_question.correct_index:
            client.current_game.round_three_module.add_chased_correct_answer()
        client.current_answer_index = msg["answer_index"]

        other_state_transitions = [
            c.change_state(RoundThreeStateChasedDidNotAnswer())
            for c in client.current_game.round_three_module.chased_clients
            if c is not client
        ]
        # TODO Yes i know this is a race condition but i'm losing it dude
        if other_state_transitions:
            asyncio.wait(other_state_transitions)
        return RoundThreeStateChasedAnswered()

    @classmethod
    async def get_and_send_question(cls, client: Client):
        question: Optional[
            Question
        ] = client.current_game.round_three_module.current_question
        if question is None:
            logging.error("Tried to get a question but question was None :O")
            return
        await client.send(
            {
                "action": "round_3_chased_question",
                "question": question.question,
                "answers": question.shuffled_answers,
                "time_remaining": client.current_game.round_three_module.time_remaining,
            }
        )


RoundThreeStateChasedAnswering.actions = {
    "answer_question": RoundThreeStateChasedAnswering.action_answer_question
}


class RoundThreeStateChasedAnswered(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, _old_state: AbstractState
    ) -> Optional[AbstractState]:
        current_game = client.current_game
        current_question = current_game.round_three_module.current_question
        # TODO We need to send this to all
        await client.send(
            {
                "action": "question_answered",
                "correct_answer": current_question.correct_index,
                "given_answer": client.current_answer_index,
                "round_3_score": current_game.round_three_module.chased_num_questions_correct,
            }
        )
        # We need to transition everyone 
        # return RoundOneStateAnswering()


class RoundThreeStateChasedDidNotAnswer(RoundThreeState):
    pass


class RoundThreeStateChasedWatching(RoundThreeState):
    pass


class RoundThreeStateChaserWaiting(RoundThreeState):
    pass


class RoundThreeStateChaserReady(RoundThreeState):
    pass


class RoundThreeStateChaserReadyLast(RoundThreeState):
    pass


class RoundThreeStateChaserWatching(RoundThreeState):
    pass


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
    @classmethod
    async def get_and_send_question(cls, client: Client):
        # Need a way to have one question being asked at a time, index etc in module
        question: Question = (
            await client.current_game.round_three_module.get_current_question()
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


class RoundThreeStateAnswered(RoundThreeState):
    pass
