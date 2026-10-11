"""Pure protocol helpers for Home AI Gateway."""

from __future__ import annotations

from typing import Any


def normalize_gateway_url(
    value: str,
) -> str:
    """Normalize a configured gateway base URL."""

    return value.strip().rstrip("/")


def client_headers(
    token: str,
) -> dict[str, str]:
    """Return authenticated native-client headers."""

    return {
        "Authorization":
            f"Bearer {token}",
        "Content-Type":
            "application/json",
        "X-Client-Id":
            "home-assistant-conversation",
        "X-Client-Type":
            "voice",
        "X-Client-Name":
            "Home Assistant Conversation",
    }


def command_payload(
    text: str,
    conversation_id: str | None,
) -> dict[str, Any]:
    """Build a gateway command request."""

    return {
        "text":
            text,
        "dry_run":
            False,
        "confirmed":
            False,
        "conversation_id":
            conversation_id,
    }


def response_speech(
    payload: dict[str, Any],
) -> str:
    """Extract a safe spoken response from a gateway response."""

    speech = payload.get(
        "speech"
    )

    if isinstance(
        speech,
        str,
    ) and speech.strip():
        return speech.strip()

    if payload.get(
        "ok"
    ) is True:
        return "Rendben."

    return (
        "A Home AI Gateway nem adott "
        "érvényes választ."
    )


def response_needs_follow_up(
    payload: dict[str, Any],
) -> bool:
    """Return whether Home Assistant should keep the conversation open."""

    return bool(
        payload.get(
            "needs_clarification"
        )
        or payload.get(
            "action"
        )
        == "clarification_required"
    )


def sanitized_health(
    payload: Any,
) -> dict[str, Any]:
    """Reduce gateway health data to the public contract."""

    healthy = (
        isinstance(
            payload,
            dict,
        )
        and payload.get(
            "ok"
        )
        is True
    )

    result: dict[str, Any] = {
        "ok":
            healthy,
        "service":
            "home-ai-gateway",
    }

    if isinstance(
        payload,
        dict,
    ):
        version = payload.get(
            "version"
        )

        if isinstance(
            version,
            str,
        ) and version.strip():
            result[
                "version"
            ] = version.strip()

    return result
