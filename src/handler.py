import json
import logging
from typing import Any

from src.bot import BlueskyBot
from src.quotes import QuoteRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger.info("daily-warhammer starting")
    repo = QuoteRepository()
    quote = repo.get_random_quote()
    logger.info("selected quote_id=%s", quote.quote_id)
    BlueskyBot().post(quote)
    repo.mark_used(quote.quote_id)
    return {"statusCode": 200, "body": json.dumps({"quote_id": quote.quote_id})}
