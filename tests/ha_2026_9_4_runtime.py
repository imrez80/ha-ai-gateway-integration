"""Source compatibility probe for Home Assistant Core 2026.9.4.

The CI job checks out the exact Home Assistant Core 2026.9.4 tag beside this
repository and verifies the API surfaces used by the integration. The probe is
intentionally source-based: Home Assistant Core may target a newer Python
syntax than the generic GitHub runner used for these lightweight checks.
"""

from __future__ import annotations

import os
from pathlib import Path


HA_CORE = Path(
    os.environ.get(
        "HA_CORE_PATH",
        "ha-core",
    )
).resolve()


def read(relative: str) -> str:
    path = HA_CORE / relative
    assert path.exists(), path
    return path.read_text(
        encoding="utf-8"
    )


def require(
    source: str,
    *needles: str,
) -> None:
    for needle in needles:
        assert needle in source, needle


def main() -> None:
    conversation_init = read(
        "homeassistant/components/conversation/__init__.py"
    )
    conversation_entity = read(
        "homeassistant/components/conversation/entity.py"
    )
    conversation_models = read(
        "homeassistant/components/conversation/models.py"
    )
    conversation_chat_log = read(
        "homeassistant/components/conversation/chat_log.py"
    )
    config_entries = read(
        "homeassistant/config_entries.py"
    )
    http_init = read(
        "homeassistant/components/http/__init__.py"
    )
    entity_platform = read(
        "homeassistant/helpers/entity_platform.py"
    )
    aiohttp_client = read(
        "homeassistant/helpers/aiohttp_client.py"
    )

    require(
        conversation_init,
        "ConversationEntity",
        "AbstractConversationAgent",
        "ConversationEntityFeature",
        "ConversationInput",
        "ConversationResult",
        "ChatLog",
        "AssistantContent",
        "async_set_agent",
        "async_unset_agent",
    )

    require(
        conversation_entity,
        "class ConversationEntity",
        "async def _async_handle_message",
    )

    require(
        conversation_models,
        "class ConversationInput",
        "class ConversationResult",
        "conversation_id:",
        "continue_conversation:",
    )

    require(
        conversation_chat_log,
        "class AssistantContent",
        "class ChatLog",
        "def async_add_assistant_content_without_tools",
    )

    require(
        config_entries,
        "class ConfigFlow",
        "def async_update_reload_and_abort",
    )

    require(
        http_init,
        "KEY_HASS",
        "HomeAssistantView",
    )

    require(
        entity_platform,
        "class AddConfigEntryEntitiesCallback",
    )

    require(
        aiohttp_client,
        "def async_get_clientsession",
    )

    print(
        "Home Assistant Core 2026.9.4 source compatibility probe passed."
    )


if __name__ == "__main__":
    main()
