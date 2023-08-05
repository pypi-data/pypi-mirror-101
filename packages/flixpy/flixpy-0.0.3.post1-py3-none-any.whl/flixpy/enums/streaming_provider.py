from enum import unique, auto
from .auto_enum import AutoEnumLower


@unique
class StreamingProvider(AutoEnumLower):
    NETFLIX = auto()
    HULU = auto()
    AMAZON_PRIME = auto()
    AMAZON_BUY = auto()
    DISNEY_PLUS = auto()
    HBO_MAX = auto()
    HBO = auto()
    APPLE_TV_PLUS = auto()
    ITUNES = auto()
    GOOGLE_PLAY = auto()
    MICROSOFT = auto()
    FUBO_TV = auto()
    STARZ = auto()
    EPIX = auto()
    FUNIMATION = auto()
    KANOPY = auto()
    BRITBOX = auto()
    MUBI = auto()
    FANDOR = auto()
    HALLMARK_MOVIES_NOW = auto()
    SHUDDER = auto()
    INDIEFLIX = auto()
    SHOWTIME = auto()
    CBS_ALL_ACCESS = auto()
    CRUNCYROLL_PREMIUM = auto()
    AMC_PREMIERE = auto()
    CRITERION_CHANNEL = auto()
    DC_UNIVERSE = auto()
    CINEMAX = auto()
    ACORNTV = auto()
    BET_PLUS = auto()
    YOUTUBE_PREMIUM = auto()
    YOUTUBE_PURCHASE = auto()
    VUDU = auto()
    TVISION = auto()

    AMC = auto()
    CARTOON_NETWORK = auto()
    TBS = auto()
    TNT = auto()
    IFC = auto()

    ABC = "abc_tveverywhere"
    A_AND_E = "ae_tveverywhere"
    FX = "fx_tveverywhere"
    FOX = "fox_tveverywhere"
    NBC = "nbc_tveverywhere"
    USA = "usa_tveverywhere"
    COMEDY_CENTRAL = "comedy_central_tveverywhere"
    FOOD_NETWORK = "watch_food_network"
    DISNEY = "watchdisney_tveverywhere"
    BET = "bet_tveverywhere"
    ADULT_SWIM = "adult_swim_tveverywhere"
    E = "e_tveverywhere"
    HALLMARK = "hallmark_tveverywhere"
    HISTORY = "history_tveverywhere"
    LIFETIME = "lifetime_tveverywhere"
    NATGEO = "natgeo_tveverywhere"
    TVLAND = "tvland_tveverywhere"
    BRAVO = "bravo_tveverywhere"
    HGTV = "watch_hgtv"
    SUNDANCE = "sundance_tveverywhere"
    SYFY = "syfy_tveverywhere"
    MTV = "mtv_tveverywhere"
    VH1 = "vh1_tveverywhere"
    TRAVEL_CHANNEL = "watch_travel_channel"
    DIY = "watch_diy_network"
    NICK = "nick_tveverywhere"
    BBC_AMERICA = "bbc_america_tve"
    FYI = "fyi_tveverywhere"
    TCM = "watch_tcm"
    VICELAND = "viceland_tve"
    TRUTV = "trutv_tveverywhere"
    CNBC = "cnbc_tveverywhere"
    SCIENCE = "science_go"
    TLC = "tlc_go"
