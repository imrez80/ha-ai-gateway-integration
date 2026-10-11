# Home AI Gateway Integration

Home Assistant custom integration for the **Home AI Gateway** project.

This repository contains the Home Assistant-side conversation agent. The gateway application itself lives in [imrez80/ha-ai-gateway](https://github.com/imrez80/ha-ai-gateway).

## Architecture

```text
Voice PE / Assist
        |
        v
Home Assistant Conversation
        |
        v
custom_components/home_ai_gateway
        |
        | authenticated /command request
        v
Home AI Gateway app
        |
        +--> deterministic router / executor
        +--> constrained semantic fallback
        +--> OpenAI Realtime + Home Assistant MCP
```

The integration also exposes a deliberately minimal public health endpoint for external uptime monitoring:

```text
GET /api/home_ai_gateway/health
```

The endpoint returns only sanitized health information:

```json
{
  "ok": true,
  "service": "home-ai-gateway",
  "version": "0.6.2"
}
```

It does **not** expose credentials, entity mappings, configuration, commands, or Home Assistant state.

## Version

Current integration version: **0.6.2**

For now the integration version follows the Home AI Gateway app version. The repositories may use independent versioning later if their release cadence diverges.

## Installation

### Existing manual installation

The integration domain remains `home_ai_gateway`, so an existing manually installed copy uses the same directory:

```text
/config/custom_components/home_ai_gateway/
```

After the repository version has been copied or installed over that directory, restart Home Assistant Core once.

### HACS

The repository is structured as a HACS custom integration repository.

HACS currently requires GitHub repositories to be **public**. While this repository remains private it is development/source control only and cannot be installed through HACS. Once made public:

1. HACS → three-dot menu → **Custom repositories**
2. Add `https://github.com/imrez80/ha-ai-gateway-integration`
3. Category: **Integration**
4. Download **Home AI Gateway**
5. Restart Home Assistant Core

HACS installs to the same `custom_components/home_ai_gateway` directory, so it can take over an existing manual installation of the same integration after the repository contains the complete working component.

## Configuration

The integration is configured from the Home Assistant UI.

Required values:

- **Gateway URL** — normally the local Home AI Gateway app URL, for example `http://192.168.68.112:8787`
- **Client token** — the gateway client token used by `/auth-check` and `/command`

The config flow validates connectivity and authentication before saving.

## Multi-turn conversations

The Home Assistant conversation id is forwarded to the gateway. Clarification responses keep the conversation open, allowing follow-up answers such as:

- “A konyhai rádiót.”
- “30.”
- “A kert felőlit.”

The gateway remains authoritative for intent validation, sensitive-action confirmation, and execution policy.

## Uptime Kuma

After installing version 0.6.2 and restarting Home Assistant Core, point Uptime Kuma at:

```text
https://<your-nabu-casa-host>/api/home_ai_gateway/health
```

Expected healthy response: HTTP 200 with `"ok": true`.

An unavailable or unhealthy gateway returns HTTP 503 with the same sanitized schema.

## Development

Repository layout:

```text
custom_components/home_ai_gateway/
├── __init__.py
├── config_flow.py
├── const.py
├── conversation.py
├── health.py
├── manifest.json
├── protocol.py
├── strings.json
└── translations/
    ├── en.json
    └── hu.json

tests/
.github/workflows/
```

Pull requests run syntax/contract regression tests. Hassfest is included as a separate validation workflow.

## Security

- The gateway client token is stored in the Home Assistant config entry.
- Browser/API callers do not receive that token.
- The public health endpoint is read-only and intentionally unauthenticated.
- The public health endpoint proxies only the gateway's public `/health` endpoint and sanitizes the result.
- No Home Assistant service execution is exposed through the public health route.

## License

MIT.
