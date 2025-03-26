from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charityproject_crud

from app.utils import (
    format_time_in_days, prepare_data, spreadsheets_create,
    set_user_permissions, spreadsheets_update_value
)

router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    """Только для суперюзеров."""
    table_body, rows, columns = await prepare_data(
        dict(
            name=project.name,
            time=format_time_in_days(project.time),
            description=project.description,
        ) for project in
        await charityproject_crud.get_projects_by_completion_rate(session)
    )
    try:
        spreadsheet_id, spreadsheet_url = await spreadsheets_create(
            wrapper_services, rows, columns
        )
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e),
        )
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(
        wrapper_services,
        spreadsheet_id,
        table_body,
        rows,
        columns
    )
    return spreadsheet_url