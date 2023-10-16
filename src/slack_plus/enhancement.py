"""
Adds custom methods to the SlackClient class which go above and beyond the generic
improvements provided by the other features.
"""


import warnings
from slack_sdk.web import WebClient

from .api import MethodMap
from .util import filter_list_by


class CustomSlackClient(WebClient):
    def get_channels_by(
        self,
        *,
        name: str | None = None,
        names: list[str] | None = None,
        ids: list[str] | None = None,
        **kwargs,
    ):
        """Return a list of channels matching the supplied names and/or ids."""

        channels = self.conversations_list(**kwargs)

        if name:
            names = [name]

        if names:
            return filter_list_by("name", names, channels)

        if ids:
            if len(ids) == 1:
                warnings.warn(
                    "get_channels_by(ids=...) with a single ID is very inefficient. "
                    "Use conversations_info(channel=...) instead to ensure you only "
                    "make one request to the Slack API."
                )
            return filter_list_by("id", ids, channels)

        raise RuntimeError("Must supply at least one of: name, names, or ids")


def enhancement(methods: MethodMap) -> MethodMap:
    """Add custom enhancement methods"""

    methods["get_channels_by"] = CustomSlackClient.get_channels_by

    return methods
