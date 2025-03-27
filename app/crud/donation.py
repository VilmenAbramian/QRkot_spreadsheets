from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import (
    DonationCreate, DonationGet
)


class CRUDDonation(
    CRUDBase[Donation, DonationCreate, DonationGet]
):

    async def get_user_donations(
            self,
            session: AsyncSession,
            user: User,
    ):
        return (
            await session.execute(
                select(Donation).where(
                    Donation.user_id == user.id
                )
            )
        ).scalars().all()


donation_crud = CRUDDonation(Donation)
