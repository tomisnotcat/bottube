"""Tests for BoTTube CLI."""
import pytest
from unittest.mock import Mock, patch
from bottube_cli.api import BoTTubeClient


@pytest.fixture
def client():
    with patch("bottube_cli.api.CONFIG_PATH"):
        return BoTTubeClient(api_key="test-key")


def test_client_init(client):
    assert client.api_key == "test-key"


def test_get_videos(client):
    mock_resp = Mock()
    mock_resp.json.return_value = {"videos": [{"title": "Test"}]}
    mock_resp.raise_for_status = Mock()
    with patch.object(client.session, "get", return_value=mock_resp):
        result = client.get_videos()
        assert "videos" in result


def test_upload_dry_run(client):
    result = client.upload_video("test.mp4", "Test", dry_run=True)
    assert result["dry_run"] is True
