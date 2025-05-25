from fastapi import HTTPException, status
from typing import List
from backend.ideas import models
from backend.auth.models import User
from sqlalchemy.orm import Session


async def create_new_script(
    request, database: Session, current_user: User
) -> models.IdeaScript:
    try:
        # check for script count
        script_count = (
            database.query(models.IdeaScript)
            .filter(
                models.IdeaScript.idea_id == request.idea_id,
                models.IdeaScript.user_id == current_user.id,
            )
            .count()
        )
        if script_count >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot add more than 3 scripts for this idea.",
            )

        new_script = models.IdeaScript(
            idea_id=request.idea_id,
            title=request.title,
            script_content=request.script_content,
            user_id=current_user.id,
        )
        database.add(new_script)
        database.commit()
        database.refresh(new_script)
        return new_script

    except HTTPException as http_exc:

        print(f"HTTP Exception caught: Status {http_exc.status_code}, Detail: {http_exc.detail}")
        database.rollback()
        raise http_exc

    except Exception as e:
        print(f"Error creating script: {str(e)}")
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the script: {str(e)}",
        )


async def get_script_listing(database, current_user) -> List[models.IdeaScript]:
    try:
        scripts = (
            database.query(models.IdeaScript)
            .filter(models.IdeaScript.user_id == current_user)
            .all()
        )
        return scripts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching scripts: {str(e)}",
        )


async def get_script_by_id(script_id, current_user, database):
    try:
        script = (
            database.query(models.IdeaScript)
            .filter_by(id=script_id, user_id=current_user)
            .first()
        )
        if not script:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Script Not Found!"
            )
        return script
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the script: {str(e)}",
        )


async def update_script_by_id(
    script_id, request, current_user: User, database: Session
) -> models.IdeaScript:
    try:
        # check if script belongs to the user
        script = (
            database.query(models.IdeaScript)
            .filter_by(id=script_id, user_id=current_user.id)
            .first()
        )
        if not script:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Script Not Found!"
            )

        # update script details
        script.script_content = request.script_content or script.script_content
        script.title = request.title or script.title

        database.commit()
        database.refresh(script)
        return script
    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the script: {str(e)}",
        )


async def delete_script_by_id(script_id, current_user: User, database: Session):
    try:
        # check if script belongs to the user
        script = (
            database.query(models.IdeaScript)
            .filter_by(id=script_id, user_id=current_user.id)
            .first()
        )
        if not script:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Script Not Found!"
            )
        database.query(models.IdeaScript).filter(
            models.IdeaScript.id == script_id
        ).delete()
        database.commit()
    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the script: {str(e)}",
        )
