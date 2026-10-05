import sqlite3

from inventory import get_product_by_id


def create_database(path):
    connection = sqlite3.connect(path)
    connection.execute(
        "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER)"
    )
    connection.executemany(
        "INSERT INTO products VALUES (?, ?, ?)",
        [(1, "Widget", 10), (2, "Tool", 20)],
    )
    connection.commit()
    connection.close()


def test_get_product_by_id_returns_product_for_valid_id(tmp_path):
    db_path = tmp_path / "inventory.db"
    create_database(db_path)

    assert get_product_by_id("1", str(db_path)) == {
        "id": 1,
        "name": "Widget",
        "quantity": 10,
    }


def test_get_product_by_id_rejects_sql_injection(tmp_path):
    db_path = tmp_path / "inventory.db"
    create_database(db_path)

    assert get_product_by_id("1 OR 1=1", str(db_path)) is None
