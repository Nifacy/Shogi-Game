class IdGenerator:
    _last_generated_id: int

    def __init__(self):
        self._last_generated_id = 0

    def generate_id(self) -> int:
        generated_id = self._last_generated_id
        self._last_generated_id += 1
        return generated_id
