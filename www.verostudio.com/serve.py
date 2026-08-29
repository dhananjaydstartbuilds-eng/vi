#!/usr/bin/env python3
"""Local dev server for the mirrored verostudio.com site."""

from __future__ import annotations

import mimetypes
import re
import socket
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

ROOT = Path(__file__).resolve().parent
SITE_ROOT = ROOT / "www.verostudio.com"
CDN_ROOT = ROOT / "cdn.sanity.io"
LIVE_ORIGIN = "https://www.verostudio.com"
SANITY_PROJECT_ID = "xei5vqg0"
SANITY_PROJECT_API = f"https://{SANITY_PROJECT_ID}.api.sanity.io"
CDN_ORIGIN = "https://cdn.sanity.io"
DEFAULT_PORT = 8080
NO_CONTENT_RE = re.compile(r"^No Content:\s+(https?://[^\s]+)", re.IGNORECASE)
LIVE_EVENTS_RE = re.compile(r"/data/live/events/")

API_PROXIES = {
    "/sanity-api": SANITY_PROJECT_API,
    "/api-sanity": "https://api.sanity.io",
}

PATCH_REPLACEMENTS = (
    ("https://xei5vqg0.api.sanity.io", "/sanity-api"),
    ("https://api.sanity.io", "/api-sanity"),
    ('"apiHost":"/api-sanity"', '"apiHost":"/sanity-api"'),
    ("'apiHost':'/api-sanity'", "'apiHost':'/sanity-api'"),
    ("https://cdn.sanity.io", "/sanity-cdn"),
)

PROXY_PATH_PREFIXES = (
    "/webgl/",
    "/fonts/",
    "/favicon",
    "/apple-touch-icon",
    "/site.webmanifest",
)

PATCH_EXTENSIONS = {".html", ".js", ".css", ".mjs", ".json"}

# Legacy Sanity splash media remapped to local synthwave hero assets.
SPLASH_VIDEO_ALIASES = frozenset(
    {
        "/sanity-cdn/files/xei5vqg0/production/bea646a70445ada4b773c2621bc82183bbb837d6.mp4",
        "/sanity-cdn/files/xei5vqg0/production/c4f39f4aedd09681f150b0b8f6a05db6d5c55bcd.mp4",
    }
)
SPLASH_POSTER_ALIAS = (
    "/sanity-cdn/images/xei5vqg0/production/fe9dfb2b06f0b04fa45dc0ebd925dc3b39517dc5-1728x1001.jpg"
)


class SiteHandler(SimpleHTTPRequestHandler):
    site_root = SITE_ROOT
    cdn_root = CDN_ROOT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(self.site_root), **kwargs)

    def log_message(self, format: str, *args) -> None:
        sys.stdout.write("%s - %s\n" % (self.address_string(), format % args))

    def handle_one_request(self) -> None:
        try:
            super().handle_one_request()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_OPTIONS(self) -> None:
        if self._is_api_proxy_path(urlparse(self.path).path):
            self.send_response(204)
            self._send_cors_headers()
            self.end_headers()
            return
        self.send_error(404)

    def do_GET(self) -> None:
        if self._handle_api_proxy("GET"):
            return
        self._handle_request("GET")

    def do_HEAD(self) -> None:
        if self._handle_api_proxy("HEAD"):
            return
        self._handle_request("HEAD")

    def do_POST(self) -> None:
        if self._handle_api_proxy("POST"):
            return
        if self._handle_analytics_noop():
            return
        self.send_error(405, "Method not allowed")

    def _handle_analytics_noop(self) -> bool:
        path = unquote(urlparse(self.path).path)
        if path.startswith("/ingest/") or path.startswith("/_vercel/insights/"):
            length = int(self.headers.get("Content-Length", 0))
            if length:
                self.rfile.read(length)
            self.send_response(204)
            self.end_headers()
            return True
        return False

    def _handle_request(self, method: str) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        query_suffix = f"?{parsed.query}" if parsed.query else ""

        if path.startswith("/sanity/"):
            self._serve_cdn(path[len("/sanity/") :])
            return

        if path in SPLASH_VIDEO_ALIASES:
            self.path = f"/videos/hero-bg.mp4{query_suffix}"
            path = "/videos/hero-bg.mp4"
        elif path == SPLASH_POSTER_ALIAS:
            self.path = f"/videos/hero-bg-poster.jpg{query_suffix}"
            path = "/videos/hero-bg-poster.jpg"

        if path.startswith("/sanity-cdn/"):
            self._serve_cdn(path[len("/sanity-cdn/") :], remote_prefix="/")
            return

        if path in ("", "/"):
            self.path = f"/index.html{query_suffix}"
            path = "/index.html"
        elif path in ("/hero", "/hero/"):
            self.send_response(302)
            self.send_header("Location", f"/{query_suffix}" if query_suffix else "/")
            self.end_headers()
            return
        elif path == "/vero/":
            self.send_response(302)
            self.send_header("Location", f"/vero{query_suffix}")
            self.end_headers()
            return
        elif path == "/vero":
            self.path = f"/vero/index.html{query_suffix}"
            path = "/vero/index.html"
        elif not self._local_path_exists(path):
            html_fallback = f"{path.rstrip('/')}.html"
            if self._local_path_exists(html_fallback):
                self.path = f"{html_fallback}{query_suffix}"
                path = html_fallback

        local_file = Path(self.translate_path(urlparse(self.path).path))
        if local_file.is_file() and local_file.suffix == ".html":
            content = local_file.read_text(encoding="utf-8", errors="ignore")
            match = NO_CONTENT_RE.match(content.strip())
            if match:
                live_url = match.group(1).split("?", 1)[0]
                if self._proxy_live(live_url, head_only=method == "HEAD"):
                    return

        if not local_file.is_file() and path.startswith("/_next/"):
            live_url = urljoin(LIVE_ORIGIN, self.path)
            if self._proxy_live(live_url, head_only=method == "HEAD"):
                return

        if local_file.is_file():
            if local_file.suffix in PATCH_EXTENSIONS:
                body = self._patch_text(local_file.read_text(encoding="utf-8", errors="ignore"))
                if method == "HEAD":
                    self._send_head_only(body, local_file.name)
                else:
                    self._send_text(body, local_file.name)
                return
            if local_file.suffix == ".svg":
                data = local_file.read_bytes()
                if method == "HEAD":
                    self._send_head_only_bytes(data, local_file.name)
                else:
                    self._send_bytes_no_cache(data, local_file.name)
                return
            if method == "HEAD":
                return super().do_HEAD()
            return super().do_GET()

        if any(path.startswith(prefix) for prefix in PROXY_PATH_PREFIXES):
            live_url = urljoin(LIVE_ORIGIN, self.path)
            if self._proxy_live(live_url, head_only=method == "HEAD"):
                return

        live_url = urljoin(LIVE_ORIGIN, path) + query_suffix
        if self._proxy_live(live_url, head_only=method == "HEAD"):
            return

        if not path.endswith(".html"):
            html_url = urljoin(LIVE_ORIGIN, f"{path.rstrip('/')}.html") + query_suffix
            if self._proxy_live(html_url, head_only=method == "HEAD"):
                return

        if method == "HEAD":
            return super().do_HEAD()
        super().do_GET()

    def _is_api_proxy_path(self, path: str) -> bool:
        return any(
            path == prefix or path.startswith(prefix + "/")
            for prefix in API_PROXIES
        )

    def _handle_api_proxy(self, method: str) -> bool:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        target_prefix = None
        target_origin = None
        for prefix, origin in API_PROXIES.items():
            if path == prefix or path.startswith(prefix + "/"):
                target_prefix = prefix
                target_origin = origin
                break

        if not target_origin:
            return False

        suffix = path[len(target_prefix) :]
        target_origin = self._sanity_target_origin(suffix, target_origin)
        target_url = f"{target_origin}{suffix}"
        if parsed.query:
            target_url = f"{target_url}?{parsed.query}"

        if method in ("GET", "HEAD") and LIVE_EVENTS_RE.search(suffix):
            return self._proxy_live_events(target_url, head_only=method == "HEAD")

        body = None
        if method == "POST":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else None

        headers = self._sanity_request_headers()

        try:
            request = urllib.request.Request(
                target_url,
                data=body,
                headers=headers,
                method="GET" if method == "HEAD" else method,
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = response.read()
                upstream_type = response.headers.get(
                    "Content-Type", "application/json"
                )
        except urllib.error.HTTPError as exc:
            payload = exc.read()
            upstream_type = exc.headers.get("Content-Type", "application/json")
            self.send_response(exc.code)
        except Exception as exc:
            self.send_error(502, f"Sanity proxy failed: {exc}")
            return True
        else:
            self.send_response(200)

        self.send_header("Content-Type", upstream_type.split(";")[0])
        if not (method == "HEAD" and not payload):
            self.send_header("Content-Length", str(len(payload)))
        self._send_cors_headers()
        self.end_headers()
        if method != "HEAD":
            try:
                self.wfile.write(payload)
            except (BrokenPipeError, ConnectionResetError):
                pass
        return True

    def _sanity_target_origin(self, suffix: str, origin: str) -> str:
        if origin == "https://api.sanity.io":
            return SANITY_PROJECT_API
        if LIVE_EVENTS_RE.search(suffix):
            return SANITY_PROJECT_API
        return origin

    def _sanity_request_headers(self) -> dict[str, str]:
        headers = {
            "User-Agent": "verostudio-local-mirror/1.0",
            "Accept": self.headers.get("Accept", "*/*"),
            "X-Sanity-Project-ID": SANITY_PROJECT_ID,
        }
        for name in (
            "Content-Type",
            "Authorization",
            "Sanity-Tag",
            "X-Sanity-Dataset",
        ):
            value = self.headers.get(name)
            if value:
                headers[name] = value
        return headers

    def _disable_socket_timeout(self, response) -> None:
        """Idle SSE must not inherit urlopen's 30s read timeout."""
        try:
            response.timeout = None
        except Exception:
            pass
        fp = getattr(response, "fp", None)
        raw = getattr(fp, "raw", None) if fp is not None else None
        sock = getattr(raw, "_sock", None) if raw is not None else None
        if sock is None and fp is not None:
            sock = getattr(fp, "_sock", None)
        if sock is not None:
            try:
                sock.settimeout(None)
            except Exception:
                pass

    def _send_sse_headers(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self._send_cors_headers()
        self.end_headers()

    def _write_sse_keepalives(self) -> None:
        try:
            while True:
                self.wfile.write(b": keepalive\n\n")
                self.wfile.flush()
                time.sleep(15)
        except (BrokenPipeError, ConnectionResetError, TimeoutError, OSError):
            pass

    def _proxy_live_events(self, url: str, head_only: bool = False) -> bool:
        headers = self._sanity_request_headers()
        response = None
        try:
            request = urllib.request.Request(url, headers=headers, method="GET")
            response = urllib.request.urlopen(request, timeout=30)
            self._disable_socket_timeout(response)
        except Exception as exc:
            sys.stdout.write(f"Sanity live fallback to keepalive: {exc}\n")
            if head_only:
                self._send_sse_headers()
                return True
            self._send_sse_headers()
            self._write_sse_keepalives()
            return True

        content_type = response.headers.get("Content-Type", "text/event-stream")
        self.send_response(response.status)
        self.send_header("Content-Type", content_type.split(";")[0])
        self.send_header("Cache-Control", "no-cache")
        self._send_cors_headers()
        self.end_headers()

        if head_only:
            response.close()
            return True

        try:
            while True:
                chunk = response.read(4096)
                if not chunk:
                    break
                self.wfile.write(chunk)
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            return True
        except (TimeoutError, OSError) as exc:
            sys.stdout.write(f"Sanity live stream ended, keepalive: {exc}\n")
        finally:
            try:
                response.close()
            except Exception:
                pass

        self._write_sse_keepalives()
        return True

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, OPTIONS"
        )
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization, Accept",
        )

    def _local_path_exists(self, path: str) -> bool:
        return Path(self.translate_path(path)).exists()

    def _serve_cdn(self, rel_path: str, remote_prefix: str = "") -> None:
        rel_path = rel_path.lstrip("/")
        candidate = self.cdn_root / rel_path

        if not candidate.is_file():
            base = rel_path.split("?", 1)[0]
            stem = Path(base).stem
            parent = self.cdn_root / Path(base).parent
            if parent.is_dir():
                matches = sorted(parent.glob(f"{stem}*"))
                if matches:
                    candidate = matches[0]

        if candidate.is_file():
            self._send_bytes(candidate.read_bytes(), candidate.name)
            return

        live_url = f"{CDN_ORIGIN}{remote_prefix}{rel_path}"
        if self._proxy_live(live_url):
            return

        self.send_error(404, f"CDN asset not found locally: {rel_path}")

    def _proxy_live(self, url: str, head_only: bool = False) -> bool:
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "verostudio-local-mirror/1.0"},
                method="GET",
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                body = response.read()
                content_type = response.headers.get(
                    "Content-Type", "application/octet-stream"
                )
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return False
            self.send_error(exc.code, f"Live proxy failed for {url}")
            return True
        except Exception as exc:
            sys.stdout.write(f"Proxy error for {url}: {exc}\n")
            return False

        if "text/" in content_type or "javascript" in content_type:
            body = self._patch_text(body.decode("utf-8", errors="ignore")).encode(
                "utf-8"
            )

        self.send_response(200)
        self.send_header("Content-Type", content_type.split(";")[0])
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        if not head_only:
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass
        return True

    def _local_origin(self) -> str:
        host = self.headers.get("Host", f"127.0.0.1:{DEFAULT_PORT}")
        return f"http://{host}"

    def _patch_text(self, text: str) -> str:
        for old, new in PATCH_REPLACEMENTS:
            text = text.replace(old, new)

        # Normalize api-sanity -> sanity-api before making URLs absolute.
        text = text.replace('"/api-sanity"', '"/sanity-api"')
        text = text.replace("'/api-sanity'", "'/sanity-api'")
        text = text.replace('\\"/api-sanity\\"', '\\"/sanity-api\\"')
        text = text.replace('apiHost:"/api-sanity"', 'apiHost:"/sanity-api"')
        text = text.replace("apiHost:'/api-sanity'", "apiHost:'/sanity-api'")

        origin = self._local_origin()
        api_host = f"{origin}/sanity-api"

        # Sanity client and PostHog call `new URL()` which requires absolute URLs.
        api_host_patterns = (
            ('"apiHost":"/sanity-api"', f'"apiHost":"{api_host}"'),
            ("'apiHost':'/sanity-api'", f"'apiHost':'{api_host}'"),
            ('\\"apiHost\\":\\"/sanity-api\\"', f'\\"apiHost\\":\\"{api_host}\\"'),
            ('apiHost:"/sanity-api"', f'apiHost:"{api_host}"'),
            ("apiHost:'/sanity-api'", f"apiHost:'{api_host}'"),
            (f'"apiHost":"{origin}/api-sanity"', f'"apiHost":"{api_host}"'),
            (f'\\"apiHost\\":\\"{origin}/api-sanity\\"', f'\\"apiHost\\":\\"{api_host}\\"'),
        )
        for old, new in api_host_patterns:
            text = text.replace(old, new)

        for path in ("/sanity-api", "/ingest", "/sanity-cdn"):
            absolute = f"{origin}{path}"
            text = text.replace(f'"{path}"', f'"{absolute}"')
            text = text.replace(f"'{path}'", f"'{absolute}'")
            text = text.replace(f'\\"{path}\\"', f'\\"{absolute}\\"')

        # Relative /sanity-cdn/images/... URLs break Sanity image ref parsing
        # (only https?:// URLs are converted; bare paths become invalid _ref values).
        cdn_prefix = f"{origin}/sanity-cdn/"
        text = text.replace('"/sanity-cdn/', f'"{cdn_prefix}')
        text = text.replace("'/sanity-cdn/", f"'{cdn_prefix}")
        text = text.replace('\\"/sanity-cdn/', f'\\"{cdn_prefix}')

        text = text.replace('api_host:"/ingest"', f'api_host:"{origin}/ingest"')

        # Project-hostname mode builds invalid URLs when apiHost is localhost.
        text = text.replace('"useProjectHostname":true', '"useProjectHostname":false')
        text = text.replace('\\"useProjectHostname\\":true', '\\"useProjectHostname\\":false')
        text = text.replace("useProjectHostname:!0", "useProjectHostname:!1")

        return text

    def _send_text(self, text: str, filename: str) -> None:
        data = text.encode("utf-8")
        content_type, _ = mimetypes.guess_type(filename)
        content_type = content_type or "text/plain; charset=utf-8"
        if content_type.startswith("text/") and "charset" not in content_type:
            content_type = f"{content_type}; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _send_head_only(self, text: str, filename: str) -> None:
        data = text.encode("utf-8")
        content_type, _ = mimetypes.guess_type(filename)
        content_type = content_type or "text/plain; charset=utf-8"
        if content_type.startswith("text/") and "charset" not in content_type:
            content_type = f"{content_type}; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

    def _send_bytes(self, data: bytes, filename: str) -> None:
        content_type, _ = mimetypes.guess_type(filename)
        content_type = content_type or "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "public, max-age=3600")
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _send_bytes_no_cache(self, data: bytes, filename: str) -> None:
        content_type, _ = mimetypes.guess_type(filename)
        content_type = content_type or "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _send_head_only_bytes(self, data: bytes, filename: str) -> None:
        content_type, _ = mimetypes.guess_type(filename)
        content_type = content_type or "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

    def end_headers(self) -> None:
        super().end_headers()


def patch_html_for_local_api() -> None:
    """Rewrite Sanity API URLs so localhost can reach them through the proxy."""
    for html_path in SITE_ROOT.glob("*.html"):
        original = html_path.read_text(encoding="utf-8")
        if original.startswith("No Content:"):
            continue
        updated = original
        for old, new in PATCH_REPLACEMENTS:
            updated = updated.replace(old, new)
        if updated != original:
            html_path.write_text(updated, encoding="utf-8")
            print(f"Patched API URLs in {html_path.name}")


def port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def find_port(preferred: int) -> int:
    for port in range(preferred, preferred + 20):
        if port_is_free(port):
            return port
    raise RuntimeError(f"No free port found near {preferred}")


def main() -> None:
    if not SITE_ROOT.is_dir():
        print(f"Site folder not found: {SITE_ROOT}")
        sys.exit(1)

    patch_html_for_local_api()

    preferred = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT

    if not port_is_free(preferred):
        print(f"Port {preferred} is already in use.")
        print(f"Stop the old server with Ctrl+C, then run: python3 serve.py {preferred}")
        sys.exit(1)

    handler = partial(SiteHandler)
    server = ThreadingHTTPServer(("127.0.0.1", preferred), handler)

    url = f"http://127.0.0.1:{preferred}/"
    print("=" * 60)
    print("Vero Studio local site")
    print(f"  Site root : {SITE_ROOT}")
    print(f"  CDN mirror: {CDN_ROOT}")
    print(f"  Open      : {url}")
    print(f"  Verostudio: {url}vero")
    print("  Note      : Sanity API is proxied for localhost compatibility")
    print("=" * 60)
    print("Press Ctrl+C to stop the server.")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
