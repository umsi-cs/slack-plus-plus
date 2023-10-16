"""
Modify the SlackClient to handle rate limit errors by waiting and retrying.
"""

import time
import logging

from functools import wraps
from slack_sdk.web import WebClient
from slack_sdk.errors import SlackApiError

from .api import MethodMap

log = logging.getLogger("slack")


class RateLimitedSlackClient(WebClient):
    def api_call(self, *args, **kwargs):
        """Wrap API calls to handle common errors"""

        try:
            return super().api_call(*args, **kwargs)
        except SlackApiError as err:
            if err.response["error"] == "ratelimited":
                log.warning(
                    "Slack API rate limit exceeded. Retrying in %s seconds",
                    err.response.headers["Retry-After"],
                )
                time.sleep(int(err.response.headers["Retry-After"]))
                return self.api_call(*args, **kwargs)

            raise err from err


def rate_limit(methods: MethodMap) -> MethodMap:
    """Wrap methods to handle rate limit errors"""

    super_method = methods["api_call"]

    @wraps(super_method)
    def api_call(self, *args, **kwargs):
        try:
            return super_method(self, *args, **kwargs)
        except SlackApiError as err:
            if err.response["error"] == "ratelimited":
                log.warning(
                    "Slack API rate limit exceeded. Retrying in %s seconds",
                    err.response.headers["Retry-After"],
                )
                time.sleep(int(err.response.headers["Retry-After"]))
                return super_method(self, *args, **kwargs)

            raise err from err

    methods["api_call"] = api_call

    return methods
