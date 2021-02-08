from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.Game import Game
    from client.Client import Client
    from game.Question import Question

class RoundOneModule:

    ROUND_ONE_TIMER_LENGTH = 60
    ROUND_ONE_SCORE_PER_QUESTION = 1000

    def __init__(self, game: Game):
        self._game = game
        self.score: dict[Client, int] = {}
        self._question_list: list[Question] = []
        self._client_current_question_index: dict[Client, int] = {}

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
        self._client_current_question_index[client] += 1
        return question
