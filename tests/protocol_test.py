from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPONENT = (
    ROOT
    / "custom_components"
    / "home_ai_gateway"
)

sys.path.insert(
    0,
    str(
        COMPONENT
    ),
)

from protocol import (
    client_headers,
    command_payload,
    normalize_gateway_url,
    response_needs_follow_up,
    response_speech,
    sanitized_health,
)


def main():
    assert (
        normalize_gateway_url(
            " http://host:8787/ "
        )
        ==
        "http://host:8787"
    )

    headers = client_headers(
        "secret"
    )
    assert (
        headers[
            "Authorization"
        ]
        ==
        "Bearer secret"
    )
    assert (
        headers[
            "X-Client-Id"
        ]
        ==
        "home-assistant-conversation"
    )

    request = command_payload(
        "Kapcsold ki a rádiót.",
        "conversation-1",
    )
    assert request == {
        "text":
            "Kapcsold ki a rádiót.",
        "dry_run":
            False,
        "confirmed":
            False,
        "conversation_id":
            "conversation-1",
    }

    assert response_speech({
        "ok": True,
        "speech":
            "Rendben.",
    }) == "Rendben."

    assert response_needs_follow_up({
        "needs_clarification":
            True,
    }) is True

    assert response_needs_follow_up({
        "action":
            "clarification_required",
    }) is True

    assert response_needs_follow_up({
        "action":
            "executed",
    }) is False

    health = sanitized_health({
        "ok": True,
        "service":
            "home-ai-gateway",
        "version":
            "0.6.2",
        "mapping": {
            "must_not":
                "leak"
        },
        "endpoints": [
            "/command"
        ],
    })

    assert health == {
        "ok":
            True,
        "service":
            "home-ai-gateway",
        "version":
            "0.6.2",
    }

    print(
        "Protocol regression tests passed."
    )


if __name__ == "__main__":
    main()
