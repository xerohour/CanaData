import argparse
import json
import subprocess
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple


DEFAULT_HEADERS: List[str] = [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept: application/json, text/plain, */*",
    "Accept-Language: en-US,en;q=0.9",
    "Origin: https://weedmaps.com",
    "Referer: https://weedmaps.com/",
]


ENDPOINTS: List[Tuple[str, str]] = [
    ("listings", "https://api-g.weedmaps.com/discovery/v1/listings?page_size=1&size=1"),
    ("brands", "https://api-g.weedmaps.com/discovery/v1/brands?page_size=1&size=1"),
    ("products", "https://api-g.weedmaps.com/discovery/v1/products?page_size=1&size=1"),
    ("categories", "https://api-g.weedmaps.com/discovery/v1/categories"),
    ("deals", "https://api-g.weedmaps.com/discovery/v1/deals?page_size=1&size=1"),
    ("search", "https://api-g.weedmaps.com/discovery/v1/search?q=flower&page_size=1&size=1"),
    ("tags", "https://api-g.weedmaps.com/discovery/v1/tags?page_size=1&size=1"),
    ("brand_products", "https://api-g.weedmaps.com/discovery/v1/brands/products?page_size=1&size=1"),
]


def run_curl(url: str, timeout_seconds: int = 30) -> Dict[str, Any]:
    cmd = ["curl", "-sS", "-L", "-g"]
    for header in DEFAULT_HEADERS:
        cmd.extend(["-H", header])
    cmd.extend(["-w", "\n__STATUS__:%{http_code}", url])

    result = subprocess.run(cmd, capture_output=True, timeout=timeout_seconds)
    text = (result.stdout or b"").decode("utf-8", "replace")

    if "__STATUS__:" not in text:
        return {
            "status": 0,
            "ok": False,
            "error": "missing_status_marker",
            "raw": text[:500],
        }

    body, status_text = text.rsplit("__STATUS__:", 1)
    body = body.strip()
    status_text = status_text.strip()

    try:
        status = int(status_text)
    except ValueError:
        status = 0

    report: Dict[str, Any] = {
        "status": status,
        "ok": 200 <= status < 300,
        "response_type": "text",
    }

    if not body:
        report["body_empty"] = True
        return report

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        report["raw"] = body[:500]
        return report

    if isinstance(payload, dict):
        report["response_type"] = "json_object"
        report["top_keys"] = list(payload.keys())[:20]

        data = payload.get("data")
        if isinstance(data, dict):
            report["data_type"] = "object"
            report["data_keys"] = list(data.keys())[:20]
        elif isinstance(data, list):
            report["data_type"] = "array"
            report["data_len"] = len(data)

        meta = payload.get("meta")
        if isinstance(meta, dict):
            report["meta_keys"] = list(meta.keys())[:20]

        errors = payload.get("errors")
        if isinstance(errors, list) and errors:
            first_error = errors[0]
            if isinstance(first_error, dict):
                report["error_detail"] = first_error.get("detail")
            else:
                report["error_detail"] = str(first_error)
    elif isinstance(payload, list):
        report["response_type"] = "json_array"
        report["top_level_len"] = len(payload)
        if payload and isinstance(payload[0], dict):
            report["item_keys"] = list(payload[0].keys())[:20]
    else:
        report["response_type"] = type(payload).__name__

    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Probe Weedmaps endpoints and emit JSON health report.")
    parser.add_argument(
        "--output", help="Optional file path to write JSON report")
    parser.add_argument("--timeout", type=int, default=30,
                        help="curl timeout in seconds")
    args = parser.parse_args()

    checks: List[Dict[str, Any]] = []
    for name, url in ENDPOINTS:
        result = run_curl(url, timeout_seconds=args.timeout)
        result["name"] = name
        result["url"] = url
        checks.append(result)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_checks": len(checks),
        "ok_checks": sum(1 for c in checks if c.get("ok")),
        "checks": checks,
    }

    report_json = json.dumps(report, indent=2)
    print(report_json)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as outfile:
            outfile.write(report_json)


if __name__ == "__main__":
    main()
