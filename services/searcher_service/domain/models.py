from dataclasses import dataclass


@dataclass(frozen=True)
class SearchParameters:
    min_rating: int
    max_rating: int


@dataclass(frozen=True)
class WaitingPlayer:
    name: str
    rating: int
    parameters: SearchParameters

    def check_opponent(self, opponent: "WaitingPlayer") -> bool:
        return self.parameters.min_rating <= opponent.rating <= self.parameters.max_rating
