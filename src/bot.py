import logging
import os

from atproto import Client

from src.models import Quote

logger = logging.getLogger(__name__)


class BlueskyBot:
    def __init__(self) -> None:
        self._client = Client()
        self._client.login(
            login=os.environ["BLUESKY_HANDLE"],
            password=os.environ["BLUESKY_PASSWORD"],
        )

    def post(self, quote: Quote) -> None:
        text = f'"{quote.text}"\n\n— {quote.source}'
        response = self._client.send_post(text=text)
        logger.info("posted uri=%s", response.uri)
