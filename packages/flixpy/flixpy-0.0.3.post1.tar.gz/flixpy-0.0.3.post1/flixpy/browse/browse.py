import concurrent.futures
from enum import Enum, unique
from urllib.parse import urlencode
from typing import Union

from flixpy.utils import get_json
from flixpy.constants import BASE_URL
from flixpy.enums.streaming_provider import StreamingProvider
from flixpy.enums.genre import Genre
from flixpy.enums.tag import Tag
from flixpy.models.movie import Movie
from flixpy.models.show.show import Show


@unique
class Type(Enum):
    STREAMING_PROVIDER = "source"
    GENRE = "genre"
    TAG = "tag"


@unique
class Sort(Enum):
    # These values were found from the URL on the Reelgood search page
    IMDB_RATING = 2
    REALEASE_DATE = 3
    ALPHABETICALLY = 4


class Browse:
    def __init__(self) -> None:
        """
        By default, there are no streaming providers, but this can be set in
        by_streaming_provider. If

        Examples:
            .../browse/source/_?genre=5&tag=superhero&availability=onAnySource
            .../browse/genre/5/?tag=superhero&availability=onAnySource

        Both are of genre Action and Adventure and tag superhero from ANY
        streaming platform. There is no streaming platform called "_", and even
        if there was, this query will get content from any streaming platform
        because of `availability=onAnySource`.

        In order to keep things simpler, we always use the `/browse/source` API
        even if no streaming provider is provided. The default streaming
        providier is "_".

        The following should return the same set of content:
            - `Browse().by_genre(Genre.ACTION_AND_ADVENTURE).by_tag(Tag.SUPERHERO).get()`
            - `Browse().by_tag(Tag.SUPERHERO).by_genre(Genre.ACTION_AND_ADVENTURE).get()`

        Both will return results from the APIs:
            - https://api.reelgood.com/v3.0/content/browse/source/_?genre=5&tag=superhero&availability=onAnySource
            - https://api.reelgood.com/v3.0/content/browse/source/_?tag=superhero&genre=5&availability=onAnySource
        """

        self.source = "_"
        """
        "_" doesn't mean anything, but some string is required here. The
        string can be anything because it is always overriden by
        availability=onAnySource
        """

        self.browse_dictionary = {}
        self.streaming_provider = None

    def by_streaming_provider(self, streaming_provider: Union[StreamingProvider, None]):
        if streaming_provider is not None:
            self.streaming_provider = streaming_provider
            self.source = streaming_provider.value
        return self

    def by_genre(self, genre: Union[Genre, None]):
        if genre is not None:
            self.type = Type.GENRE
            self.browse_dictionary["genre"] = genre.value
        return self

    def by_tag(self, tag: Union[Tag, None]):
        if tag is not None:
            self.type = Type.TAG
            self.browse_dictionary["tag"] = tag.value
        return self

    def skipping(self, skip: int = 0):
        """Specify the number of movies/shows to skip.

        Use to go to the next page in the API. Each page contains 30 results.
        """

        self.browse_dictionary["skip"] = str(skip)

        return self

    @property
    def api_url(self) -> str:
        # If by genre or tag, but not streaming_provider, set to any source
        if self.streaming_provider is None and self.type in [Type.GENRE, Type.TAG]:
            self.browse_dictionary["availability"] = "onAnySource"

        url = f"{BASE_URL}/browse/source/{self.source}?{urlencode(self.browse_dictionary)}"
        return url

    def get(self):
        results = get_json(self.api_url)["results"]

        slugs_list = [result["slug"] for result in results]
        content_type_list = [result["content_type"] for result in results]

        # Fetch results for each movie/show concurrently to reduce time
        with concurrent.futures.ThreadPoolExecutor(max_workers=90) as executor:
            content_list = executor.map(
                _get_movie_or_slug,
                slugs_list,
                content_type_list,
            )

            return list(content_list)


def _get_movie_or_slug(slug, content_type):
    """Return a movie or show from the slug based on the content type"""

    if content_type == "m":
        return Movie(slug)
    return Show(slug)
