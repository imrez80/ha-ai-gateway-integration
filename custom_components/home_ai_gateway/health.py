"""Public, read-only health endpoint for Home AI Gateway."""

from __future__ import annotations

import asyncio
from http import HTTPStatus

from aiohttp import ClientError, web

from homeassistant.components.http import (
    KEY_HASS,
    HomeAssistantView,
)
from homeassistant.helpers.aiohttp_client import (
    async_get_clientsession,
)

from .const import (
    CONF_GATEWAY_URL,
    DEFAULT_GATEWAY_URL,
    DOMAIN,
    GATEWAY_HEALTH_PATH,
    HEALTH_TIMEOUT_SECONDS,
    PUBLIC_HEALTH_PATH,
)
from .protocol import (
    normalize_gateway_url,
    sanitized_health,
)


class HomeAIGatewayHealthView(
    HomeAssistantView
):
    """Expose a sanitized public gateway health check."""

    url = PUBLIC_HEALTH_PATH
    name = "api:home_ai_gateway:health"
    requires_auth = False

    async def get(
        self,
        request: web.Request,
    ) -> web.Response:
        """Return gateway availability without exposing configuration."""

        hass = request.app[
            KEY_HASS
        ]

        entries = (
            hass.config_entries.async_entries(
                DOMAIN
            )
        )

        if not entries:
            return self.json(
                {
                    "ok": False,
                    "service":
                        "home-ai-gateway",
                },
                status_code=
                    HTTPStatus.SERVICE_UNAVAILABLE,
            )

        entry = entries[0]

        gateway_url = normalize_gateway_url(
            str(
                entry.data.get(
                    CONF_GATEWAY_URL,
                    DEFAULT_GATEWAY_URL,
                )
            )
        )

        session = async_get_clientsession(
            hass
        )

        try:
            async with asyncio.timeout(
                HEALTH_TIMEOUT_SECONDS
            ):
                response = await session.get(
                    gateway_url
                    + GATEWAY_HEALTH_PATH
                )

                if (
                    response.status
                    != HTTPStatus.OK
                ):
                    return self.json(
                        {
                            "ok": False,
                            "service":
                                "home-ai-gateway",
                        },
                        status_code=
                            HTTPStatus.SERVICE_UNAVAILABLE,
                    )

                payload = await response.json(
                    content_type=None
                )

        except (
            TimeoutError,
            ClientError,
            ValueError,
            TypeError,
        ):
            return self.json(
                {
                    "ok": False,
                    "service":
                        "home-ai-gateway",
                },
                status_code=
                    HTTPStatus.SERVICE_UNAVAILABLE,
            )

        result = sanitized_health(
            payload
        )

        return self.json(
            result,
            status_code=(
                HTTPStatus.OK
                if result[
                    "ok"
                ]
                else
                HTTPStatus.SERVICE_UNAVAILABLE
            ),
        )
