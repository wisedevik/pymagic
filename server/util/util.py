import string
import random

STRING_CHARACTERS = string.ascii_letters + string.digits

class Util:
    @staticmethod
    def random_string(len: int = 32):
        return ''.join(random.choice(STRING_CHARACTERS) for _ in range(len))
