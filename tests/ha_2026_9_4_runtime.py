"""Runtime compatibility probe for Home Assistant 2026.9.4.

This file is intentionally not named *_test.py because the ordinary contract
suite runs without Home Assistant installed. The dedicated CI compatibility
job installs exactly Home Assistant 2026.9.4 and executes this probe.
"""

from __future__ import annotations

import importlib
import inspect

from homeassistant import config_entries
from homeassistant.components import conversation
from homeassistant.components.conversation import AssistantContent
from homeassistant.components.http import KEY_HASS, HomeAssistantView
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback


def main() -> None:
    """Verify every Home Assistant API surface used by the integration."""

    assert conversation.ConversationEntity is not None
    assert conversation.AbstractConversationAgent is not None
    assert conversation.ConversationEntityFeature is not None
    assert conversation.ChatLog is not None
    assert conversation.ConversationInput is not None
    assert conversation.ConversationResult is not None

    assert hasattr(
        conversation,
        "async_set_agent",
    )
    assert hasattr(
        conversation,
        "async_unset_agent",
    )
    assert hasattr(
        conversation.ChatLog,
        "async_add_assistant_content_without_tools",
    )

    result_parameters = inspect.signature(
        conversation.ConversationResult
    ).parameters
    assert "continue_conversation" in result_parameters
    assert "conversation_id" in result_parameters

    assistant_parameters = inspect.signature(
        AssistantContent
    ).parameters
    assert "agent_id" in assistant_parameters
    assert "content" in assistant_parameters

    assert HomeAssistantView is not None
    assert KEY_HASS is not None
    assert async_get_clientsession is not None
    assert AddConfigEntryEntitiesCallback is not None

    assert hasattr(
        config_entries.ConfigFlow,
        "async_update_reload_and_abort",
    )

    for module_name in (
        "custom_components.home_ai_gateway",
        "custom_components.home_ai_gateway.config_flow",
        "custom_components.home_ai_gateway.conversation",
        "custom_components.home_ai_gateway.health",
        "custom_components.home_ai_gateway.protocol",
    ):
        importlib.import_module(
            module_name
        )

    print(
        "Home Assistant 2026.9.4 runtime compatibility probe passed."
    )


if __name__ == "__main__":
    main()
