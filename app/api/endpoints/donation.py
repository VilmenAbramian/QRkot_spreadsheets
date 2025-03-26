from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import charityproject_crud, donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationGet
from app.utils.investment_util import spread_donations

router = APIRouter()


@router.post('/', response_model=DonationGet,)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
) -> DonationGet:
    """Создание пожертвования."""
    new_donation = await donation_crud.create(
        donation, session, user, do_commit=False
    )
    session.add_all(
        spread_donations(
            target=new_donation,
            sources=await charityproject_crud.get_opened(session)
        )
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get('/my', response_model=list[DonationGet])
async def get_all_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Получить все пожертвования пользователя."""
    return await donation_crud.get_user_donations(session, user)


@router.get('/', response_model=list[DonationDB],)
async def get_whole_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_superuser),
):
    """
    Получение всех(совсем) пожертвований.

    Только для супер пользователей.
    """
    return await donation_crud.get_multi(session)