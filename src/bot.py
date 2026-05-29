import logging
import os

from atproto import Client, client_utils

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

    def _build_post(self, quote: Quote, hashtags: list[str]) -> client_utils.TextBuilder:
        tb = client_utils.TextBuilder()
        tb.text(f'"{quote.text}"\n\n— {quote.source}\n\n')
        for i, tag in enumerate(hashtags):
            if i > 0:
                tb.text(" ")
            tb.tag(tag, tag.lstrip("#"))
        return tb

    def _post_length(self, quote: Quote, hashtags: list[str]) -> int:
        tags_str = " ".join(hashtags)
        return len(f'"{quote.text}"\n\n— {quote.source}\n\n{tags_str}')

    def _truncate(self, quote: Quote) -> client_utils.TextBuilder:
        for n in range(len(DEFAULT_HASHTAGS), -1, -1):
            if self._post_length(quote, DEFAULT_HASHTAGS[:n]) <= MAX_POST_LENGTH:
                return self._build_post(quote, DEFAULT_HASHTAGS[:n])

        base = f'"{quote.text}"\n\n— '
        truncated_source = quote.source[: max(MAX_POST_LENGTH - len(base), 0)]
        tb = client_utils.TextBuilder()
        tb.text(f"{base}{truncated_source}")
        return tb

    def post(self, quote: Quote) -> None:
        if self._post_length(quote, DEFAULT_HASHTAGS) > MAX_POST_LENGTH:
            logger.warning("post too long, truncating")
            post = self._truncate(quote)
        else:
            post = self._build_post(quote, DEFAULT_HASHTAGS)
        response = self._client.send_post(post)
        logger.info("posted uri=%s", response.uri)
