# Практична робота №5 — Виправлення технічних проблем та верифікація змін

## Обраний дефект

Обрано варіант A — SQL Injection у `inventory.py`.

У функції `get_product_by_id` SQL-запит формувався через f-string:

`WHERE id = {product_id}`

Тому значення `product_id` могло інтерпретуватися як SQL-код.

## Виконане виправлення

Запит замінено на параметризований:

`SELECT id, name, quantity FROM products WHERE id = ?`

Значення передається окремим параметром:

`connection.execute(query, (product_id,))`

Це відокремлює дані від SQL-коду та усуває можливість SQL injection через цей параметр.

## Регресійний тест

Додано `tests/test_inventory_fix.py`.

Тест перевіряє:
1. коректне отримання товару за звичайним ID;
2. що значення `1 OR 1=1` не виконується як SQL-умова і не повертає всі товари.

## Git

Створено гілку:

`fix/CR-001-sql-injection`

Коміти:
- `fix(inventory): parameterize product lookup query`
- `test(inventory): add SQL injection regression test`

## Висновок

Джерело SQL injection у `get_product_by_id` усунуто шляхом використання параметризованого SQL-запиту. Додано регресійні тести, які фіксують очікувану безпечну поведінку та захищають виправлення від повторного внесення дефекту.
