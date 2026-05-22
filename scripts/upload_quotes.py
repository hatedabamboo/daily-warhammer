#!/usr/bin/env python3
"""Upload quotes from the quotes/ directory to DynamoDB, skipping any that already exist."""

import json
import os
import sys
from pathlib import Path

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "daily-warhammer-quotes")
QUOTES_DIR = Path(__file__).parent.parent / "quotes"


def load_quotes(path: Path) -> list[dict]:  # type: ignore[type-arg]
    items = json.loads(path.read_text())
    return [{"quote_id": q["quote_id"], "text": q["text"], "source": q["source"], "last_used": None} for q in items]


def upload(table, items: list[dict]) -> tuple[int, int]:  # type: ignore[type-arg]
    added = skipped = 0
    for item in items:
        try:
            table.put_item(
                Item=item,
                ConditionExpression=Attr("quote_id").not_exists(),
            )
            added += 1
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                skipped += 1
            else:
                raise
    return added, skipped


def main() -> None:
    files = sorted(QUOTES_DIR.glob("*.json"))
    if not files:
        print(f"No JSON files found in {QUOTES_DIR}")
        sys.exit(1)

    table = boto3.resource("dynamodb").Table(TABLE_NAME)
    total_added = total_skipped = 0

    for path in files:
        items = load_quotes(path)
        added, skipped = upload(table, items)
        total_added += added
        total_skipped += skipped
        print(f"{path.name}: {added} added, {skipped} skipped")

    print(f"\nTotal: {total_added} added, {total_skipped} skipped")


if __name__ == "__main__":
    main()
