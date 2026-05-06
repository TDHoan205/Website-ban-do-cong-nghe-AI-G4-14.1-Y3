"""
Statistics Controller - Thong ke
Tuong duong Controllers/StatisticsController.cs trong C#
"""
from datetime import datetime
import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func

from Data.database import get_db
from Models.Order import Order, OrderItem, OrderStatus
from Models.Product import Product
from Models.Inventory import Inventory
from Services.OrderService import OrderService

router = APIRouter(prefix="/Statistics")


def _parse_date(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid date format") from exc


def _csv_response(filename: str, headers: list, rows: list) -> StreamingResponse:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/Orders")
def order_stats(db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.get_order_stats()


@router.get("/Revenue")
def revenue_stats(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.get_revenue_stats(days)


@router.get("/RevenueRange")
def revenue_range(
    start_date: str = Query(...),
    end_date: str = Query(...),
    export: str = Query("none"),
    db: Session = Depends(get_db)
):
    start = _parse_date(start_date)
    end = _parse_date(end_date)
    if end < start:
        raise HTTPException(status_code=400, detail="End date must be after start date")

    orders = db.query(Order).filter(
        Order.order_date >= start,
        Order.order_date <= end,
        Order.status == OrderStatus.DELIVERED
    ).all()

    total_revenue = sum(float(o.total_amount) for o in orders)
    result = {
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "order_count": len(orders),
        "total_revenue": total_revenue,
    }

    if export == "csv":
        rows = [
            [o.order_id, o.order_date.isoformat() if o.order_date else "", float(o.total_amount), o.status]
            for o in orders
        ]
        return _csv_response("revenue_report.csv", ["order_id", "order_date", "total_amount", "status"], rows)

    if export != "none":
        raise HTTPException(status_code=400, detail="Unsupported export format")

    return result


@router.get("/TopProducts")
def top_products(
    start_date: str = Query(...),
    end_date: str = Query(...),
    limit: int = Query(10, ge=1, le=100),
    export: str = Query("none"),
    db: Session = Depends(get_db)
):
    start = _parse_date(start_date)
    end = _parse_date(end_date)
    if end < start:
        raise HTTPException(status_code=400, detail="End date must be after start date")

    rows = db.query(
        OrderItem.product_id,
        OrderItem.product_name,
        func.sum(OrderItem.quantity).label("total_quantity"),
        func.sum(OrderItem.subtotal).label("total_amount"),
    ).join(Order, Order.order_id == OrderItem.order_id).filter(
        Order.order_date >= start,
        Order.order_date <= end,
        Order.status == OrderStatus.DELIVERED
    ).group_by(OrderItem.product_id, OrderItem.product_name).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(limit).all()

    items = [
        {
            "product_id": r.product_id,
            "product_name": r.product_name,
            "total_quantity": int(r.total_quantity or 0),
            "total_amount": float(r.total_amount or 0),
        }
        for r in rows
    ]

    if export == "csv":
        return _csv_response(
            "top_products.csv",
            ["product_id", "product_name", "total_quantity", "total_amount"],
            [[i["product_id"], i["product_name"], i["total_quantity"], i["total_amount"]] for i in items],
        )
    if export != "none":
        raise HTTPException(status_code=400, detail="Unsupported export format")

    return {
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "items": items,
    }


@router.get("/Inventory")
def inventory_stats(
    low_stock_threshold: int = Query(5, ge=0, le=1000),
    export: str = Query("none"),
    db: Session = Depends(get_db)
):
    rows = db.query(
        Inventory.inventory_id,
        Inventory.product_id,
        Inventory.quantity_in_stock,
        Inventory.min_stock_level,
        Inventory.max_stock_level,
        Product.name.label("product_name"),
    ).join(Product, Product.product_id == Inventory.product_id).all()

    items = [
        {
            "inventory_id": r.inventory_id,
            "product_id": r.product_id,
            "product_name": r.product_name,
            "quantity_in_stock": r.quantity_in_stock,
            "min_stock_level": r.min_stock_level,
            "max_stock_level": r.max_stock_level,
            "is_low_stock": r.quantity_in_stock <= low_stock_threshold,
        }
        for r in rows
    ]

    if export == "csv":
        return _csv_response(
            "inventory_stats.csv",
            ["product_id", "product_name", "quantity_in_stock", "min_stock_level", "max_stock_level"],
            [
                [i["product_id"], i["product_name"], i["quantity_in_stock"], i["min_stock_level"], i["max_stock_level"]]
                for i in items
            ],
        )
    if export != "none":
        raise HTTPException(status_code=400, detail="Unsupported export format")

    return {
        "low_stock_threshold": low_stock_threshold,
        "items": items,
    }
