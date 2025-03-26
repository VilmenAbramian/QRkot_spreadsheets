from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = '%Y/%m/%d %H:%M:%S'
MAX_CELLS = 5_000_000
COLUMNS_LIMIT = 18_278

SPREADSHEET_BODY_TEMPLATE = dict(
    properties=dict(
        title='Отчет на ...',
        locale='ru_RU'
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Список проектов',
        gridProperties=dict(
            rowCount=None,
            columnCount=None,
        )
    ))]
)

TABLE_VALUES = [
    ['Отчёт от', None],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание проекта']
]


def format_time_in_days(time_in_days: float) -> str:
    days = int(time_in_days)
    fractional_day = time_in_days - days
    hours = int(fractional_day * 24)
    minutes = int((fractional_day * 24 - hours) * 60)
    seconds = int(((fractional_day * 24 - hours) * 60 - minutes) * 60)
    if days > 1:
        return f'{days} days {hours}:{minutes}:{seconds}'
    return f'{days} day, {hours}:{minutes}:{seconds}'


async def prepare_data(projects):
    """
    Возвращает подготовленные данные для записи в таблицу, а также
    необходимое количество строк и колонок.
    """
    table_values = deepcopy(TABLE_VALUES)
    table_values[0][1] = datetime.now().strftime(FORMAT)
    table_values.extend(
        list(project.values()) for project in projects
    )
    return table_values, len(table_values), max(map(len, table_values))


async def spreadsheets_create(
        wrapper_service: Aiogoogle,
        rows: int,
        columns: int,
        spreadsheet_template: dict = SPREADSHEET_BODY_TEMPLATE,
):
    service = await wrapper_service.discover('sheets', 'v4')
    if columns > COLUMNS_LIMIT:
        raise ValueError(
            'Слишком много колонок!'
        )
    if rows * columns > MAX_CELLS:
        raise ValueError(
            'Слишком много ячеек!'
        )
    now_date_time = datetime.now().strftime(FORMAT)
    body = deepcopy(spreadsheet_template)
    body['properties']['title'] = f'Отчет на {now_date_time}'
    grid_properties = body['sheets'][0]['properties']['gridProperties']
    grid_properties['rowCount'] = rows
    grid_properties['columnCount'] = columns
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=dict(
                type='user',
                role='writer',
                emailAddress=settings.email,
            ),
            fields='id'
        )
    )


async def spreadsheets_update_value(
        wrapper_services: Aiogoogle,
        spreadsheet_id: str,
        table_values: list,
        rows: int,
        columns: int,
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows}C{columns}',
            valueInputOption='USER_ENTERED',
            json=dict(
                majorDimension='ROWS',
                values=table_values
            )
        )
    )