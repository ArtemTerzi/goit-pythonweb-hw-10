from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas import UserCreate, TokenModel, TokenRefreshRequest, User
from src.services.auth import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    get_current_user,
    Hash,
)
from src.services.users import UserService
from src.database.db import get_db
from src.conf import messages

router = APIRouter(prefix="/auth", tags=["auth"])
hash_handler = Hash()


@router.post("/signup")
async def signup(body: UserCreate, db: AsyncSession = Depends(get_db)):
    user_servive = UserService(db)

    exist_user = await user_servive.get_user_by_username(body.username)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account with this username already exists",
        )

    exist_email = await user_servive.get_user_by_email(body.email)
    if exist_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account with this email already exists",
        )

    hashed_password = hash_handler.get_password_hash(body.password)
    body.password = hashed_password
    return await user_servive.create_user(body)


@router.post("/login", response_model=TokenModel)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)

    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.INVALID_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )

    # if not user.confirmed:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail=messages.USER_NOT_CONFIRMED,
    #     )

    access_token = await create_access_token(data={"sub": user.username})
    refresh_token = await create_refresh_token(data={"sub": user.username})
    user.refresh_token = refresh_token
    await db.commit()
    await db.refresh(user)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh-token", response_model=TokenModel)
async def refresh_token(
    request: TokenRefreshRequest, db: AsyncSession = Depends(get_db)
):
    user = await verify_refresh_token(request.refresh_token, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    new_access_token = await create_access_token(data={"sub": user.username})
    new_refresh_token = await create_refresh_token(data={"sub": user.username})

    user.refresh_token = new_refresh_token
    await db.commit()
    await db.refresh(user)
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    return {"message": "secret router", "owner": current_user.username}
