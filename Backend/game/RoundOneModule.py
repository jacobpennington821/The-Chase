from __future__ import annotations
import asyncio

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from game.Game import Game
    from game.Question import Question
    from client.Client import Client
    from asyncio import TimerHandle


class RoundOneModule:

    ROUND_ONE_TIMER_LENGTH = 60
    ROUND_ONE_SCORE_PER_QUESTION = 1000

    def __init__(self, game: Game):
        self._game = game
        self.score: dict[Client, int] = {}
        self._question_list: list[Question] = []
        self._client_current_question_index: dict[Client, int] = {}
        self._timer: Optional[TimerHandle] = None
        self.client_question: dict[Client, Question] = {}

    def start_round(self):
        for client in self._game.clients:
            self.score[client] = 0
            self._client_current_question_index[client] = 0

    async def get_next_question(self, client: Client) -> Question:
        current_question_index: int = self._client_current_question_index[client]
        if len(self._question_list) == current_question_index:
            question: Question = await self._game.question_handler.get_next_question()
            self._question_list.append(question)
        question = self._question_list[current_question_index]
        self.client_question[client] = question
        self._client_current_question_index[client] += 1
        return question

    def reset_timer(self, callback, *args):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = asyncio.get_event_loop().call_later(
            self.ROUND_ONE_TIMER_LENGTH,
            asyncio.create_task,
            callback(self._game, *args),
        )

    @property
    def time_remaining(self) -> Optional[float]:
        if self._timer is None or self._timer.cancelled():
            return None
        return self._timer.when() - asyncio.get_event_loop().time()

    def get_client_score(self, client: Client) -> int:
        return self.score[client]

    def add_correct_answer(self, client: Client) -> None:
        self.score[client] += self.ROUND_ONE_SCORE_PER_QUESTION
