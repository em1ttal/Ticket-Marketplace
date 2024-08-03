""" Match management routes """

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import col, delete, func, select
from typing import List
from app import crud
from app.api.deps import SessionDep, get_current_active_superuser
from app.models import (Match, Message, MatchOut,
                        MatchesOut, MatchCreate, MatchCreateIn,
                        MatchUpdate, MatchUpdateIn, Team, Competition)

router = APIRouter()

@router.get('/', response_model=MatchesOut)
async def get_matches(session: SessionDep, skip: int = 0, limit: int = 10):
    query = select(Match).offset(skip).limit(limit)
    matches = session.exec(query).all()

    # Transform Match to MatchOut
    match_out_list = []
    for match in matches:
        local_team = session.get(Team, match.local_id)
        visitor_team = session.get(Team, match.visitor_id)
        competition = session.get(Competition, match.competition_id)
        match_out = MatchOut(
            id=match.id,
            date=match.date,
            price=match.price,
            local_team=local_team,
            visitor_team=visitor_team,
            competition=competition,
            total_available_tickets=match.total_available_tickets
        )
        match_out_list.append(match_out)

    count_statement = select(func.count()).select_from(Match)
    count = session.exec(count_statement).one()

    return MatchesOut(data=match_out_list, count=count)


@router.get('/{match_id}', response_model=MatchOut)
async def get_match(session: SessionDep, match_id: int):
    match = crud.match.get_match(session=session, match_id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail=f'Match with id {match_id} not found')

    local_team = session.get(Team, match.local_id)
    visitor_team = session.get(Team, match.visitor_id)
    competition = session.get(Competition, match.competition_id)
    match_out = MatchOut(
        id=match.id,
        date=match.date,
        price=match.price,
        local_team=local_team,
        visitor_team=visitor_team,
        competition=competition,
        total_available_tickets=match.total_available_tickets
    )

    return match_out


@router.delete('/{match_id}',
               dependencies=[Depends(get_current_active_superuser)],
               response_model=Message)
async def delete_match(session: SessionDep, match_id: int):
    match = crud.match.get_match(session=session, match_id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail=f'Match with id {match_id} not found')
    crud.match.delete_match(session=session, match_id=match_id)

    return Message(message=f'Match with id {match_id} deleted')


@router.put('/{match_id}',
            dependencies=[Depends(get_current_active_superuser)],
            response_model=MatchOut)
async def update_match(session: SessionDep, match_in: MatchUpdateIn|MatchCreateIn):
    if match_in.local_team == match_in.visitor_team:
        raise HTTPException(status_code=400, detail='Local and visitor teams must be different')
    local_team = crud.team.get_team_by_name(session=session, name=match_in.local_team)
    visitor_team = crud.team.get_team_by_name(session=session, name=match_in.visitor_team)
    competition = crud.competition.get_competition_by_name(session=session, name=match_in.competition)
    if not local_team or not visitor_team or not competition:
        raise HTTPException(status_code=400, detail='Local, visitor and competition must exist')
    if match_in.price < 0:
        raise HTTPException(status_code=400, detail='Price must be a positive number')

    match = crud.match.get_match(session=session, match_id=match_in.id)
    if match:
        match_update = MatchUpdate(
            date=match_in.date,
            price=match_in.price,
            local_id=local_team.id,
            visitor_id=visitor_team.id,
            competition_id=competition.id
        )
        match = crud.match.update_match(session=session, db_match=match, match_in=match_update)
    else:
        match_create = MatchCreate(
            date=match_in.date,
            price=match_in.price,
            local_id=local_team.id,
            visitor_id=visitor_team.id,
            competition_id=competition.id
        )
        match = crud.match.create_match(session=session, match_create=match_create)

    match_out = MatchOut(
        id=match.id,
        date=match.date,
        price=match.price,
        local_team=local_team,
        visitor_team=visitor_team,
        competition=competition,
        total_available_tickets=match.total_available_tickets
    )

    return match_out


@router.post('/',
             dependencies=[Depends(get_current_active_superuser)],
             response_model=MatchOut)
async def create_match(session: SessionDep, match_in: MatchCreateIn):
    local_team = crud.team.get_team_by_name(session=session, name=match_in.local_team)
    visitor_team = crud.team.get_team_by_name(session=session, name=match_in.visitor_team)
    competition = crud.competition.get_competition_by_name(session=session, name=match_in.competition)
    if not local_team or not visitor_team or not competition:
        raise HTTPException(status_code=400, detail='Local, visitor and competition must exist')
    if match_in.local_team == match_in.visitor_team:
        raise HTTPException(status_code=400, detail='Local and visitor teams must be different')
    if match_in.price < 0:
        raise HTTPException(status_code=400, detail='Price must be a positive number')

    match_create = MatchCreate(date=match_in.date, price=match_in.price, local_id=local_team.id, visitor_id=visitor_team.id, competition_id=competition.id, total_available_tickets=match_in.total_available_tickets)
    match = crud.match.create_match(session=session, match_create=match_create)

    match_out = MatchOut(
        id=match.id,
        date=match.date,
        price=match.price,
        local_team=local_team,
        visitor_team=visitor_team,
        competition=competition,
        total_available_tickets=match.total_available_tickets
    )

    return match_out
