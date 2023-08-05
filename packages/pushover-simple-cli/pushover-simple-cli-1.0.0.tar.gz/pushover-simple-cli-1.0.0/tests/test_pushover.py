"""Tests for `pushover` package."""
import os
import urllib.parse

import pushover
import pytest
import responses
from click.testing import CliRunner


def test_command_line_help():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(pushover.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help" in help_result.output
    assert "Show this message and exit." in help_result.output


@pytest.fixture(scope="module", autouse=True)
def mask_credentials():
    os.environ.pop("PUSHOVER_USER_ID", None)
    os.environ.pop("PUSHOVER_API_TOKEN", None)


@pytest.fixture()
def credentials(monkeypatch):

    user_id = "pushover-user-id-for-test"
    api_token = "puhsover-token-for-test"
    monkeypatch.setenv("PUSHOVER_USER_ID", user_id)
    monkeypatch.setenv("PUSHOVER_API_TOKEN", api_token)

    yield pushover.PushoverCredentials(user_id, api_token)


@pytest.fixture(autouse=True)
def response():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture()
def service(response):
    response.add(responses.POST, "https://api.pushover.net/1/messages.json", body="Success", status=200)
    yield response


def get_message_from_body(body: str) -> str:
    data = urllib.parse.parse_qs(body)
    assert len(data["message"]) == 1
    return data["message"][0]


def test_basic_message(credentials, service):

    runner = CliRunner()

    result = runner.invoke(pushover.main, ["hello", "world"])

    assert result.exit_code == 0
    assert result.output == ""

    assert service.calls[0].request.url == "https://api.pushover.net/1/messages.json"
    message = get_message_from_body(service.calls[0].request.body)
    assert message == "hello world"

    data = urllib.parse.parse_qs(service.calls[0].request.body)
    assert data["user"] == [credentials.user_id]
    assert data["token"] == [credentials.api_token]


def test_alt_credentials(service, monkeypatch):

    monkeypatch.setenv("PUSHOVER_USER_TOKEN", "pushover-user-id-for-test")
    monkeypatch.setenv("PUSHOVER_APP_TOKEN", "puhsover-token-for-test")

    runner = CliRunner()

    result = runner.invoke(pushover.main, ["hello", "world"])

    assert result.exit_code == 0
    assert result.output == ""

    assert service.calls[0].request.url == "https://api.pushover.net/1/messages.json"
    message = get_message_from_body(service.calls[0].request.body)
    assert message == "hello world"


def test_no_credentials(response):
    runner = CliRunner()

    result = runner.invoke(pushover.main, ["hello", "world"])

    assert result.exit_code == 2
    assert result.output.strip() == "Error: Can't discover credentials!"

    assert len(response.calls) == 0


@pytest.mark.usefixtures("credentials")
def test_connection_error(response):
    runner = CliRunner()

    result = runner.invoke(pushover.main, ["hello", "world"])

    assert result.exit_code == 3
    assert result.output.strip() == "Error: Unable to connect to api.pushover.net"

    assert len(response.calls) == 1


@pytest.mark.usefixtures("credentials")
def test_failing_repsonse(response):

    response.add(responses.POST, "https://api.pushover.net/1/messages.json", status=400, body="Bad Request!")

    runner = CliRunner()

    result = runner.invoke(pushover.main, ["hello", "world"])

    assert result.exit_code == 4
    assert result.output.strip() == "Error: 400 Bad Request!"

    assert len(response.calls) == 1


@pytest.mark.usefixtures("credentials")
def test_status_code(service):
    runner = CliRunner()

    result = runner.invoke(pushover.main, ["hello", "world", "-s", "5"])
    assert result.exit_code == 5
    assert result.output == ""

    message = get_message_from_body(service.calls[0].request.body)
    assert "\u274c" in message


@pytest.mark.usefixtures("credentials")
def test_status_code_success(service):
    runner = CliRunner()

    result = runner.invoke(pushover.main, ["hello", "world", "-s", "0"])
    assert result.exit_code == 0
    assert result.output == ""

    message = get_message_from_body(service.calls[0].request.body)
    assert "\u2705" in message


@pytest.mark.usefixtures("credentials", "service")
def test_status_code_suppressed():
    runner = CliRunner()

    result = runner.invoke(pushover.main, ["hello", "world", "-s", "5", "--supress-exit-code"])
    assert result.exit_code == 0
    assert result.output == ""


@pytest.mark.usefixtures("credentials")
def test_python_api(service):

    pushover.send_message("Foo Message")

    message = get_message_from_body(service.calls[0].request.body)
    assert message == "Foo Message"


@pytest.mark.usefixtures("credentials")
def test_python_api_explicit_credentials(service):

    credentials = pushover.PushoverCredentials("test-user-id-explicit", "test-api-token-explicit")
    pushover.send_message("Foo Message", credentials)

    message = get_message_from_body(service.calls[0].request.body)
    assert message == "Foo Message"
    data = urllib.parse.parse_qs(service.calls[0].request.body)
    assert data["user"] == [credentials.user_id]
    assert data["token"] == [credentials.api_token]
