from flixpy.enums.streaming_provider import StreamingProvider
from flixpy.models.stream import Stream
from typing import Dict, List, Union


def get_streams(availaibility: Dict) -> List[Stream]:
    """Get a list of Streams based on the 'availbility' JSON for a movie or episode"""

    streams_list: List[Stream] = []

    for stream_json in availaibility:
        try:
            streams_list.append(
                Stream(
                    source_name=stream_json["source_name"],
                    url=stream_json["source_data"]["web_link"],
                )
            )
        except:
            pass

    return streams_list


def is_on(streaming_provider: StreamingProvider, streams: List[Stream]) -> bool:
    """Returns True if the movie is on the streaming platform

    Parameters:
        streaming_provider (StreamingProvider)
        streams (List[Stream]): exisitng streams from get_streams to check against

    """

    for stream in streams:
        if streaming_provider == stream.streaming_provider:
            return True

    return False


def link_for(streaming_provider: StreamingProvider, streams: List[Stream]) -> Union[str, None]:
    """
    Get the URL for a content on a particular streaming platform.
    Returns None if the content is not the platform
    """

    for stream in streams:
        if streaming_provider == stream.streaming_provider:
            return stream.url

    return None
