class AccountModel:
    _username: str
    _rating: int

    def __init__(self, username: str, rating: int):
        self.username = username
        self.rating = rating

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        if ' ' in value:
            raise ValueError('Username must be without spaces')
        if not value:
            raise ValueError('Username must be not empty')
        self._username = value

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, value: int):
        if value < 0:
            raise ValueError('Rating must be positive or 0')
        self._rating = value
