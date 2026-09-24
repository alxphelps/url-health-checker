#!/usr/bin/env python3
import json
import re
import socket
import ssl
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

URLS_FILE = Path(__file__).resolve().parents[1] / "sites" / "urls"
TIMEOUT = 15
HOSTNAME_PATTERN = re.compile(r"^[A-Za-z0-9.-]+$")


def request_status(scheme, hostname, context=None):
    request = Request(f"{scheme}://{hostname}", method="GET")
    started = time.perf_counter()
    try:
        with urlopen(request, context=context, timeout=TIMEOUT) as response:
            status = str(response.status)
    except HTTPError as error:
        status = str(error.code)
    except (OSError, ValueError, ssl.SSLError):
        status = "ERROR"

    response_time = time.perf_counter() - started
    return status, response_time


def certificate_status(hostname):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=TIMEOUT) as connection:
            with context.wrap_socket(connection, server_hostname=hostname) as tls:
                return "PASS", tls.version() or "unknown"
    except (OSError, ValueError, ssl.SSLError):
        return "FAIL", "-"


def read_hostnames():
    return [
        line.strip()
        for line in URLS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def main():
    if not URLS_FILE.is_file():
        print(f"Missing {URLS_FILE}")
        return 1

    results = []
    all_passed = True
    for hostname in read_hostnames():
        if not HOSTNAME_PATTERN.fullmatch(hostname):
            results.append(
                {
                    "endpoint": hostname,
                    "https": {"status": "INVALID", "response_time_ms": None},
                    "http": {"status": "INVALID", "response_time_ms": None},
                    "certificate": {"status": "FAIL", "tls": None},
                }
            )
            all_passed = False
            continue

        certificate, tls_version = certificate_status(hostname)
        https_status, https_time = request_status("https", hostname, ssl.create_default_context())
        http_status, http_time = request_status("http", hostname)
        results.append(
            {
                "endpoint": hostname,
                "https": {
                    "status": https_status,
                    "response_time_ms": round(https_time * 1000),
                },
                "http": {
                    "status": http_status,
                    "response_time_ms": round(http_time * 1000),
                },
                "certificate": {"status": certificate, "tls": tls_version},
            }
        )
        all_passed &= https_status != "ERROR" and http_status != "ERROR" and certificate == "PASS"

    print(json.dumps({"results": results, "overall": "PASS" if all_passed else "FAIL"}, indent=2))
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
