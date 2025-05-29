from fastapi import HTTPException, status
from typing import List
from backend.auth.models import User


async def get_user_listing(database, current_user) -> List[User]:
    try:
        return database.query(User)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching users: {str(e)}",
        )


async def get_user_by_id(user_id, current_user, database) -> User:
    try:
        user = (
            database.query(User)
            .filter_by(id=user_id)
            .first()
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found!"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the user: {str(e)}",
        )