import random
from typing import Tuple


class Question:
    def __init__(self, question_dict: dict):
        self.category: str = question_dict["category"]
        self.question_type: str = question_dict["type"]
        self.difficulty: str = question_dict["difficulty"]
        self.question: str = question_dict["question"]
        self.correct_answer: str = question_dict["correct_answer"]
        self.incorrect_answers: list[str] = question_dict["incorrect_answers"]
        shuffled_answers, correct_index = self.make_shuffled_answers()
        self.shuffled_answers: list[str] = shuffled_answers
        self.correct_index: int = correct_index

    def __str__(self):
        return f"{self.category=}, {self.question_type=}, {self.difficulty=}, {self.question=}, {self.correct_answer=}, {self.incorrect_answers=}"

    def make_shuffled_answers(self) -> Tuple[list[str], int]:
        shuffled_answers = self.incorrect_answers + [self.correct_answer]
        random.shuffle(shuffled_answers)
        correct_index = shuffled_answers.index(self.correct_answer)
        return shuffled_answers, correct_index
