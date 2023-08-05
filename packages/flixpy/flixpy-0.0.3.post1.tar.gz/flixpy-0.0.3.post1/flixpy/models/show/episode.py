import datetime
from typing import Callable, Dict, Union
from flixpy.enums.streaming_provider import StreamingProvider
from flixpy.models.use_streaming_provider import get_streams, is_on, link_for


class Episode:
    def __init__(
        self,
        id: str,
        season_no: int,
        episode_no: int,
        title: str,
        overview: str,
        aired_on: Union[datetime.date, None],
        availability: Dict,
    ) -> None:
        self.id = id
        self.season_no = season_no
        self.episode_no = episode_no
        self.title = title
        self.overview = overview
        self.aired_on = aired_on

        # Dictionary with JSON of all streaming provider data
        self._availability = availability

        """Composition functions for streams"""
        self.streams = get_streams(self._availability)
        self.is_on: Callable[[StreamingProvider], bool] = lambda streaming_provider: is_on(
            streaming_provider, self.streams
        )
        self.link_for: Callable[[StreamingProvider], Union[str, None]] = lambda streaming_provider: link_for(
            streaming_provider, self.streams
        )

    def __repr__(self):
        return f"<Episode {self.season_no}:{self.episode_no}>"
