class Question:

    def __init__(self):
        self.category: str
        self.question_type: str
        self.difficulty: str
        self.question: str
        self.correct_answer: str
        self.incorrect_answers: list[str]
