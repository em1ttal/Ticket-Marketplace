""" Order management routes """

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import col, delete, func, select
from typing import List
from app import crud
from app.api.deps import SessionDep, get_current_active_superuser, get_current_user
from app.models import (Account, Message, AccountOut,
                        AccountCreate, OrderOut,
                        OrderCreate, OrdersOut, User, Match)

router = APIRouter()


# get orders of a person
@router.get('/{username}',
            dependencies=[Depends(get_current_user)],
            response_model=OrdersOut)
async def get_order(session: SessionDep, username: str, skip: int = 0, limit: int = 100):
    user = session.exec(select(User).where(User.full_name == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    orders = crud.order.get_orders(session=session, skip=skip, limit=limit, username=username)
    order_out_list = []
    for order in orders:
        order_out = OrderOut(
            id=order.id,
            tickets_bought=order.tickets_bought,
            match_id=order.match_id,
            account_id=order.account_id,
            user_name=user.full_name
        )
        order_out_list.append(order_out)

    return OrdersOut(data=order_out_list, count=len(order_out_list))


# create order
@router.post('/{username}',
             dependencies=[Depends(get_current_user)],
             response_model=OrderOut)
async def create_order(session: SessionDep, order_in: OrderCreate):
    match = session.exec(select(Match).where(Match.id == order_in.match_id)).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    account = session.exec(select(Account).where(Account.id == order_in.account_id)).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    can_order = crud.order.has_funds(session=session, order_create=order_in)
    if not can_order:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    can_order = crud.order.tickets_left(session=session, order_create=order_in)
    if order_in.tickets_bought < 1:
        raise HTTPException(status_code=400, detail="Must buy at least 1 ticket")
    if not can_order:
        raise HTTPException(status_code=400, detail="Not enough tickets left")

    order = crud.order.create_order(session=session, order_create=order_in)
    crud.match.update_tickets_left(session=session, order_create=order_in)

    user = session.get(User, account.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    crud.account.update_funds(session=session, order_create=order_in)

    order_out = OrderOut(
        id=order.id,
        tickets_bought=order.tickets_bought,
        match_id=order.match_id,
        account_id=order.account_id,
        user_name=user.full_name
    )
    return order_out


# get all orders
@router.get('/',
            dependencies=[Depends(get_current_active_superuser)],
            response_model=OrdersOut)
async def get_orders(session: SessionDep, skip: int = 0, limit: int = 100):
    orders = crud.order.get_orders(session=session, skip=skip, limit=limit)
    order_out_list = []
    for order in orders:
        account = session.get(Account, order.account_id)
        user = session.get(User, account.user_id)
        account = session.get(Account, order.account_id)
        order_out = OrderOut(
            id=order.id,
            tickets_bought=order.tickets_bought,
            match_id=order.match_id,
            account_id=order.account_id,
            user_name=user.full_name
        )
        order_out_list.append(order_out)

    return OrdersOut(data=order_out_list, count=len(order_out_list))
