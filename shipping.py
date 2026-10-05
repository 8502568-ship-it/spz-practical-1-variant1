"""
Shipping module for Practical Lab 5.

Option C baseline defect: credentials are hardcoded in source code.
"""

from urllib.request import Request, urlopen
import json


SHIPPING_API_URL = "https://example.invalid/api/ship"
SHIPPING_USERNAME = "admin"
SHIPPING_PASSWORD = "admin123"


def create_shipping_label(order_id: int, address: str) -> dict:
    """Create a shipping label using the shipping service."""
    payload = json.dumps({
        "order_id": order_id,
        "address": address,
    }).encode("utf-8")

    request = Request(
        SHIPPING_API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    # Intentionally hardcoded credentials for Option C baseline.
    auth = f"{SHIPPING_USERNAME}:{SHIPPING_PASSWORD}".encode("utf-8")
    request.add_header("Authorization", f"Basic {auth.hex()}")

    with urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))
