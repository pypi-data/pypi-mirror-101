import datetime
from flixpy.models.show.episode import Episode
from flixpy.models.show.season import Season
from typing import List

from flixpy.enums.content_type import ContentType
from flixpy.models.base_content_model import BaseContentModel


class Show(BaseContentModel):
    """Show class

    Attributes
        completed_on
        seasons

    Methods
        __len__
        __getitem__
    """

    def __init__(self, slug_or_id: str) -> None:
        super().__init__(slug_or_id, content_type=ContentType.SHOW)

        if self._json["completed_on"] is not None:
            self.completed_on = datetime.datetime.strptime(self._json["completed_on"], "%Y-%m-%dT%H:%M:%SZ")
        else:
            self.completed_on = None

    @property
    def seasons(self) -> List[Season]:
        seasons_list: List[Season] = []

        """
        episodes_json contains a dictionary of all episodes

        {
            episode_id_1: {
                ...episode information
            },
            episode_id_2: ...
        }

        The keys are not in order
        """
        episodes_json = self._json["episodes"]

        """
        seasons_json contains a list of all seasons

        [
            {
                number: season_no,
                ...,
                episodes: [
                    ...list of episodes IDs
                ]
            }
        ]
        """
        seasons_json = self._json["seasons"]

        for season_json in seasons_json:
            episodes_list: List[Episode] = []  # will be populated in this loop
            episode_id_list = season_json["episodes"]  # see above comment

            for episode_id in episode_id_list:
                episode_json = episodes_json[episode_id]

                # Create the episode ...
                if episode_json["aired_at"] is not None:
                    # Get datetime, and convert to date
                    aired_on = datetime.datetime.strptime(
                        episode_json["aired_at"].split("T")[0],
                        "%Y-%m-%d",
                    ).date()
                else:
                    aired_on = None

                episode = Episode(
                    id=episode_id,
                    season_no=season_json["number"],
                    episode_no=episode_json["number"],
                    title=episode_json["title"],
                    availability=episode_json["availability"],
                    overview=episode_json["overview"],
                    aired_on=aired_on,
                )

                # ... then add it to the list
                episodes_list.append(episode)

            # We have all the episodes, so create the season ...
            season = Season(
                show_slug=self.slug,
                season_id=season_json["id"],
                season_no=season_json["number"],
                episodes=episodes_list,
            )

            # ... then add it to the seasons list
            seasons_list.append(season)

        # Reelgood provides seasons in the reverse order (season 1 last)
        seasons_list.reverse()

        return seasons_list

    def __len__(self):
        """Get the length of a show in seasons

        >>> show = Show('breaking-bad-2008')
        >>> len(show)
        5
        """

        return len(self.seasons)

    def __getitem__(self, season_no: int) -> Season:
        """Get a season (make a show like an array)

        >>> show = Show('breaking-bad-2008')
        >>> season_one = show[0]

        Or
        >>> for season in show:
        >>>     print(season)
        """

        return self.seasons[season_no]
