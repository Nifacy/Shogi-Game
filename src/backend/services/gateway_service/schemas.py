import pydantic


class AccountInfo(pydantic.BaseModel):
    username: str
    rating: int


class Registration(pydantic.BaseModel):
    username: str
    password: str


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class PrivateRoomInfo(pydantic.BaseModel):
    connection_key: str


class SearchParameters(pydantic.BaseModel):
    min_rating: int
    max_rating: int
