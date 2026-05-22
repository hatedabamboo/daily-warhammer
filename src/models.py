from dataclasses import dataclass, field


@dataclass(frozen=True)
class Quote:
    quote_id: str
    text: str
    source: str
    last_used: int | None = field(default=None)  # Unix timestamp; None means never posted
