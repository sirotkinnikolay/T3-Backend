### 2.1
```sql
SELECT 
    c.name AS client_name,
    COALESCE(SUM(oi.quantity * p.price), 0) AS total_amount
FROM clients c
LEFT JOIN orders o ON c.id = o.client_id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
GROUP BY c.id, c.name
ORDER BY total_amount DESC;
```
### 2.2
```sql
SELECT 
    parent.name AS category_name,
    COUNT(DISTINCT child.child_id) AS direct_children_count
FROM categories parent
LEFT JOIN category_hierarchy child ON parent.id = child.parent_id AND child.depth = 1
GROUP BY parent.id, parent.name
ORDER BY parent.name;
```
### 2.3.1
```sql
CREATE OR REPLACE VIEW top_5_products_last_month AS
SELECT 
    p.name AS product_name,
    (SELECT c1.name 
     FROM categories c1
     JOIN category_hierarchy ch1 ON c1.id = ch1.parent_id
     JOIN product_categories pc1 ON ch1.child_id = pc1.category_id
     WHERE pc1.product_id = p.id AND ch1.depth = 0
     LIMIT 1) AS first_level_category,
    SUM(oi.quantity) AS total_sold_quantity
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
WHERE o.order_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
    AND o.order_date < DATE_TRUNC('month', CURRENT_DATE)
GROUP BY p.id, p.name
ORDER BY total_sold_quantity DESC
LIMIT 5;
```
### 2.3.2
* Индексы: Добавить индексы на order_date, product_id, category_id, ancestor_id, descendant_id.
* Кэширование: Использовать кэширование для результатов популярных запросов.
* Партиционирование: Разделить таблицу orders по датам.
