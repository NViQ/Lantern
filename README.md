### Задание 1. Фонарь

[lantern.py](Lantern/lantern.py) 
[test.py](Lantern/test.py)


### Запуск программы:
```python
import asyncio
from lantern.lantern import main
asyncio.run(main())
```

### Задание 2. Проектирование БД.
Схема БД:

<img src=./"TZ_DB.png"></details>

### SQL запросы:
1) Получение информации о сумме товаров заказанных под каждого клиента (Наименование клиента, сумма)
```sql
SELECT 
    clients.name as client_name,
    SUM(order_numencl.amount * nomenclature.price) as sum
FROM
    orders
JOIN order_numencl ON orders.id = order_nomencl.order_id
JOIN nomenclature ON order_nomencl.nomenc_id = nomenclature.id
JOIN clients ON orders.client_id = clients.id
GROUP BY clients.name
```
2) Найти количество дочерних элементов первого уровня вложенности для категорий номенклатуры.
```sql
SELECT 
    lvl1.name,
    (SELECT COUNT(*)
     FROM categories lvl2
     WHERE parent_id = lvl1.id) as children_amount
FROM categories as lvl1
```
