from src.extract import fetch_klines


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_fetch_klines_returns_api_payload(monkeypatch):
    expected = [[1, "10", "11", "9", "10.5", "100", 2]]
    calls = {}

    def fake_get(url, params, timeout):
        calls.update(url=url, params=params, timeout=timeout)
        return FakeResponse(expected)

    monkeypatch.setattr("src.extract.session.get", fake_get)

    result = fetch_klines("BTCUSDT", interval="1m", limit=1)

    assert result == expected
    assert calls["params"] == {"symbol": "BTCUSDT", "interval": "1m", "limit": 1}
    assert calls["timeout"] == 10
