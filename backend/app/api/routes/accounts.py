""" Account management routes """

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import col, delete, func, select
from typing import List
from app import crud
from app.api.deps import SessionDep, get_current_user
from app.models import (Account, Message, AccountOut,
                        AccountCreate, OrderOut,
                        OrderCreate, OrdersOut, User, Match)

router = APIRouter()


# post account
@router.post('/',
             dependencies=[Depends(get_current_user)],
             response_model=AccountOut)
async def create_account(session: SessionDep, account_in: AccountCreate):
    # check if current user is the same as the user_id in the account
    account = crud.account.get_account(session=session, user_id=account_in.user_id)
    user = session.get(User, account_in.user_id)
    if account:
        raise HTTPException(status_code=400, detail="Account already exists")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    account_create = crud.account.create_account(session=session, account_create=account_in)

    account_out = AccountOut(
        id=account_create.id,
        user_id=account_create.user_id,
        available_money=account_create.available_money
    )
    return account_out


# get account
@router.get('/{user_id}',
            dependencies=[Depends(get_current_user)],
            response_model=AccountOut)
async def get_account(session: SessionDep, user_id: int):
    account = crud.account.get_user_account(session=session, user_id=user_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account_out = AccountOut(
        id=account.id,
        user_id=account.user_id,
        available_money=account.available_money
    )

    return account_out
