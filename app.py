from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import update, select, and_
import logging

from database import get_db, Product, Order, OrderItem

app = FastAPI(title="Order Service API", version="1.0.0")
logger = logging.getLogger(__name__)


class AddItemRequest(BaseModel):
    product_id: int
    quantity: int


class AddItemResponse(BaseModel):
    success: bool
    message: str
    order_id: int
    product_id: int
    total_quantity: int


@app.post("/orders/{order_id}/items", response_model=AddItemResponse)
async def add_product_to_order(
        order_id: int,
        item: AddItemRequest,
        db: Session = Depends(get_db)
):
    """
    Добавляет товар в заказ.

    - Если товар уже есть в заказе, его количество увеличивается
    - Если товара нет в наличии, возвращается ошибка
    """

    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")

        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден")

        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно товара на складе. Доступно: {product.quantity}"
            )

        existing_item = db.query(OrderItem).filter(
            and_(
                OrderItem.order_id == order_id,
                OrderItem.product_id == item.product_id
            )
        ).first()

        if existing_item:
            existing_item.quantity += item.quantity
            total_quantity = existing_item.quantity
        else:
            new_item = OrderItem(
                order_id=order_id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(new_item)
            total_quantity = item.quantity

        product.quantity -= item.quantity
        db.commit()

        return AddItemResponse(
            success=True,
            message="Товар успешно добавлен в заказ",
            order_id=order_id,
            product_id=item.product_id,
            total_quantity=total_quantity
        )

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при добавлении товара в заказ: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)