import datetime
from flixpy.enums.tag import Tag
from flixpy.enums.genre import Genre
from typing import Any, List, Union

from flixpy.constants import BASE_URL
from flixpy.enums.content_type import ContentType
from flixpy.utils import get_json


class BaseContentModel:
    """Base model class from which Movie and Show inherit from

    Attributes:
        content_type (ContentType)
        _json (dict): JSON dictionary returned from reelgood's API
        _endpoint (str)
        id (str): Content ID from reelgood
        slug (str)
        title (str)
        overview (str): Content overview/description
        released_on (dateTime)
        trailer (str): YouTube link for trailer
        genres (List[Genre])
        tags (List[Tag])
    """

    def __init__(self, slug_or_id: str, content_type: ContentType) -> None:
        self.content_type = content_type

        if self.content_type not in [ContentType.SHOW, content_type.MOVIE]:
            raise Exception(f"Invalid content_type {content_type}")

        self._endpoint = f"{BASE_URL}/{content_type.value}/{slug_or_id}"
        self._json = get_json(self._endpoint)

        # Set properties from API
        self.id = self._json["id"]
        self.slug = self._json["slug"]
        self.title = self._json["title"]
        self.overview = self._json["overview"]

        # released_on may or may not be available
        if self._json["released_on"] is not None:
            self.released_on = datetime.datetime.strptime(self._json["released_on"], "%Y-%m-%dT%H:%M:%SZ").date()
        else:
            self.released_on = None

    def __repr__(self) -> str:
        """Prettier string representation"""
        return f"<{self.content_type.value.capitalize()} {self.slug}>"

    def __eq__(self, other: object) -> bool:
        """Two 'contents' are the same if their slugs are the same

        A movie can never have the same slug as a show
        """

        return self.slug == other.slug

    @property
    def trailer(self) -> Union[str, None]:
        """Get YouTube trailer URL"""
        for trailer in self._json["trailers"]:
            if trailer["site"] == "youtube":
                return f'https://youtube.com/watch?v={trailer["key"]}'

        # TODO: return other trailers if youtube trailer isn't available
        return None

    @property
    def genres(self) -> List[Genre]:
        genre_list: List[Genre] = []

        for genre_id in self._json["genres"]:
            try:
                # If the genre ID hasn't been defined in the enum class, ignore
                # it for now
                genre_list.append(Genre(genre_id))
            except:
                pass

        return genre_list

    @property
    def tags(self) -> List[Tag]:
        tags_list: List[Tag] = []

        for tags_json in self._json["tags"]:
            tag_slug = tags_json["slug"]
            try:
                # If the tag slug hasn't been defined in the enum class, ignore
                # it for now
                tags_list.append(Tag(tag_slug))
            except:
                pass

        return tags_list

    @property
    def people(self) -> List[Any]:
        ...
