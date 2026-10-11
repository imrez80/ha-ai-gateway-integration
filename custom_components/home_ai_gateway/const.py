"""Constants for Home AI Gateway."""

DOMAIN = "home_ai_gateway"

CONF_GATEWAY_URL = "gateway_url"
CONF_CLIENT_TOKEN = "client_token"

DEFAULT_GATEWAY_URL = "http://192.168.68.112:8787"

AUTH_CHECK_PATH = "/auth-check"
COMMAND_PATH = "/command"
PUBLIC_HEALTH_PATH = "/api/home_ai_gateway/health"
GATEWAY_HEALTH_PATH = "/health"

CLIENT_ID = "home-assistant-conversation"
CLIENT_TYPE = "voice"
CLIENT_NAME = "Home Assistant Conversation"

REQUEST_TIMEOUT_SECONDS = 60
HEALTH_TIMEOUT_SECONDS = 5
