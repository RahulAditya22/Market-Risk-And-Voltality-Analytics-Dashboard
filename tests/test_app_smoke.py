from __future__ import annotations


def test_streamlit_app_imports_without_network(monkeypatch):
    import market_risk.data_loader as loader

    def fail(*args, **kwargs):
        raise AssertionError("Network access occurred during Streamlit import")

    monkeypatch.setattr(loader.yf, "download", fail)
    import app.streamlit_app  # noqa: F401
