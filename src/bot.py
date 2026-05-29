import logging
import os

from atproto import Client

from src.models import Quote

logger = logging.getLogger(__name__)

MAX_POST_LENGTH = 300
DEFAULT_HASHTAGS = ["#Warhammer", "#WarhammerCommunity", "#Warhammer40k", "#WH40K", "#Grimdark"]


class BlueskyBot:
    def __init__(self) -> None:
        self._client = Client()
        self._client.login(
            login=os.environ["BLUESKY_HANDLE"],
            password=os.environ["BLUESKY_PASSWORD"],
        )

    def _build_post(self, quote: Quote, hashtags: list[str]) -> str:
        tags_str = " ".join(hashtags)
        return f'"{quote.text}"\n\n— {quote.source}\n\n{tags_str}'

    def _truncate(self, quote: Quote) -> str:
        for n in range(len(DEFAULT_HASHTAGS), -1, -1):
            text = self._build_post(quote, DEFAULT_HASHTAGS[:n])
            if len(text) <= MAX_POST_LENGTH:
                return text

        base = f'"{quote.text}"\n\n— '
        truncated_source = quote.source[: max(MAX_POST_LENGTH - len(base), 0)]
        return f"{base}{truncated_source}"

    def post(self, quote: Quote) -> None:
        full_text = self._build_post(quote, DEFAULT_HASHTAGS)
        if len(full_text) > MAX_POST_LENGTH:
            logger.warning("post too long (%d chars), truncating", len(full_text))
            text = self._truncate(quote)
        else:
            text = full_text
        response = self._client.send_post(text=text)
        logger.info("posted uri=%s", response.uri)
