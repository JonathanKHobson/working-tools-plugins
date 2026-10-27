"""Public-source fetch boundary for the adapted audio-course scraper."""
import ipaddress
import os
import socket
import urllib.error
import urllib.parse
import urllib.request

MAX_BYTES = 5 * 1024 * 1024


def validate_url(url):
    parts = urllib.parse.urlsplit(url)
    allowed = {h.strip().lower() for h in os.environ.get("AUDIO_LESSON_ALLOWED_HOSTS", "").split(",") if h.strip()}
    if parts.scheme != "https" or parts.username or parts.password or parts.port not in (None, 443):
        raise ValueError("Only public HTTPS URLs without credentials are permitted")
    host = (parts.hostname or "").lower()
    if host not in allowed:
        raise ValueError("Source host is outside the explicit allowlist")
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(x[4][0]).is_global for x in addresses):
        raise ValueError("Source resolves to a nonpublic address")
    return url


class PublicRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_public(url, headers):
    validate_url(url)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), PublicRedirect())
    with opener.open(urllib.request.Request(url, headers=headers), timeout=30) as response:
        validate_url(response.url)
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Source exceeds the 5 MiB fetch limit")
    return data
