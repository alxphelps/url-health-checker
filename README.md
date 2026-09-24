# URL Health Checker

This script checks a list of hostnames from the `urls` file and prints the results as JSON.

It does three things for every hostname:

- Tries an HTTPS request and reports the returned HTTP status
- Tries an HTTP request and reports the returned HTTP status
- Opens a secure TLS connection on port 443 and confirms the certificate is valid

It reads the hostnames from `urls`, skips blank lines and comment lines, and includes a final PASS/FAIL summary in the `overall` field.

## Run it

From this directory:

```bash
python endpoint_test.py
```

## Example output

```json
{
	"results": [
		{
			"endpoint": "google.com",
			"https": {
				"status": "200",
				"response_time_ms": 221
			},
			"http": {
				"status": "200",
				"response_time_ms": 202
			},
			"certificate": {
				"status": "PASS",
				"tls": "TLSv1.3"
			}
		}
	],
	"overall": "PASS"
}
```

This is useful for quickly checking whether a site is reachable over HTTP and HTTPS and whether its TLS certificate validates cleanly. Response times are reported as numeric milliseconds.
