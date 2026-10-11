"""Home AI Gateway integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .health import HomeAIGatewayHealthView


PLATFORMS: list[Platform] = [
    Platform.CONVERSATION,
]


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up integration-level resources."""

    hass.http.register_view(
        HomeAIGatewayHealthView
    )

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Home AI Gateway from a config entry."""

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a Home AI Gateway config entry."""

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )
