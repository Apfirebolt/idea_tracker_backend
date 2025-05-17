from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from backend.auth.jwt import get_current_user
from backend.auth.models import User

from backend import db

from . import schema
from . import services


router = APIRouter(tags=["Idea"], prefix="/api/ideas")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.IdeaBase)
async def create_new_idea(
    request: schema.IdeaBase,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    user = database.query(User).filter(User.email == current_user.email).first()
    result = await services.create_new_idea(request, database, user)
    return result


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.IdeaList])
async def idea_list(
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    result = await services.get_idea_listing(database, current_user.id)
    return result


@router.get(
    "/{idea_id}", status_code=status.HTTP_200_OK, response_model=schema.IdeaBase
)
async def get_idea_by_id(
    idea_id: int,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.get_idea_by_id(idea_id, current_user.id, database)


@router.delete(
    "/{idea_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def delete_idea_by_id(
    idea_id: str,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.delete_idea_by_id(idea_id, current_user, database)


@router.put(
    "/{idea_id}", status_code=status.HTTP_200_OK, response_model=schema.IdeaBase
)
async def update_idea_by_id(
    idea_id: int,
    request: schema.IdeaUpdate,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.update_idea(idea_id, request, current_user, database)
