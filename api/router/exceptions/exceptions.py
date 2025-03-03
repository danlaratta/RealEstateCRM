from fastapi import HTTPException, status

def database_exception(error: Exception) -> HTTPException:
    error_message = str(error) if error else "Unknown database error" # Extracts the error message from exception
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Database Error Occurred: {error_message}"
    )


def user_not_found_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No user found, register for an account and log in.",
        headers={"WWW-Authenticate": "Bearer"},  # Follows authentication standards
    )