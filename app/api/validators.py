from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models import CharityProject


async def check_name_duplicate(project_name: str, session: AsyncSession):
    charity_project_id = await charityproject_crud.get_project_id_by_name(
        project_name, session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Имя проекта не должно повторяться'
        )


async def charity_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    charity_project = await charityproject_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден'
        )
    return charity_project


async def check_project_is_open(project_id: int, session: AsyncSession):
    charity_project = await charityproject_crud.get(project_id, session)
    if charity_project.close_date and charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект менять нельзя'
        )


async def check_invested_amount(project_id: int, session: AsyncSession):
    """
    Проверка наличия средств в проекте
    """
    charity_project = await charityproject_crud.get(project_id, session)
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект внесены средства, его нельзя удалить.'
        )


async def check_invested_summ(
        project_id: int, new_full_amount: int, session: AsyncSession
):
    """
    Проверка, что новая сумма сборов не меньше,
    чем сумма уже внесенных средств
    """
    charity_project = await charityproject_crud.get(project_id, session)
    if charity_project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Нельзя изменить на сумму, меньшую, чем уже внесено в проект'
            )
        )
