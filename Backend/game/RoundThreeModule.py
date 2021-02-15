from __future__ import annotations

import asyncio
import logging
import random

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from game.Game import Game
    from game.Question import Question
    from client.Client import Client
    from asyncio import TimerHandle


class RoundThreeModule:

    ROUND_THREE_TIMER_LENGTH = 60

    def __init__(self, game: Game):
        self._game: Game = game
        self.chased_num_questions_correct: int = 0
        self._question_list: list[Question] = []
        self._timer: Optional[TimerHandle] = None
        self.current_question: Optional[Question] = None
        self.playing_clients: set[Client] = set()
        self.ready_chasers: set[Client] = set()
        self.ready_chased: set[Client] = set()
        self.chased_clients: set[Client] = set()
        self.chaser_clients: set[Client] = set()

    async def get_next_question(self) -> Question:
        question: Question = await self._game.question_handler.get_next_question()
        self._question_list.append(question)
        self.current_question = question
        return question

    def reset_timer(self, callback, *args):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = asyncio.get_event_loop().call_later(
            self.ROUND_THREE_TIMER_LENGTH,
            asyncio.create_task,
            callback(self._game, *args),
        )

    @property
    def chased_time_remaining(self) -> Optional[float]:
        if self._timer is None or self._timer.cancelled():
            return None
        return self._timer.when() - asyncio.get_event_loop().time()

    def add_chased_correct_answer(self) -> None:
        self.chased_num_questions_correct += 1

    @property
    def are_all_chased_clients_ready(self):
        assert self.ready_chased.issubset(self.chased_clients)
        return self.chased_clients == self.ready_chased

    @property
    def are_all_chaser_clients_ready(self):
        assert self.ready_chasers.issubset(self.chaser_clients)
        return self.chaser_clients == self.ready_chasers

    def split_clients(self):
        if len(self.playing_clients) <= 1:
            logging.warning(
                "Tried to split clients with insufficent number of clients."
            )
        client_list: list[Client] = list(self.playing_clients)
        random.shuffle(client_list)

        self.chaser_clients = set(client_list[: len(client_list) // 2])
        self.chased_clients = set(client_list[len(client_list) // 2 :])
