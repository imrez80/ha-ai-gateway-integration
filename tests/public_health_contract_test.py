from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPONENT = (
    ROOT
    / "custom_components"
    / "home_ai_gateway"
)


def main():
    health = (
        COMPONENT
        / "health.py"
    ).read_text(
        encoding="utf-8"
    )

    protocol = (
        COMPONENT
        / "protocol.py"
    ).read_text(
        encoding="utf-8"
    )

    constants = (
        COMPONENT
        / "const.py"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        'PUBLIC_HEALTH_PATH = "/api/home_ai_gateway/health"'
        in constants
    )
    assert (
        "requires_auth = False"
        in health
    )

    forbidden = (
        "CONF_CLIENT_TOKEN",
        "OPENAI_API_KEY",
        "HA_TOKEN",
    )

    for token in forbidden:
        assert token not in health

    assert (
        "sanitized_health"
        in health
    )

    assert (
        '"service":\n            "home-ai-gateway"'
        in protocol
    )

    print(
        "Public health contract tests passed."
    )


if __name__ == "__main__":
    main()
