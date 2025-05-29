from fastapi import HTTPException, status
from typing import List
from . import models
from backend.auth.models import User
from sqlalchemy.orm import Session, joinedload
import logging

logger = logging.getLogger("idea_app")


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
            # Log this specific error, potentially with the user ID
            logger.warning(
                "Attempt to create duplicate idea by user ID %s: %s",
                current_user.id,
                request.title,
                extra={"object_id": current_user.id},  # Use 'extra' for custom fields
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Idea already exists in your collection.",
            )

        # Create the new idea
        new_idea = models.Idea(
            title=request.title,
            description=request.description,
            user_id=current_user.id,
        )

        # Handle tags if provided
        tags = getattr(request, "tags", None)
        if tags and isinstance(tags, list):
            for tag_name in tags:
                tag = (
                    database.query(models.Tag)
                    .filter_by(name=tag_name, user_id=current_user.id)
                    .first()
                )
                if not tag:
                    tag = models.Tag(name=tag_name, user_id=current_user.id)
                    database.add(tag)
                    database.flush()  # Ensure tag.id is available
                new_idea.tags.append(tag)

        database.add(new_idea)
        database.commit()
        database.refresh(new_idea)
        return new_idea
    except HTTPException as http_exc:
        # Re-raise HTTPExceptions as they are handled by FastAPI's error handlers
        raise http_exc
    except Exception as e:
        database.rollback()
        # Log the error with relevant information
        logger.error(
            "Error creating idea for user ID %s: %s",
            current_user.id,
            str(e),
            exc_info=True,  # exc_info=True adds traceback
            extra={"object_id": current_user.id},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the idea: {str(e)}",
        )


async def get_idea_listing(database, current_user) -> List[models.Idea]:
    try:
        query = database.query(models.Idea).filter(models.Idea.user_id == current_user)
        return query
    except Exception as e:
        logger.error(
            "Error getting idea listing for user ID %s: %s",
            current_user,
            str(e),
            exc_info=True,
            extra={"object_id": current_user},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while preparing the idea query: {str(e)}",
        )


async def get_shared_idea_listing(database, current_user) -> List[models.Idea]:
    try:
        if not current_user:
            logger.warning(
                "Unauthorized attempt to access shared ideas (no current user)."
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated.",
            )
        query = database.query(models.Idea).filter(models.Idea.is_shared == 1)
        return query
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(
            "Error getting shared idea listing for user ID %s: %s",
            current_user,
            str(e),
            exc_info=True,
            extra={"object_id": current_user},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while preparing the idea query: {str(e)}",
        )


async def get_idea_by_id(idea_id, current_user, database):
    try:
        idea = (
            database.query(models.Idea)
            .options(
                joinedload(models.Idea.comments).joinedload(models.IdeaComment.user),
                joinedload(models.Idea.tags),
                joinedload(models.Idea.scripts),
            )
            .filter_by(id=idea_id, user_id=current_user)
            .first()
        )
        if not idea:
            logger.warning(
                "Idea ID %s not found for user ID %s",
                idea_id,
                current_user,
                extra={"object_id": idea_id},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Idea Not Found!"
            )
        return idea

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(
            "Error fetching idea ID %s for user ID %s: %s",
            idea_id,
            current_user,
            str(e),
            exc_info=True,
            extra={"object_id": idea_id},
        )
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
            logger.warning(
                "Attempt to update non-existent or unauthorized idea ID %s by user ID %s",
                idea_id,
                current_user.id,
                extra={"object_id": idea_id},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Idea Not Found!"
            )

        # update idea details
        idea.title = request.title or idea.title
        idea.description = request.description or idea.description
        idea.status = request.status or idea.status
        # if is_shared is provided and true then set is_shared to 1
        if hasattr(request, "is_shared"):
            if request.is_shared:
                idea.is_shared = 1
            else:
                idea.is_shared = 0

        # update tags if provided
        if hasattr(request, "tags") and isinstance(request.tags, list):
            # clear existing tags
            idea.tags.clear()
            for tag_name in request.tags:
                tag = (
                    database.query(models.Tag)
                    .filter_by(name=tag_name, user_id=current_user.id)
                    .first()
                )
                if not tag:
                    tag = models.Tag(name=tag_name, user_id=current_user.id)
                    database.add(tag)
                    database.flush()

                idea.tags.append(tag)

        database.commit()
        database.refresh(idea)
        return idea

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        database.rollback()
        logger.error(
            "Error updating idea ID %s for user ID %s: %s",
            idea_id,
            current_user.id,
            str(e),
            exc_info=True,
            extra={"object_id": idea_id},
        )
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
            logger.warning(
                "Attempt to delete non-existent or unauthorized idea ID %s by user ID %s",
                idea_id,
                current_user.id,
                extra={"object_id": idea_id},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Idea Not Found!"
            )
        database.query(models.Idea).filter(models.Idea.id == idea_id).delete()
        database.commit()

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        database.rollback()
        logger.error(
            "Error deleting idea ID %s for user ID %s: %s",
            idea_id,
            current_user.id,
            str(e),
            exc_info=True,
            extra={"object_id": idea_id},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the idea: {str(e)}",
        )


async def add_comments_to_idea(
    idea_id: int, request, current_user: User, database: Session
) -> models.IdeaComment:
    try:
        # check if idea belongs to the user
        idea = database.query(models.Idea).filter_by(id=idea_id).first()
        if not idea:
            logger.warning(
                "Attempt to add comment to non-existent idea ID %s",
                idea_id,
                extra={"object_id": idea_id},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Idea Not Found!"
            )

        # if idea is not shared then comments are not allowed
        if idea.is_shared == 0:
            logger.warning(
                "Attempt to add comment to private idea ID %s by user ID %s",
                idea_id,
                current_user.id,
                extra={"object_id": idea_id},
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Comments are not allowed on private ideas.",
            )

        # Create a new comment
        new_comment = models.IdeaComment(
            content=request.content,
            idea_id=idea_id,  # Use idea_id from path, not request.idea_id
            user_id=current_user.id,
        )

        database.add(new_comment)
        database.commit()
        database.refresh(new_comment)
        return new_comment

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        database.rollback()
        logger.error(
            "Error adding comment to idea ID %s by user ID %s: %s",
            idea_id,
            current_user.id,
            str(e),
            exc_info=True,
            extra={"object_id": idea_id},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while adding the comment: {str(e)}",
        )
