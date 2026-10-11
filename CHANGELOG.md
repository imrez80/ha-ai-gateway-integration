# Changelog

## 0.6.2

### Added

- Initial standalone repository for the Home AI Gateway Home Assistant integration
- Conversation agent bridge to the Home AI Gateway `/command` API
- Home Assistant conversation-id forwarding for multi-turn clarification
- UI config flow with gateway authentication validation
- Reconfigure flow
- Public read-only health endpoint for Uptime Kuma:
  - `/api/home_ai_gateway/health`
  - no Home Assistant authentication required
  - sanitized `ok`, `service`, and optional `version` only
- HACS repository metadata
- English and Hungarian UI translations
- Regression/contract tests
- GitHub Actions syntax and contract test workflow
- Hassfest workflow

### Security

- Client token is never returned by the public health endpoint
- Public health does not expose entity mappings, configuration, command APIs, or Home Assistant state
- Gateway command requests remain authenticated with the configured client token

### Compatibility

- Home Assistant minimum version declared for HACS: 2026.10.0
- Integration version follows Home AI Gateway app version for now
- Installing or updating the custom integration requires one Home Assistant Core restart
