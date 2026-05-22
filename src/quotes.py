import os
import random
import time
from typing import TYPE_CHECKING, Any

import boto3
from boto3.dynamodb.conditions import Attr

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.type_defs import ScanOutputTableTypeDef

from src.models import Quote

ONE_MONTH_SECONDS = 30 * 24 * 60 * 60


class QuoteRepository:
    def __init__(self) -> None:
        self._table = boto3.resource("dynamodb").Table(os.environ["DYNAMODB_TABLE"])

    def get_random_quote(self) -> Quote:
        cutoff = int(time.time()) - ONE_MONTH_SECONDS
        filter_expr = (
            Attr("last_used").not_exists()
            | Attr("last_used").eq(None)
            | Attr("last_used").lt(cutoff)
        )

        response: ScanOutputTableTypeDef = self._table.scan(FilterExpression=filter_expr)
        items: list[dict[str, Any]] = list(response["Items"])
        while "LastEvaluatedKey" in response:
            response = self._table.scan(
                FilterExpression=filter_expr,
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            items.extend(response["Items"])

        if not items:
            raise RuntimeError("No eligible quotes (all used in the last 30 days)")

        item = random.choice(items)
        return Quote(
            quote_id=str(item["quote_id"]),
            text=str(item["text"]),
            source=str(item["source"]),
            last_used=int(item["last_used"]) if item.get("last_used") is not None else None,
        )

    def mark_used(self, quote_id: str) -> None:
        self._table.update_item(
            Key={"quote_id": quote_id},
            UpdateExpression="SET last_used = :ts",
            ExpressionAttributeValues={":ts": int(time.time())},
        )
