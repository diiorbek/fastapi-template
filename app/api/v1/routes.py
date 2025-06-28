from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud import user as crud_user

router = APIRouter()

@router.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud_user.create_user(db, user)
