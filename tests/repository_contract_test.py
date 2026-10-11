from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
COMPONENT = (
    ROOT
    / "custom_components"
    / "home_ai_gateway"
)


def main():
    manifest = json.loads(
        (
            COMPONENT
            / "manifest.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    hacs = json.loads(
        (
            ROOT
            / "hacs.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    assert (
        manifest[
            "domain"
        ]
        ==
        "home_ai_gateway"
    )
    assert (
        manifest[
            "version"
        ]
        ==
        "0.6.2"
    )
    assert (
        manifest[
            "config_flow"
        ]
        is True
    )
    assert (
        manifest[
            "single_config_entry"
        ]
        is True
    )
    assert (
        hacs[
            "name"
        ]
        ==
        "Home AI Gateway"
    )

    required = {
        "__init__.py",
        "config_flow.py",
        "const.py",
        "conversation.py",
        "health.py",
        "manifest.json",
        "protocol.py",
        "strings.json",
    }

    assert required.issubset({
        path.name
        for path in COMPONENT.iterdir()
        if path.is_file()
    })

    assert (
        COMPONENT
        / "translations"
        / "en.json"
    ).exists()

    assert (
        COMPONENT
        / "translations"
        / "hu.json"
    ).exists()

    print(
        "Repository contract tests passed."
    )


if __name__ == "__main__":
    main()
