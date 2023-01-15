from dataclasses import dataclass
from aievents import Events
from . import adapters, models


@dataclass(frozen=True)
class OnFindOpponentMessage:
    created_session: adapters.Session
    caller: models.WaitingPlayer


class SearcherEvents(Events):
    __events__ = ('on_find_opponent', )


searcher_events = SearcherEvents()
print('Initialized events')