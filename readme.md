Slack++
=======

An augmented version of the Slack API Client for Python.

The primary function of this library is a class generator which applies features
onto the existing library methods of the `slack_sdk.web.client.WebClient`.

```python
from slack_plus import SlackClient, client, FEATURES

# The following three lines evaluate to equivalent values:
SlackClient
client()
client(*FEATURES.keys())

# Pass a list of your desired feature labels to the client method to generate
# a new version of the client:
CustomSlackClient = client('rate-limit', 'response-cache')
```

The following features are already implemented:

| Name | Methods | Description |
|------|---------|-------------|
| rate-limit | `api_call` | Intercept Rate Limit errors and wait until the limit has reset to allow more requests |
| response-cache | select methods | Wrap the method with `functools.cache` for in-memory memoization of the result |
| pagination | paginated methods | For methods that use cursor-based pagination, collect all pages and return them in one value |
