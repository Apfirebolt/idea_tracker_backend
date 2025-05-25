from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from backend.auth.jwt import get_current_user
from backend.auth.models import User

from backend import db

from . import schema
from . import services


router = APIRouter(tags=["Scripts"], prefix="/api/scripts")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.ScriptBase)
async def create_new_script(
    request: schema.ScriptBase,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    user = database.query(User).filter(User.email == current_user.email).first()
    result = await services.create_new_script(request, database, user)
    return result


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.ScriptList])
async def script_list(
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    result = await services.get_script_listing(database, current_user.id)
    return result


@router.get(
    "/{script_id}", status_code=status.HTTP_200_OK, response_model=schema.ScriptBase
)
async def get_script_by_id(
    script_id: int,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.get_script_by_id(script_id, current_user.id, database)


@router.delete(
    "/{script_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def delete_script_by_id(
    script_id: str,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.delete_script_by_id(script_id, current_user, database)


@router.put(
    "/{script_id}", status_code=status.HTTP_200_OK, response_model=schema.ScriptBase
)
async def update_script_by_id(
    script_id: int,
    request: schema.ScriptBase,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.update_script_by_id(script_id, request, current_user, database)
