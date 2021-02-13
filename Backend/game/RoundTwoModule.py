from __future__ import annotations

import logging
import random

from typing import TYPE_CHECKING, Tuple


if TYPE_CHECKING:
    from game.RoundOneModule import RoundOneModule
    from game.Game import Game
    from client.Client import Client
    from game.Question import Question


class RoundTwoModule:
    def __init__(self, game: Game):
        self._game = game
        self._round_one_module: RoundOneModule = game.round_one_module
        self.selected_offers: dict[Client, int] = {}
        self._generated_offers: dict[Client, Tuple[int, int, int]] = {}
        self.player_positions: dict[Client, int] = {}
        self.chaser_positions: dict[Client, int] = {}
        self.client_question: dict[Client, Question] = {}
        self._question_list: list[Question] = []
        self._client_current_question_index: dict[Client, int] = {}
        self.current_chaser_answer_index: dict[Client, int] = {}

    def generate_offer(self, client: Client) -> Tuple[int, int, int]:
        if client in self._generated_offers:
            return self._generated_offers[client]
        # Low offer has to be < half
        score = self._round_one_module.get_client_score(client)
        if score == 0:
            score = 100
        low_offer = int(
            random.randrange(score // 4, score // 2) - random.randrange(score // 2)
        )
        high_offer = random.randrange(int((score * 1.5)), int(score * 2.5))
        self._generated_offers[client] = low_offer, score, high_offer
        return low_offer, score, high_offer

    def pick_offer(self, client: Client, offer: int) -> bool:
        if offer not in self._generated_offers[client]:
            return False
        self.selected_offers[client] = offer
        offer_position = self._generated_offers[client].index(offer)
        self.player_positions[client] = offer_position + 3
        self.chaser_positions[client] = 7
        self._client_current_question_index[client] = 0
        return True

    @property
    def all_clients_submitted(self) -> bool:
        return set(self._game.clients) == set(self.selected_offers.keys())

    async def get_next_question(self, client: Client) -> Question:
        current_question_index: int = self._client_current_question_index[client]
        if len(self._question_list) == current_question_index:
            question: Question = await self._game.question_handler.get_next_question()
            self._question_list.append(question)
        question = self._question_list[current_question_index]
        self.client_question[client] = question
        self._client_current_question_index[client] += 1
        return question

    def add_correct_answer(self, client: Client):
        self.player_positions[client] -= 1
        self._run_chaser_turn(client)

    def add_incorrect_answer(self, client: Client):
        self._run_chaser_turn(client)

    def _run_chaser_turn(self, client: Client):
        question = self.client_question[client]
        rand = random.random()
        if question.difficulty == "easy":
            correct = rand < 0.95
        elif question.difficulty == "medium":
            correct = rand < 0.85
        else:
            correct = rand < 0.75

        if correct:
            chaser_answer = question.correct_answer
            self.chaser_positions[client] -= 1
        else:
            chaser_answer = random.choice(question.incorrect_answers)

        self.current_chaser_answer_index[client] = question.shuffled_answers.index(
            chaser_answer
        )
