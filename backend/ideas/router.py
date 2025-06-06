from typing import List
from fastapi import APIRouter, Depends, status, Response, File, UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate

from sqlalchemy.orm import Session
from backend.auth.jwt import get_current_user
from backend.auth.models import User


from backend import db

from . import schema
from . import services
from backend.tags.schema import AddTag


router = APIRouter(tags=["Idea"], prefix="/api/ideas")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.IdeaCreateResponse)
async def create_new_idea(
    request: schema.IdeaBase,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    user = database.query(User).filter(User.email == current_user.email).first()
    result = await services.create_new_idea(request, database, user)
    return result


@router.get("/", status_code=status.HTTP_200_OK, response_model=Page[schema.IdeaList])# Cache for 1 minute
async def idea_list(
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    idea_query = await services.get_idea_listing(database, current_user.id) # Renamed service function slightly
    return sqlalchemy_paginate(database,idea_query)


@router.get("/shared", status_code=status.HTTP_200_OK, response_model=Page[schema.IdeaList])
async def shared_idea_list(
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
    request: None = None,
    response: Response = None,
):
    shared_ideas_query = await services.get_shared_idea_listing(database, current_user)
    return sqlalchemy_paginate(database, shared_ideas_query)


@router.get(
    "/{idea_id}", status_code=status.HTTP_200_OK, response_model=schema.IdeaList
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
    "/{idea_id}", status_code=status.HTTP_200_OK, response_model=schema.IdeaCreateResponse
)
async def update_idea_by_id(
    idea_id: int,
    request: schema.IdeaUpdate,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.update_idea_by_id(idea_id, request, current_user, database)

@router.post(
    "/{idea_id}/tags", status_code=status.HTTP_200_OK, response_model=schema.IdeaBase
)
async def add_tags_to_idea(
    idea_id: int,
    request: AddTag,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.add_tags_to_idea(idea_id, request.tags, current_user, database)


@router.post(
    "/{idea_id}/comments", status_code=status.HTTP_200_OK, response_model=schema.IdeaCommentSchema
)
async def add_comments_to_idea(
    idea_id: int,
    request: schema.AddIdeaComment,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.add_comments_to_idea(idea_id, request, current_user, database)


@router.post(
    "/{idea_id}/images", status_code=status.HTTP_201_CREATED
)
async def upload_idea_image(
    idea_id: int,
    file: UploadFile = File(...),
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    # You should implement this function in your services module
    return await services.upload_idea_image(idea_id, file, current_user, database)
