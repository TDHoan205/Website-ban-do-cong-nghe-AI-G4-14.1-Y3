"""
Employees Controller - Quan ly nhan vien
Tuong duong Controllers/EmployeesController.cs trong C#
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from Data.database import get_db
from Models.Account import Account, Employee

router = APIRouter(prefix="/Employees")


def _require_admin(db: Session, actor_account_id: Optional[int]) -> None:
    if actor_account_id is None:
        raise HTTPException(status_code=401, detail="Actor account is required")
    actor = db.query(Account).filter(Account.account_id == actor_account_id).first()
    if not actor or not actor.role or actor.role.role_name != "Admin":
        raise HTTPException(status_code=403, detail="Admin permission required")


class EmployeeCreate(BaseModel):
    account_id: int
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[int] = None


class EmployeeUpdate(BaseModel):
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[int] = None
    is_active: Optional[bool] = None


def _employee_to_dict(e: Employee) -> dict:
    return {
        "employee_id": e.employee_id,
        "account_id": e.account_id,
        "department": e.department,
        "position": e.position,
        "salary": e.salary,
        "is_active": e.is_active,
    }


@router.get("")
def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Employee)
    total = query.count()
    items = query.order_by(Employee.employee_id).offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": [_employee_to_dict(e) for e in items],
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@router.get("/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return _employee_to_dict(employee)


@router.post("")
def create_employee(
    payload: EmployeeCreate,
    actor_account_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    _require_admin(db, actor_account_id)
    account = db.query(Account).filter(Account.account_id == payload.account_id).first()
    if not account:
        raise HTTPException(status_code=400, detail="Account not found")
    exists = db.query(Employee).filter(Employee.account_id == payload.account_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Employee already exists for account")
    employee = Employee(**payload.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return _employee_to_dict(employee)


@router.put("/{employee_id}")
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    actor_account_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    _require_admin(db, actor_account_id)
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return _employee_to_dict(employee)


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    actor_account_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    _require_admin(db, actor_account_id)
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"success": True}
