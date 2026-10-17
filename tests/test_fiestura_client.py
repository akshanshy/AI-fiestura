import httpx
from unittest.mock import patch

from app.clients.fiestura_client import check_fiestura_backend


def test_backend_health_success():
    mock_response = httpx.Response(
        200,
        json={"status": "healthy"},
        request=httpx.Request("GET", "http://fiestura.test/health"),
    )

    with patch("app.clients.fiestura_client.httpx.get",
               return_value=mock_response):
        result = check_fiestura_backend("http://fiestura.test")

    assert result == {"status": "healthy"}


def test_backend_connection_error():
    with patch(
        "app.clients.fiestura_client.httpx.get",
        side_effect=httpx.ConnectError("Connection refused"),
    ):
        result = check_fiestura_backend("http://localhost:9999")

    assert result == {
        "error": "Could not connect to Fiestura backend"
    }
def test_backend_timeout():
    with patch(
        "app.clients.fiestura_client.httpx.get",
        side_effect=httpx.TimeoutException("Request timed out"),
    ):
        result = check_fiestura_backend("http://fiestura.test")

    assert result == {
        "error": "Fiestura backend timed out"
    }
    
def test_backend_http_error():
    mock_response = httpx.Response(
        500,
        json={"detail": "Internal server error"},
        request=httpx.Request(
            "GET",
            "http://fiestura.test/health",
        ),
    )

    with patch(
        "app.clients.fiestura_client.httpx.get",
        return_value=mock_response,
    ):
        result = check_fiestura_backend("http://fiestura.test")

    assert result == {
        "error": "Fiestura backend returned an unsuccessful status"
    }
def test_backend_invalid_json():
    mock_response = httpx.Response(
        200,
        content=b"this is not valid JSON",
        request=httpx.Request(
            "GET",
            "http://fiestura.test/health",
        ),
    )

    with patch(
        "app.clients.fiestura_client.httpx.get",
        return_value=mock_response,
    ):
        result = check_fiestura_backend("http://fiestura.test")

    assert result == {
        "error": "Fiestura backend returned invalid JSON"
    }