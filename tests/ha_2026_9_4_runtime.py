"""Source compatibility probe for Home Assistant Core 2026.9.4.

The CI job checks out the exact Home Assistant Core 2026.9.4 tag beside this
repository and this script verifies the API surfaces used by the integration.
This avoids depending on PyPI publication timing for Home Assistant releases.
"""

from __future__ import annotations

import ast
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


def module_symbols(source: str) -> set[str]:
    tree = ast.parse(source)
    names: set[str] = set()

    for node in tree.body:
        if isinstance(
            node,
            (
                ast.ClassDef,
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            names.add(
                node.name
            )

    return names


def class_methods(
    source: str,
    class_name: str,
) -> set[str]:
    tree = ast.parse(source)

    for node in tree.body:
        if (
            isinstance(
                node,
                ast.ClassDef,
            )
            and node.name
            == class_name
        ):
            return {
                item.name
                for item in node.body
                if isinstance(
                    item,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                    ),
                )
            }

    raise AssertionError(
        f"Class not found: {class_name}"
    )


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

    for symbol in (
        "ConversationEntity",
        "AbstractConversationAgent",
        "ConversationEntityFeature",
        "ConversationInput",
        "ConversationResult",
        "ChatLog",
        "AssistantContent",
        "async_set_agent",
        "async_unset_agent",
    ):
        assert symbol in conversation_init, symbol

    assert (
        "_async_handle_message"
        in class_methods(
            conversation_entity,
            "ConversationEntity",
        )
    )

    result_source = conversation_models
    assert "continue_conversation" in result_source
    assert "conversation_id" in result_source

    chat_methods = class_methods(
        conversation_chat_log,
        "ChatLog",
    )
    assert (
        "async_add_assistant_content_without_tools"
        in chat_methods
    )

    config_flow_methods = class_methods(
        config_entries,
        "ConfigFlow",
    )
    assert (
        "async_update_reload_and_abort"
        in config_flow_methods
    )

    assert "HomeAssistantView" in http_init
    assert "KEY_HASS" in http_init
    assert (
        "AddConfigEntryEntitiesCallback"
        in entity_platform
    )

    print(
        "Home Assistant Core 2026.9.4 source compatibility probe passed."
    )


if __name__ == "__main__":
    main()
