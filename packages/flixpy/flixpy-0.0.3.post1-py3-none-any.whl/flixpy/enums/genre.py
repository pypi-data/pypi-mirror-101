from enum import Enum, unique


@unique
class Genre(Enum):
    """All numbers are IDs used by reelgood"""

    ACTION_AND_ADVENTURE = 5
    ANIMATION = 6
    ANIME = 39
    BIOGRAPHY = 7
    CHILDREN = 8
    COMEDY = 9
    CRIME = 10
    CULT = 41
    DOCUMENTARY = 11
    FAMILY = 12
    FANTASY = 13
    FOOD = 15
    GAME_SHOW = 16
    HISTORY = 17
    HORROR = 19
    INDEPENDENT = 43
    LGBTQ = 37
    MUSICAL = 22
    MYSTERY = 23
    REALITY = 25
    ROMANCE = 4
    SCIENCE_FICTION = 26
    SPORT = 29
    STAND_UP_AND_TALK = 45
    THRILLER = 32
    TRAVEL = 33

    # TODO: finish this
