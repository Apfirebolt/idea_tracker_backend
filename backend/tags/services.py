from fastapi import HTTPException, status
from typing import List
from backend.ideas import models
from backend.auth.models import User
from sqlalchemy.orm import Session


async def create_new_tag(
    request, database: Session, current_user: User
) -> models.Tag:
    try:
        # error if the same tag has been added by the same user
        existing_tag = (
            database.query(models.Tag)
            .filter(
                models.Tag.name == request.name,
                models.Tag.user_id == current_user.id,
            )
            .first()
        )
        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag already exists in your collection.",
            )

        new_tag = models.Tag(
            name=request.name,
            description=request.description,
            user_id=current_user.id,
        )
        database.add(new_tag)
        database.commit()
        database.refresh(new_tag)
        return new_tag
    except Exception as e:
        print(f"Error creating tag: {str(e)}")
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the tag: {str(e)}",
        )


async def get_tag_listing(database, current_user) -> List[models.Tag]:
    try:
        tags = (
            database.query(models.Tag)
            .filter(models.Tag.user_id == current_user)
            .all()
        )
        return tags
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching tags: {str(e)}",
        )


async def get_tag_by_id(tag_id, current_user, database):
    try:
        tag = (
            database.query(models.Tag)
            .filter_by(id=tag_id, user_id=current_user)
            .first()
        )
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tag Not Found!"
            )
        return tag
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the tag: {str(e)}",
        )
    

async def update_tag_by_id(
    tag_id, request, current_user: User, database: Session
) -> models.Tag:
    try:
        # check if tag belongs to the user
        tag = (
            database.query(models.Tag)
            .filter_by(id=tag_id, user_id=current_user.id)
            .first()
        )
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tag Not Found!"
            )

        # update tag details
        tag.name = request.name or tag.name
        tag.description = request.description or tag.description

        database.commit()
        database.refresh(tag)
        return tag
    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the tag: {str(e)}",
        )


async def delete_tag_by_id(tag_id, current_user: User, database: Session):
    try:
        # check if tag belongs to the user
        tag = (
            database.query(models.Tag)
            .filter_by(id=tag_id, user_id=current_user.id)
            .first()
        )
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tag Not Found!"
            )
        database.query(models.Tag).filter(models.Tag.id == tag_id).delete()
        database.commit()
    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the tag: {str(e)}",
        )
