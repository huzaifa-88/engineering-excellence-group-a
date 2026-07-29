from fastapi import HTTPException, status


class EmailAlreadyExistsError(HTTPException):
    """Raised when a user attempts to register with an email that is already taken."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "EMAIL_ALREADY_EXISTS",
                    "message": "User with this email already exists",
                }
            },
        )


class UsernameAlreadyExistsError(HTTPException):
    """Raised when a user attempts to register with a username that is already taken."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "USERNAME_ALREADY_EXISTS",
                    "message": "User with this username already exists",
                }
            },
        )


class UserNotFoundError(HTTPException):
    """Raised when a requested user cannot be found by ID or query."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "USER_NOT_FOUND",
                    "message": "User not found",
                }
            },
        )


class ProjectNotFoundError(HTTPException):
    """Raised when a requested project cannot be found by ID."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PROJECT_NOT_FOUND",
                    "message": "Project not found",
                }
            },
        )
