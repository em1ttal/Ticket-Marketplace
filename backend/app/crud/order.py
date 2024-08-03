""" Order related CRUD methods """
from typing import Any

from sqlmodel import Session, select
from app.models import Order, OrderCreate, Account, Match, User, OrdersOut


def get_orders(*, session: Session, skip: int, limit: int, username: str = None) -> Any:
    if username:
        user = session.exec(select(User).where(User.full_name == username)).first()
        account = session.exec(select(Account).where(Account.user_id == user.id)).first()
        orders = account.orders
    else:
        orders = session.exec(select(Order).offset(skip).limit(limit)).all()

    return orders


def create_order(*, session: Session, order_create: OrderCreate) -> Order:
    order = Order(**order_create.dict())
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def has_funds(*, session: Session, order_create: OrderCreate) -> Any:
    account = session.exec(select(Account).where(Account.id == order_create.account_id)).first()
    match_price = session.exec(select(Match).where(Match.id == order_create.match_id)).first().price
    return account.available_money >= match_price * order_create.tickets_bought


def tickets_left(*, session: Session, order_create: OrderCreate) -> Any:
    match = session.exec(select(Match).where(Match.id == order_create.match_id)).first()
    return match.total_available_tickets >= order_create.tickets_bought
