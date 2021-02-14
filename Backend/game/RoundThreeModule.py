from __future__ import annotations

import asyncio

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
        self.num_questions_correct: int = 0
        self._question_list: list[Question] = []
        self._timer: Optional[TimerHandle] = None
        self.current_question: Optional[Question] = None
        self.playing_clients: set[Client] = set()
        self.ready_clients: set[Client] = set()

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
    def time_remaining(self) -> Optional[float]:
        if self._timer is None or self._timer.cancelled():
            return None
        return self._timer.when() - asyncio.get_event_loop().time()

    def add_correct_answer(self) -> None:
        self.num_questions_correct += 1

    @property
    def are_all_clients_ready(self):
        assert self.ready_clients & self.playing_clients == self.ready_clients
        return self.ready_clients == self.playing_clients
