from typing import Union, Callable
from flixpy.enums.streaming_provider import StreamingProvider
from flixpy.models.use_streaming_provider import get_streams, is_on, link_for
from flixpy.enums.content_type import ContentType
from .base_content_model import BaseContentModel


class Movie(BaseContentModel):
    """Movie class

    Attributes:
        streaming_providers
        _availaility (dict): JSON containing all provider
        information
    """

    def __init__(self, slug_or_id: str) -> None:
        super().__init__(slug_or_id, content_type=ContentType.MOVIE)

        # Dictionary with JSON of all streaming provider data
        self._availability = self._json["availability"]

        """Composition functions for streams"""
        self.streams = get_streams(self._availability)
        self.is_on: Callable[[StreamingProvider], bool] = lambda streaming_provider: is_on(
            streaming_provider, self.streams
        )
        self.link_for: Callable[[StreamingProvider], Union[str, None]] = lambda streaming_provider: link_for(
            streaming_provider, self.streams
        )
