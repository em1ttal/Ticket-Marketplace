""" Account related CRUD methods """
from typing import Any

from sqlmodel import Session, select

from app.models import Account, AccountCreate, OrderCreate, Match


def get_account(*, session: Session, user_id: int) -> Account:
    account = session.exec(select(Account).where(Account.user_id == user_id)).first()
    return account


def create_account(*, session: Session, account_create: AccountCreate) -> Account:
    db_obj = Account(**account_create.dict())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return db_obj


def update_funds(*, session: Session, order_create: OrderCreate):
    account = session.exec(select(Account).where(Account.id == order_create.account_id)).first()
    match_price = session.exec(select(Match).where(Match.id == order_create.match_id)).first().price
    account.available_money -= match_price * order_create.tickets_bought
    session.commit()
    session.refresh(account)
    return account


def get_user_account(*, session: Session, user_id: int):
    account = session.exec(select(Account).where(Account.user_id == user_id)).first()
    return account
