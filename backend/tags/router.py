from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from backend.auth.jwt import get_current_user
from backend.auth.models import User

from backend import db

from . import schema
from . import services


router = APIRouter(tags=["Tag"], prefix="/api/tags")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.TagBase)
async def create_new_tag(
    request: schema.TagBase,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    user = database.query(User).filter(User.email == current_user.email).first()
    result = await services.create_new_tag(request, database, user)
    return result


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.TagList])
async def tag_list(
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    result = await services.get_tag_listing(database, current_user.id)
    return result


@router.get(
    "/{tag_id}", status_code=status.HTTP_200_OK, response_model=schema.TagBase
)
async def get_tag_by_id(
    tag_id: int,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.get_tag_by_id(tag_id, current_user.id, database)


@router.delete(
    "/{tag_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def delete_tag_by_id(
    tag_id: str,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.delete_tag_by_id(tag_id, current_user, database)


@router.put(
    "/{tag_id}", status_code=status.HTTP_200_OK, response_model=schema.TagBase
)
async def update_tag_by_id(
    tag_id: int,
    request: schema.TagUpdate,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.update_tag_by_id(tag_id, request, current_user, database)
