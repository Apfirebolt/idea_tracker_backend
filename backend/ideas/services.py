from fastapi import HTTPException, status
from typing import List
from . import models
from backend.auth.models import User
from sqlalchemy.orm import Session


async def create_new_idea(
    request, database: Session, current_user: User
) -> models.Idea:
    try:
        # error if the same idea has been added by the same user
        existing_idea = (
            database.query(models.Idea)
            .filter(
                models.Idea.title == request.title,
                models.Idea.user_id == current_user.id,
            )
            .first()
        )
        if existing_idea:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Idea already exists in your collection.",
            )

        new_idea = models.Idea(
            title=request.title,
            description=request.description,
            user_id=current_user.id,
        )
        database.add(new_idea)
        database.commit()
        database.refresh(new_idea)
        return new_idea
    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the idea: {str(e)}",
        )


async def get_idea_listing(database, current_user) -> List[models.Idea]:
    try:
        ideas = (
            database.query(models.Idea)
            .filter(models.Idea.user_id == current_user)
            .all()
        )
        return ideas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching ideas: {str(e)}",
        )


async def get_idea_by_id(idea_id, current_user, database):
    try:
        idea = (
            database.query(models.Idea)
            .filter_by(id=idea_id, user_id=current_user)
            .first()
        )
        if not idea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Idea Not Found!"
            )
        return idea
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the idea: {str(e)}",
        )
    

async def update_idea_by_id(
    idea_id, request, current_user: User, database: Session
) -> models.Idea:
    try:
        # check if idea belongs to the user
        idea = (
            database.query(models.Idea)
            .filter_by(id=idea_id, user_id=current_user.id)
            .first()
        )
        if not idea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Idea Not Found!"
            )

        # update idea details
        idea.title = request.title or idea.title
        idea.description = request.description or idea.description

        database.commit()
        database.refresh(idea)
        return idea
    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the idea: {str(e)}",
        )


async def delete_idea_by_id(idea_id, current_user: User, database: Session):
    try:
        # check if idea belongs to the user
        idea = (
            database.query(models.Idea)
            .filter_by(id=idea_id, user_id=current_user.id)
            .first()
        )
        if not idea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Idea Not Found!"
            )
        database.query(models.Idea).filter(models.Idea.id == idea_id).delete()
        database.commit()
    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the idea: {str(e)}",
        )
