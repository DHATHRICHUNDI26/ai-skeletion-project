
from ai_client.config import settings


def test_settings_loaded():
    assert settings.api_base_url == "https://api.example.com"
    assert settings.api_key == "your_actual_api_key"
    assert settings.request_timeout == 10
    assert settings.max_retries == 3
