"""
Slack++

An augmented version of the Slack API Client for Python.
"""

__version__ = "0.1.0"

import types
from functools import reduce
from slack_sdk.web import WebClient

from .api import MethodMap, TransformMap, MethodTransform
from .pagination import pagination
from .rate_limit import rate_limit
from .response_cache import response_cache

FEATURES: TransformMap = {
    "pagination": pagination,
    "rate_limit": rate_limit,
    "response_cache": response_cache,
}


def base_methods() -> MethodMap:
    """Return a map of all methods from the WebClient class."""

    return {
        name: method
        for name, method in reduce(
            lambda x, y: {**x, **y},
            [cls.__dict__ for cls in WebClient.__mro__],
        ).items()
        if isinstance(method, types.FunctionType)
    }


def lookup_method_transform(identifier: str | MethodTransform) -> MethodTransform:
    """Given an identifier, try to return a method transform."""

    if isinstance(identifier, types.FunctionType):
        return identifier

    if identifier in FEATURES:
        return FEATURES[identifier]

    # TODO: Try to import identifier as a custom feature

    raise ValueError(f"Unknown method transform: {identifier}")


def client(*features: str, **extras) -> type:
    """Generate a new client class based on a list of features."""

    if features == ():
        features = tuple(FEATURES.keys())

    methods = base_methods()

    for feature in features:
        transform = lookup_method_transform(feature)
        methods = transform(methods)

    return type(
        "SlackClient",
        (WebClient,),
        {
            "__doc__": """A Slack API client with the following features: %s"""
            % ", ".join(features),
            "__features__": features,
            **methods,
            **extras,
        },
    )


# Generate a default client with all features enabled
SlackClient = client()
