# URL Health Checker

This script checks a list of hostnames from the `urls` file and prints a simple table showing the result of each check.

It does three things for every hostname:

- Tries an HTTPS request and reports the returned HTTP status
- Tries an HTTP request and reports the returned HTTP status
- Opens a secure TLS connection on port 443 and confirms the certificate is valid

It reads the hostnames from `urls`, skips blank lines and comment lines, and prints a final PASS/FAIL summary.

## Run it

From this directory:

```bash
python endpoint_test.py
```

## Example output

```text
Endpoint    | HTTPS | HTTP | Certificate | TLS
------------+-------+------+-------------+--------
google.com  | 200   | 200  | PASS        | TLSv1.3
yahoo.com   | 429   | 429  | PASS        | TLSv1.3
youtube.com | 200   | 200  | PASS        | TLSv1.3

Overall: PASS
```

This is useful for quickly checking whether a site is reachable over HTTP and HTTPS and whether its TLS certificate validates cleanly.
