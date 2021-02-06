import aiohttp
import logging
from typing import Deque
from game.Question import Question
from collections import deque


class QuestionHandler:

    def __init__(self):
        self.question_buffer: Deque[Question] = deque()
        self.question_buffer_size = 10
        self.question_url = "https://opentdb.com/api.php"
        # TODO: Use a session token
        self.session_token = None

    async def get_next_question(self) -> Question:
        if len(self.question_buffer) == 0:
            questions_added = await self._fill_question_buffer()
            if questions_added == 0:
                logging.error("Buffer has been starved!!!")

        return self.question_buffer.popleft()

    async def _fill_question_buffer(self) -> int:
        params = {
            "amount": str(self.question_buffer_size),
            "type": "multiple",
        }
        async with aiohttp.request("GET", self.question_url, params=params) as resp:
            question_response = await resp.json()
            if "response_code" not in question_response:
                logging.error("Question API response invalid, response=%s", str(question_response))
                return 0

            if question_response["response_code"] == 0:
                questions_added: int = 0
                for q in question_response["results"]:
                    try:
                        question = Question(q)
                        self.question_buffer.append(question)
                        questions_added += 1
                    except ValueError:
                        logging.error("Failed to parse question, question=%s", q)
                return questions_added
            else:
                logging.error("Got API response with error code %s", str(question_response["response_code"]))
                return 0
