from datetime import datetime

from app.models import FoundBase


def spread_donations(
    target: FoundBase,
    sources: list[FoundBase]
) -> list[FoundBase]:
    updated = []
    current_time = datetime.now()
    for source in sources:
        available_investment = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for item in (target, source):
            item.invested_amount += available_investment
            if item.invested_amount == item.full_amount:
                item.fully_invested = True
                item.close_date = current_time
        updated.append(source)
        if target.fully_invested:
            break
    return updated