from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, charity_project_exists, check_invested_summ,
    check_invested_amount, check_project_is_open
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charityproject_crud, donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.utils.investment_util import spread_donations

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    '''Создать новый проект для сбора пожертвований.'''
    await check_name_duplicate(project.name, session)
    new_charity_project = await charityproject_crud.create(
        project, session, do_commit=False
    )
    session.add_all(
        spread_donations(
            target=new_charity_project,
            sources=await donation_crud.get_opened(session),
        )
    )
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get('/', response_model=list[CharityProjectDB])
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    '''Получить объекты всех проектов.'''
    return await charityproject_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    '''
    Изменение благотворительного проекта.

    Только для суперпользователей.
    '''
    charity_project = await charity_project_exists(project_id, session)
    await check_project_is_open(charity_project.id, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_invested_summ(
            charity_project.id, obj_in.full_amount, session
        )
    charity_project = await charityproject_crud.update(
        charity_project, obj_in, session, False
    )
    if charity_project.full_amount == charity_project.invested_amount:
        charity_project.fully_invested = True
        charity_project.close_date = datetime.now()
    else:
        session.add_all(
            spread_donations(
                target=charity_project,
                sources=await donation_crud.get_opened(session),
            )
        )
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удалить благотворительный проект.

    Только для суперпользователей.
    """
    charity_project = await charity_project_exists(project_id, session)
    await check_project_is_open(project_id, session)
    await check_invested_amount(project_id, session)
    return await charityproject_crud.remove(
        charity_project, session
    )
