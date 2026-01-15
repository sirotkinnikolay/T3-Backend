# Order Service

Быстрый запуск

### 1. Клонирование
```
git clone <repository-url>
cd order_service
```

### 2. Запуск
```
docker-compose up --build
```

### 3. Инициализация БД
```
docker-compose exec app python -c "from database import init_db; init_db()"
```

# API
Добавить товар в заказ
```
curl -X POST "http://localhost:8000/orders/1/items" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```
Параметры:

    order_id - ID заказа (в пути)
    product_id - ID товара
    quantity - Количество

Особенности:

    Если товар уже в заказе - увеличивается количество
    Проверяется наличие на складе
    Возвращает ошибку при недостатке товара

Проверка здоровья
```
curl http://localhost:8000/health
```

Технологии

    FastAPI (Python)
    PostgreSQL
    SQLAlchemy
    Docker
