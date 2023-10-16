"""
Modify the Slack client to unravel paginated responses.

Supports cursor-based pagination, but not classic pagination.
See more: https://api.slack.com/docs/pagination
"""

from typing import Callable, Any
from functools import wraps
from slack_sdk.web import WebClient, SlackResponse

from .api import MethodMap

key_map = {
    "conversations_history": "messages",
    "conversations_list": "conversations",
    "conversations_members": "members",
    "conversations_replies": "messages",
    "files_info": "file",
    "reactions_list": "items",
    "stars_list": "items",
    "users_list": "members",
    "usergroups_users_list": "users",
}


def collect_keys(key: str, collection: SlackResponse) -> list[Any]:
    """Return a list of dicts with the supplied key from the supplied collection."""

    data = []
    for page in collection:
        data += page[key]
    return data


def paginates_as(key: str) -> Callable:
    """
    Wrap a function that paginates its results to return a list of dicts with the
    supplied key.
    """

    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return collect_keys(key, func(*args, **kwargs))

        wrapper.__annotations__["return"] = list[dict]
        return wrapper

    return decorator


def unraveled_super_method(method_name, pagination_key):
    annotations = WebClient.__dict__[method_name].__annotations__

    annotations.pop("cursor", None)
    annotations.pop("limit", None)
    annotations["return"] = list[dict]

    def method(self, *args, **kwargs):
        superclass = super(PaginatedSlackClient, self)
        return collect_keys(
            pagination_key,
            getattr(superclass, method_name)(*args, **kwargs),
        )

    method.__annotations__ = annotations
    method.__doc__ = WebClient.__dict__[method_name].__doc__

    return method


PaginatedSlackClient = type(
    "PaginatedSlackClient",
    (WebClient,),
    {
        "__doc__": """Unwrap results of paginated Slack API calls""",
        **{
            method_name: unraveled_super_method(method_name, pagination_key)
            for method_name, pagination_key in key_map.items()
        },
    },
)


def pagination(methods: MethodMap) -> MethodMap:
    """Wrap methods to handle pagination"""

    for method_name, pagination_key in key_map.items():
        methods[method_name] = paginates_as(pagination_key)(methods[method_name])

    return methods
