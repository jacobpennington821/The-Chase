class Question:
    def __init__(self, question_dict: dict):
        self.category: str = question_dict["category"]
        self.question_type: str = question_dict["type"]
        self.difficulty: str = question_dict["difficulty"]
        self.question: str = question_dict["question"]
        self.correct_answer: str = question_dict["correct_answer"]
        self.incorrect_answers: list[str] = question_dict["incorrect_answers"]

    def __str__(self):
        return f"{self.category=}, {self.question_type=}, {self.difficulty=}, {self.question=}, {self.correct_answer=}, {self.incorrect_answers=}"
