"""Apply certifi CA bundle for Yahoo Finance / curl SSL on Windows."""
import os


def apply_ssl_cert_bundle() -> None:
    try:
        import certifi

        bundle = certifi.where()
        os.environ.setdefault("SSL_CERT_FILE", bundle)
        os.environ.setdefault("REQUESTS_CA_BUNDLE", bundle)
        os.environ.setdefault("CURL_CA_BUNDLE", bundle)
    except ImportError:
        pass
