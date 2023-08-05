from flixpy.models.show.episode import Episode
from typing import List


class Season:
    """Season class (for show)

    Attributes
        show_slug
        season_id
        season_no
        episodes

    Methods
        __len__
        __getitem__
    """

    def __init__(self, show_slug: str, season_id: str, season_no: int, episodes: List[Episode]) -> None:
        self.show_slug = show_slug
        self.season_id = season_id
        self.season_no = season_no
        self.episodes = episodes

    def __repr__(self) -> str:
        return f"<Season {self.show_slug} : {self.season_no}"

    def __len__(self):
        """Get the length of the season in episodes

        >>> show = Show('breaking-bad-2008')
        >>> season_one = show[0]
        >>> len[season_one]
        10
        """

        return len(self.episodes)

    def __getitem__(self, episode_no: int) -> Episode:
        """Get a specific episode in the show

        >>> show = Show('breaking-bad-2008')
        >>> season_one = show[0]
        >>> for episode in season_one:
        >>>     print(episode)

        Or
        >>> show = Show('breaking-bad-2008')
        >>> season_one = show[0]
        >>> episode_one = season_one[0]
        """

        return self.episodes[episode_no]
