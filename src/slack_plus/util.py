"""
Functions which enable behavior, but don't directly add anything to the Slack Client.
"""

from typing import Any
from functools import reduce
from slack_sdk.web import SlackResponse


def collect_keys(key: str, collection: SlackResponse) -> list[Any]:
    """Return a list of dicts with the supplied key from the supplied collection."""

    data = []
    for page in collection:
        data += page[key]
    return data


def dotget(item: Any, key: str) -> Any | None:
    """
    Return the value of the supplied key from the supplied dict.
    Supports nested keys using dot notation.
    """
    keys = key.split(".")
    return reduce(
        lambda current, next_key: (
            current.get(next_key, None)
            if hasattr(current, "get")
            else getattr(current, str(next_key), None)
        ),
        keys,
        item,
    )


def filter_list_by(
    attr: str, query: list[str], collection: list[dict], case_sensitive=True
) -> list[dict]:
    """Return a list of dicts from the collection that match the supplied query."""

    if case_sensitive:

        def search(item):
            return dotget(item, attr) in query

    else:

        def search(item):
            return str(dotget(item, attr)).lower() in query

        query = [str(q).lower() for q in query]

    return list(filter(search, collection))
