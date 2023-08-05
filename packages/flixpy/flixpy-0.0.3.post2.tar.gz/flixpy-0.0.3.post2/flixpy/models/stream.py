from ..enums.streaming_provider import StreamingProvider


class Stream:
    def __init__(self, source_name: str, url: str) -> None:
        self.streaming_provider = StreamingProvider(source_name)
        self.url = url

    def __repr__(self) -> str:
        return f"<Steam {self.streaming_provider.value}>"
