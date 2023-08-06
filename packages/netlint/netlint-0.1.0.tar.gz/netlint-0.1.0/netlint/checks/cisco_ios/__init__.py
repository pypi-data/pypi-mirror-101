"""Checks for the Cisco IOS NOS."""

import typing

from ciscoconfparse import CiscoConfParse

from netlint.checks.checker import CheckResult, Checker

__all__ = [
    "check_plaintext_passwords",
    "check_console_password",
    "check_ip_http_server",
]


@Checker.register(apply_to=["cisco_ios"], name="IOS101")
def check_plaintext_passwords(config: typing.List[str]) -> typing.Optional[CheckResult]:
    """Check if there are any plaintext passwords in the configuration."""
    parsed_config = CiscoConfParse(config)
    lines = parsed_config.find_lines("^username.*password")
    if lines:
        return CheckResult(
            text="Plaintext user passwords in configuration.", lines=lines
        )
    else:
        return None


@Checker.register(apply_to=["cisco_ios"], name="IOS102")
def check_ip_http_server(config: typing.List[str]) -> typing.Optional[CheckResult]:
    """Check if the http server is enabled."""
    parsed_config = CiscoConfParse(config)
    lines = parsed_config.find_lines("^ip http")
    if lines:
        return CheckResult(text="HTTP server not disabled.", lines=lines)
    else:
        return None


@Checker.register(apply_to=["cisco_ios"], name="IOS103")
def check_console_password(config: typing.List[str]) -> typing.Optional[CheckResult]:
    """Check for authentication on the console line."""
    parsed_config = CiscoConfParse(config)
    line_con_config = parsed_config.find_all_children("^line con 0")
    if len(line_con_config) == 0:
        return None  # TODO: Log this?

    login = False
    password = False
    for line in line_con_config:
        if "login" in line:
            login = True
        if "password" in line:
            password = True

    if not login or not password:
        return CheckResult(text="Console line unauthenticated.", lines=line_con_config)
    else:
        return None
