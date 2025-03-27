from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):

    async def get_project_id_by_name(
            self, charityproject_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        return (
            await session.execute(
                select(CharityProject.id).where(
                    CharityProject.name == charityproject_name
                )
            )
        ).scalars().first()

    async def get_projects_by_completion_rate(
            self, session: AsyncSession
    ):
        time_delta = (
            func.julianday(CharityProject.close_date) -
            func.julianday(CharityProject.create_date)
        )
        return (
            await session.execute(
                select(
                    CharityProject.name,
                    time_delta.label('time'),
                    CharityProject.description,
                ).where(
                    CharityProject.fully_invested == 1
                ).order_by(time_delta.label('time'))
            )
        ).all()


charityproject_crud = CRUDCharityProject(CharityProject)
