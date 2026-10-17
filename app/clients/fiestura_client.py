import httpx


def check_fiestura_backend(base_url: str) -> dict:
    try:
        response = httpx.get(
            f"{base_url}/health",
            timeout=5.0,
        )

        response.raise_for_status()

        return response.json()

    except httpx.TimeoutException:
        return {"error": "Fiestura backend timed out"}

    except httpx.ConnectError:
        return {"error": "Could not connect to Fiestura backend"}

    except httpx.HTTPStatusError:
        return {"error": "Fiestura backend returned an unsuccessful status"}

    except ValueError:
        return {"error": "Fiestura backend returned invalid JSON"}