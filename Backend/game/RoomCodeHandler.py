import random
import string

class RoomCodeHandler:

    LOBBY_CODE_LENGTH = 6

    def __init__(self):
        self.used_room_codes = set()

    def create_new_game_code(self) -> str:
        code_is_unique = False
        code = ""
        while not code_is_unique:
            code = "".join(random.choices(string.ascii_uppercase, k=self.LOBBY_CODE_LENGTH))
            code_is_unique = not self.is_code_in_use(code)

        self.used_room_codes.add(code)
        return code

    def is_code_in_use(self, code: str):
        return code in self.used_room_codes

    def free_room_code(self, code: str):
        self.used_room_codes.remove(code)
