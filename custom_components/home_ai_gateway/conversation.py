"""Conversation agent for Home AI Gateway."""

from __future__ import annotations

import asyncio
from http import HTTPStatus
from typing import Literal

from aiohttp import ClientError

from homeassistant.components import conversation
from homeassistant.components.conversation import (
    AssistantContent,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent
from homeassistant.helpers.aiohttp_client import (
    async_get_clientsession,
)
from homeassistant.helpers.entity_platform import (
    AddConfigEntryEntitiesCallback,
)

from .const import (
    COMMAND_PATH,
    CONF_CLIENT_TOKEN,
    CONF_GATEWAY_URL,
    REQUEST_TIMEOUT_SECONDS,
)
from .protocol import (
    client_headers,
    command_payload,
    normalize_gateway_url,
    response_needs_follow_up,
    response_speech,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Home AI Gateway conversation entity."""

    async_add_entities([
        HomeAIGatewayConversationEntity(
            entry
        )
    ])


class HomeAIGatewayConversationEntity(
    conversation.ConversationEntity,
    conversation.AbstractConversationAgent,
):
    """Bridge Home Assistant Conversation to Home AI Gateway."""

    _attr_has_entity_name = False
    _attr_name = "Home AI Gateway"
    _attr_supported_features = (
        conversation.ConversationEntityFeature.CONTROL
    )

    def __init__(
        self,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the conversation entity."""

        self.entry = entry
        self._attr_unique_id = (
            entry.entry_id
        )

    @property
    def supported_languages(
        self,
    ) -> list[str] | Literal["*"]:
        """Return supported languages."""

        return MATCH_ALL

    async def async_added_to_hass(
        self,
    ) -> None:
        """Register this entity as a conversation agent."""

        await super().async_added_to_hass()

        conversation.async_set_agent(
            self.hass,
            self.entry,
            self,
        )

    async def async_will_remove_from_hass(
        self,
    ) -> None:
        """Unregister the conversation agent."""

        conversation.async_unset_agent(
            self.hass,
            self.entry,
        )

        await super().async_will_remove_from_hass()

    async def _async_handle_message(
        self,
        user_input: conversation.ConversationInput,
        chat_log: conversation.ChatLog,
    ) -> conversation.ConversationResult:
        """Send a conversation turn to Home AI Gateway."""

        gateway_url = normalize_gateway_url(
            self.entry.data[
                CONF_GATEWAY_URL
            ]
        )

        client_token = self.entry.data[
            CONF_CLIENT_TOKEN
        ]

        conversation_id = (
            chat_log.conversation_id
            or user_input.conversation_id
        )

        session = async_get_clientsession(
            self.hass
        )

        payload: dict

        try:
            async with asyncio.timeout(
                REQUEST_TIMEOUT_SECONDS
            ):
                response = await session.post(
                    gateway_url
                    + COMMAND_PATH,
                    headers=
                        client_headers(
                            client_token
                        ),
                    json=
                        command_payload(
                            user_input.text,
                            conversation_id,
                        ),
                )

                payload = await response.json(
                    content_type=None
                )

                if (
                    response.status
                    != HTTPStatus.OK
                ):
                    raise ValueError(
                        "gateway_http_error"
                    )

                if not isinstance(
                    payload,
                    dict,
                ):
                    raise ValueError(
                        "gateway_json_object_required"
                    )

        except (
            TimeoutError,
            ClientError,
            ValueError,
            TypeError,
        ):
            speech = (
                "A Home AI Gateway jelenleg "
                "nem érhető el."
            )

            response = intent.IntentResponse(
                language=
                    user_input.language
            )

            response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                speech,
            )

            return conversation.ConversationResult(
                response=
                    response,
                conversation_id=
                    conversation_id,
                continue_conversation=
                    False,
            )

        speech = response_speech(
            payload
        )

        continue_conversation = (
            response_needs_follow_up(
                payload
            )
        )

        chat_log.async_add_assistant_content_without_tools(
            AssistantContent(
                agent_id=
                    user_input.agent_id,
                content=
                    speech,
            )
        )

        intent_response = intent.IntentResponse(
            language=
                user_input.language
        )

        if payload.get(
            "ok"
        ) is True:
            intent_response.async_set_speech(
                speech
            )

        else:
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                speech,
            )

        return conversation.ConversationResult(
            response=
                intent_response,
            conversation_id=
                conversation_id,
            continue_conversation=
                continue_conversation,
        )
