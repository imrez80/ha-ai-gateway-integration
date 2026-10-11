from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONVERSATION = (
    ROOT
    / "custom_components"
    / "home_ai_gateway"
    / "conversation.py"
).read_text(
    encoding="utf-8"
)


def main():
    assert (
        "chat_log.conversation_id"
        in CONVERSATION
    )
    assert (
        "command_payload("
        in CONVERSATION
    )
    assert (
        "response_needs_follow_up("
        in CONVERSATION
    )
    assert (
        "continue_conversation="
        in CONVERSATION
    )
    assert (
        "conversation.async_set_agent("
        in CONVERSATION
    )
    assert (
        "conversation.async_unset_agent("
        in CONVERSATION
    )

    print(
        "Conversation contract tests passed."
    )


if __name__ == "__main__":
    main()
