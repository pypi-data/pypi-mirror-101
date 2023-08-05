#!/usr/bin/env python3
"""
pushover
Send yourself notifications via https://pushover.net
Just set your pushover user ID to PUSHOVER_USER_ID
and your application API token to PUSHOVER_API_TOKEN
then call this script with the message you want to
send::

    $ some-command; pushover -s$? "make test finished!"

Copyright 2017 Alexander Rudy. All rights reserved.
"""
__author__ = """Alexander Rudy"""
__email__ = "pushover@alexrudy.net"

__version__ = "1.0.0a1"

import sys
import os

from typing import Dict
from typing import Optional


try:
    import requests
    import click
except ImportError:  # pragma: nocover
    print("{} requires 'click' and 'requests' to be installed".format(sys.argv[0]))
    sys.exit(1)


class ConnectionError(click.ClickException):
    exit_code = 3


class ResponseError(click.ClickException):
    exit_code = 4


class PushoverCredentials:
    def __init__(self, user_id: str, api_token: str) -> None:
        self.user_id = str(user_id)
        self.api_token = str(api_token)

    def apply(self, payload: Dict[str, str]) -> Dict[str, str]:
        """Apply these credentials to a payload"""
        payload["user"] = self.user_id
        payload["token"] = self.api_token
        return payload


def send_message(text: str, credentials: Optional[PushoverCredentials] = None) -> requests.Response:
    """Send a message"""
    payload = {"message": text}
    if credentials is None:
        credentials = discover_credentials()
    payload = credentials.apply(payload)
    try:
        r = requests.post("https://api.pushover.net/1/messages.json", data=payload, headers={"User-Agent": "Python"})
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError("Unable to connect to api.pushover.net") from e
    return r


class CredentialDiscoveryError(click.ClickException):
    exit_code = 2


def discover_credentials() -> PushoverCredentials:
    """Discover credentials from the environment."""
    if all(f"PUSHOVER_{var}" in os.environ for var in ("USER_ID", "API_TOKEN")):
        return PushoverCredentials(os.environ["PUSHOVER_USER_ID"], os.environ["PUSHOVER_API_TOKEN"])
    if all(f"PUSHOVER_{var}" in os.environ for var in ("USER_TOKEN", "APP_TOKEN")):
        return PushoverCredentials(os.environ["PUSHOVER_USER_TOKEN"], os.environ["PUSHOVER_APP_TOKEN"])
    raise CredentialDiscoveryError("Can't discover credentials!")


def status_message(status: int, message: str) -> str:
    """Construct a status message (presumably from a process exit code.)"""
    if status == 0:
        message += " \u2705"
    else:
        message += " \u274c {:d}".format(status)
    return message


@click.command()
@click.option("-s", "--status", type=int, help="Return code to use to infer status.", metavar="CODE", default=None)
@click.option(
    "--supress-exit-code/--no-supress-exit-code",
    default=False,
    help="Return an exit code representatitve of click, not one from the --status argument.",
)
@click.argument("message", nargs=-1)
def main(status: int, supress_exit_code: bool, message: str) -> None:
    """Send a message via the pushover service.

    All positional arguments are concatenated with spaces and sent as the message text.
    The argument `-s` or `--status` will accept an interger, designed to be a return code
    from the previous command. If the return code is 0, then a green emoji checkmark is
    added to the message, otherwise a red emoji X is added. This is designed to be used
    as follows:

    \b
        somecommand; pushover -s$? your message goes here

    Credentials are discovered via environment variables. Pushover requires a user ID and
    an API token. The following environment variables are checked:

    \b
    - PUSHOVER_USER_ID and PUSHOVER_API_TOKEN
    - PUSHOVER_USER_TOKEN and PUSHOVER_APP_TOKEN

    """

    message = " ".join(message)
    if status is not None:
        message = status_message(status, message)
    creds = discover_credentials()
    r = send_message(message, creds)
    if not r.status_code == 200:
        raise ResponseError(f"{r.status_code} {r.text}")

    if not supress_exit_code:
        sys.exit(status)


if __name__ == "__main__":  # pragma: nocover
    main()
