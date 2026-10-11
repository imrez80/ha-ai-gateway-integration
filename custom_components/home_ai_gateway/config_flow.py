"""Config flow for Home AI Gateway."""

from __future__ import annotations

import asyncio
from http import HTTPStatus
from typing import Any

from aiohttp import ClientError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import (
    async_get_clientsession,
)

from .const import (
    AUTH_CHECK_PATH,
    CONF_CLIENT_TOKEN,
    CONF_GATEWAY_URL,
    DEFAULT_GATEWAY_URL,
    DOMAIN,
    HEALTH_TIMEOUT_SECONDS,
)
from .protocol import (
    client_headers,
    normalize_gateway_url,
)


class CannotConnect(Exception):
    """Raised when the gateway cannot be reached."""


class InvalidAuth(Exception):
    """Raised when the gateway rejects the client token."""


async def async_validate_gateway(
    hass: HomeAssistant,
    gateway_url: str,
    client_token: str,
) -> None:
    """Validate gateway reachability and client authentication."""

    url = (
        normalize_gateway_url(
            gateway_url
        )
        + AUTH_CHECK_PATH
    )

    session = async_get_clientsession(
        hass
    )

    try:
        async with asyncio.timeout(
            HEALTH_TIMEOUT_SECONDS
        ):
            response = await session.get(
                url,
                headers=
                    client_headers(
                        client_token
                    ),
            )

            if (
                response.status
                == HTTPStatus.UNAUTHORIZED
            ):
                raise InvalidAuth

            if (
                response.status
                != HTTPStatus.OK
            ):
                raise CannotConnect

            payload = await response.json(
                content_type=None
            )

    except InvalidAuth:
        raise

    except (
        TimeoutError,
        ClientError,
        ValueError,
        TypeError,
    ) as err:
        raise CannotConnect from err

    if not isinstance(
        payload,
        dict,
    ):
        raise CannotConnect

    if (
        payload.get(
            "ok"
        )
        is not True
        or payload.get(
            "authenticated"
        )
        is not True
    ):
        raise InvalidAuth


def _schema(
    defaults: dict[str, Any],
) -> vol.Schema:
    """Return the configuration schema."""

    return vol.Schema({
        vol.Required(
            CONF_GATEWAY_URL,
            default=defaults.get(
                CONF_GATEWAY_URL,
                DEFAULT_GATEWAY_URL,
            ),
        ):
            str,

        vol.Required(
            CONF_CLIENT_TOKEN,
            default=defaults.get(
                CONF_CLIENT_TOKEN,
                "",
            ),
        ):
            str,
    })


class HomeAIGatewayConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow for Home AI Gateway."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle initial setup."""

        errors: dict[str, str] = {}

        if user_input is not None:
            gateway_url = normalize_gateway_url(
                user_input[
                    CONF_GATEWAY_URL
                ]
            )
            client_token = user_input[
                CONF_CLIENT_TOKEN
            ].strip()

            try:
                await async_validate_gateway(
                    self.hass,
                    gateway_url,
                    client_token,
                )

            except InvalidAuth:
                errors[
                    "base"
                ] = "invalid_auth"

            except CannotConnect:
                errors[
                    "base"
                ] = "cannot_connect"

            except Exception:
                errors[
                    "base"
                ] = "unknown"

            else:
                await self.async_set_unique_id(
                    DOMAIN
                )
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=
                        "Home AI Gateway",
                    data={
                        CONF_GATEWAY_URL:
                            gateway_url,
                        CONF_CLIENT_TOKEN:
                            client_token,
                    },
                )

        return self.async_show_form(
            step_id=
                "user",
            data_schema=
                _schema(
                    user_input
                    or {}
                ),
            errors=
                errors,
        )

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Reconfigure an existing entry."""

        entry = (
            self._get_reconfigure_entry()
        )

        errors: dict[str, str] = {}

        if user_input is not None:
            gateway_url = normalize_gateway_url(
                user_input[
                    CONF_GATEWAY_URL
                ]
            )
            client_token = user_input[
                CONF_CLIENT_TOKEN
            ].strip()

            try:
                await async_validate_gateway(
                    self.hass,
                    gateway_url,
                    client_token,
                )

            except InvalidAuth:
                errors[
                    "base"
                ] = "invalid_auth"

            except CannotConnect:
                errors[
                    "base"
                ] = "cannot_connect"

            except Exception:
                errors[
                    "base"
                ] = "unknown"

            else:
                return self.async_update_reload_and_abort(
                    entry,
                    data={
                        CONF_GATEWAY_URL:
                            gateway_url,
                        CONF_CLIENT_TOKEN:
                            client_token,
                    },
                )

        return self.async_show_form(
            step_id=
                "reconfigure",
            data_schema=
                _schema(
                    user_input
                    or dict(
                        entry.data
                    )
                ),
            errors=
                errors,
        )
