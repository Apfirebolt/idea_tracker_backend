from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from backend.auth.jwt import get_current_user
from backend.auth.models import User

from backend import db

from backend.auth.schema import DisplayAccount
from . import services


router = APIRouter(tags=["Users"], prefix="/api/users")


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[DisplayAccount])
async def user_list(
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    result = await services.get_user_listing(database, current_user.id)
    return result


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=DisplayAccount
)
async def get_user_by_id(
    user_id: int,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.get_user_by_id(user_id, current_user.id, database)