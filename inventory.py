"""Inventory module for Practical Lab 5."""

import sqlite3
from typing import Any


def get_product_by_id(product_id: str, db_path: str = "inventory.db") -> dict[str, Any] | None:
    """Return a product by ID."""
    connection = sqlite3.connect(db_path)
    try:
        query = "SELECT id, name, quantity FROM products WHERE id = ?"
        row = connection.execute(query, (product_id,)).fetchone()
        if row is None:
            return None
        return {"id": row[0], "name": row[1], "quantity": row[2]}
    finally:
        connection.close()


def list_products(db_path: str = "inventory.db") -> list[dict[str, Any]]:
    """Return all products."""
    connection = sqlite3.connect(db_path)
    try:
        rows = connection.execute(
            "SELECT id, name, quantity FROM products ORDER BY id"
        ).fetchall()
        return [
            {"id": row[0], "name": row[1], "quantity": row[2]}
            for row in rows
        ]
    finally:
        connection.close()
