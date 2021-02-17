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
        game.round_three_module.timer_expired = True
        await game.send_to_all({"action": "chased_timer_expired"})
        # TODO I get the horrible feeling this is racy as well

        # If the chased get 0 then just give up here
        if game.round_three_module.chased_num_questions_correct == 0:
            chased_state_changes = [
                c.change_state(RoundThreeStateChasedLost())
                for c in game.round_three_module.chased_clients
            ]
            # Chasers to waiting
            chaser_state_changes = [
                c.change_state(RoundThreeStateChaserWon())
                for c in game.round_three_module.chaser_clients
            ]

            spectator_state_changes = [
                c.change_state(RoundThreeStateSpectatorEnd())
                for c in game.clients
                if c not in game.round_three_module.chaser_clients
                and c not in game.round_three_module.chased_clients
            ]

            if chased_state_changes + chaser_state_changes + spectator_state_changes:
                await asyncio.wait(
                    chased_state_changes
                    + chaser_state_changes
                    + spectator_state_changes
                )

        else:
            # Move everyone to the right state
            # Chased to spectating
            chased_state_changes = [
                c.change_state(RoundThreeStateChasedWatching())
                for c in game.round_three_module.chased_clients
            ]
            # Chasers to waiting
            chaser_state_changes = [
                c.change_state(RoundThreeStateChaserWaiting())
                for c in game.round_three_module.chaser_clients
            ]

            if chased_state_changes + chaser_state_changes:
                await asyncio.wait(chased_state_changes + chaser_state_changes)
            # Spectators to something idk

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
        if state_transitions:
            await asyncio.wait(state_transitions)
        if not client.current_game.round_three_module.timer_expired:
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
        if other_state_transitions:
            asyncio.wait(other_state_transitions)
        # Think this fixes some of the races idk
        if not client.current_game.round_three_module.timer_expired:
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
        await current_game.send_to_all(
            {
                "action": "question_answered",
                "correct_answer": current_question.correct_index,
                "given_answer": client.current_answer_index,
                "round_3_score": current_game.round_three_module.chased_num_questions_correct,
            }
        )

        chased_state_transitions = [
            c.change_state(RoundThreeStateChasedAnswering())
            for c in current_game.round_three_module.chased_clients
            if c is not client
        ]
        # Again i know race condition
        if chased_state_transitions:
            await asyncio.wait(chased_state_transitions)
        if not client.current_game.round_three_module.timer_expired:
            return RoundThreeStateChasedAnswering()


class RoundThreeStateChasedDidNotAnswer(RoundThreeState):
    pass


class RoundThreeStateChasedWatching(RoundThreeState):
    pass


class RoundThreeStateChasedLost(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send(
            {
                "action": "game_over",
                "game_over": "chased_lost",
                "chased_score": client.current_game.round_three_module.chased_num_questions_correct,
                "chaser_score": client.current_game.round_three_module.chaser_num_questions_correct,
            }
        )


class RoundThreeStateChasedWon(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send(
            {
                "action": "game_over",
                "game_over": "chased_won",
                "chased_score": client.current_game.round_three_module.chased_num_questions_correct,
                "chaser_score": client.current_game.round_three_module.chaser_num_questions_correct,
            }
        )


class RoundThreeStateChaserWaiting(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send({"action": "round_three_chaser_waiting"})

    @classmethod
    async def action_notify_ready(cls, _msg, client: Client) -> Optional[AbstractState]:
        client.current_game.round_three_module.ready_chasers.add(client)
        if client.current_game.round_three_module.are_all_chaser_clients_ready:
            return RoundThreeStateChaserReadyLast()
        return RoundThreeStateChaserReady()


RoundThreeStateChaserWaiting.actions = {
    "notify_ready": RoundThreeStateChaserWaiting.action_notify_ready
}


class RoundThreeStateChaserReady(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send({"action": "ack_round_three_chaser_ready"})


class RoundThreeStateChaserReadyLast(RoundThreeState):
    @classmethod
    async def round_3_timer_expired(cls, game: Game):
        game.round_three_module.timer_expired = True
        await game.send_to_all({"action": "chaser_timer_expired"})
        # TODO Probably racy but meh

        # Move everyone to the right state
        # The chasers probably lost if we're here
        # Chased to spectating
        # TODO

        if game.round_three_module.have_chasers_caught_chased:
            chased_state_changes = [
                c.change_state(RoundThreeStateChasedLost())
                for c in game.round_three_module.chased_clients
            ]

            chaser_state_changes = [
                c.change_state(RoundThreeStateChaserWon())
                for c in game.round_three_module.chaser_clients
            ]
        else:
            chased_state_changes = [
                c.change_state(RoundThreeStateChasedWon())
                for c in game.round_three_module.chased_clients
            ]
            chaser_state_changes = [
                c.change_state(RoundThreeStateChaserLost())
                for c in game.round_three_module.chaser_clients
            ]

        spectator_state_changes = [
            c.change_state(RoundThreeStateSpectatorEnd())
            for c in game.clients
            if c not in game.round_three_module.chaser_clients
            and c not in game.round_three_module.chased_clients
        ]
        if chased_state_changes + chaser_state_changes + spectator_state_changes:
            await asyncio.wait(
                chased_state_changes + chaser_state_changes + spectator_state_changes
            )

    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send({"action": "ack_round_three_chaser_ready"})

        state_transitions = [
            c.change_state(RoundThreeStateChaserAnswering())
            for c in client.current_game.round_three_module.chaser_clients
            if c is not client
        ]
        await client.current_game.round_three_module.get_next_question()
        client.current_game.round_three_module.reset_timer(cls.round_3_timer_expired)
        if state_transitions:
            await asyncio.wait(state_transitions)
        if not client.current_game.round_three_module.timer_expired:
            return RoundThreeStateChaserAnswering()


class RoundThreeStateChaserWatching(RoundThreeState):
    pass


class RoundThreeStateChaserAnswering(RoundThreeState):
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
            client.current_game.round_three_module.add_chaser_correct_answer()
        client.current_answer_index = msg["answer_index"]

        other_state_transitions = [
            c.change_state(RoundThreeStateChaserDidNotAnswer())
            for c in client.current_game.round_three_module.chased_clients
            if c is not client
        ]
        if other_state_transitions:
            asyncio.wait(other_state_transitions)
        # Think this fixes some of the races idk
        if not client.current_game.round_three_module.timer_expired:
            return RoundThreeStateChaserAnswered()

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
                "action": "round_3_chaser_question",
                "question": question.question,
                "answers": question.shuffled_answers,
                "time_remaining": client.current_game.round_three_module.time_remaining,
            }
        )


RoundThreeStateChaserAnswering.actions = {
    "answer_question": RoundThreeStateChaserAnswering.action_answer_question
}


class RoundThreeStateChaserAnswered(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, _old_state: AbstractState
    ) -> Optional[AbstractState]:
        game = client.current_game
        current_question = game.round_three_module.current_question
        await game.send_to_all(
            {
                "action": "question_answered",
                "correct_answer": current_question.correct_index,
                "given_answer": client.current_answer_index,
                "chased_score": game.round_three_module.chased_num_questions_correct,
                "round_3_score": game.round_three_module.chaser_num_questions_correct,
            }
        )

        if game.round_three_module.have_chasers_caught_chased:
            # Move chasers to victory states
            # Move chased to loss states
            chased_state_changes = [
                c.change_state(RoundThreeStateChasedLost())
                for c in game.round_three_module.chased_clients
                if c is not client
            ]
            # Chasers to waiting
            chaser_state_changes = [
                c.change_state(RoundThreeStateChaserWon())
                for c in game.round_three_module.chaser_clients
                if c is not client
            ]

            spectator_state_changes = [
                c.change_state(RoundThreeStateSpectatorEnd())
                for c in game.clients
                if c not in game.round_three_module.chaser_clients
                and c not in game.round_three_module.chased_clients
                and c is not client
            ]

            if chased_state_changes + chaser_state_changes + spectator_state_changes:
                await asyncio.wait(
                    chased_state_changes
                    + chaser_state_changes
                    + spectator_state_changes
                )
            if client in game.round_three_module.chaser_clients:
                return RoundThreeStateChaserWon()
            if client in game.round_three_module.chased_clients:
                return RoundThreeStateChasedLost()
            return RoundThreeStateSpectatorEnd()

        else:
            chaser_state_transitions = [
                c.change_state(RoundThreeStateChaserAnswering())
                for c in game.round_three_module.chased_clients
                if c is not client
            ]
            # Again i know race condition
            if chaser_state_transitions:
                await asyncio.wait(chaser_state_transitions)
            if not game.round_three_module.timer_expired:
                return RoundThreeStateChaserAnswering()


class RoundThreeStateChaserDidNotAnswer(RoundThreeState):
    pass


class RoundThreeStateChaserLost(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send(
            {
                "action": "game_over",
                "game_over": "chaser_lost",
                "chased_score": client.current_game.round_three_module.chased_num_questions_correct,
                "chaser_score": client.current_game.round_three_module.chaser_num_questions_correct,
            }
        )


class RoundThreeStateChaserWon(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send(
            {
                "action": "game_over",
                "game_over": "chaser_won",
                "chased_score": client.current_game.round_three_module.chased_num_questions_correct,
                "chaser_score": client.current_game.round_three_module.chaser_num_questions_correct,
            }
        )


class RoundThreeStateSpectatorEnd(RoundThreeState):
    @classmethod
    async def enter_state(
        cls, client: Client, old_state: AbstractState
    ) -> Optional[AbstractState]:
        await client.send(
            {
                "action": "game_over",
                "game_over": "spectator_end",
                "chased_score": client.current_game.round_three_module.chased_num_questions_correct,
                "chaser_score": client.current_game.round_three_module.chaser_num_questions_correct,
            }
        )
