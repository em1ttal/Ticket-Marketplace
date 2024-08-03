from sqlmodel import Field, Relationship
from .base import SQLModel
from typing import Optional
from .match import Match


class AccountBase(SQLModel):
    available_money: float


class Account(AccountBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    orders: list["Order"] = Relationship(back_populates="account")


class OrderBase(SQLModel):
    tickets_bought: int


class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: Optional[int] = Field(default=None, foreign_key="match.id")
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    match: "Match" = Relationship(back_populates="orders")
    account: "Account" = Relationship(back_populates="orders")
    user: "User" = Relationship(back_populates="orders")


class OrderCreate(OrderBase):
    match_id: int
    account_id: int
    user_id: int


class OrderUpdate(OrderBase):
    tickets_bought: int | None = None


class OrderOut(OrderBase):
    id: int
    match_id: int
    account_id: int
    user_name: str
    tickets_bought: int


class OrdersOut(SQLModel):
    data: list[OrderOut]
    count: int


class Message(SQLModel):
    message: str


class AccountCreate(AccountBase):
    user_id: int
    available_money: float


class AccountUpdate(AccountBase):
    available_money: float | None = None


class AccountOut(AccountBase):
    id: int
    user_id: int
    orders: Optional[list[OrderOut]] | None = None
    available_money: float


class AccountsOut(SQLModel):
    data: list[AccountOut]
    count: int
