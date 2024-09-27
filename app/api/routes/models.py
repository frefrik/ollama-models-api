from typing import Any

from fastapi import APIRouter
from sqlmodel import func, or_, select

from app.api.deps import SessionDep
from app.models import Model, ModelsPublic

router = APIRouter()


@router.get("", response_model=ModelsPublic)
def read_models(
    session: SessionDep,
    search: str | None = None,
    model_identifier: str | None = None,
    namespace: str | None = None,
    capability: str | None = None,
    model_type: str | None = None,
    sort_by: str = "pulls",
    order: str = "desc",
    limit: int = 20,
    skip: int = 0,
) -> Any:
    """
    Retrieve models with optional filtering, sorting, and pagination.
    """
    valid_sort_fields = ["pulls", "last_updated"]
    if sort_by not in valid_sort_fields:
        sort_by = "pulls"

    if order not in ["asc", "desc"]:
        order = "desc"

    # Build the base query
    query = select(Model)

    # Apply filters
    if model_identifier:
        query = query.where(Model.model_identifier == model_identifier)

    if namespace:
        query = query.where(Model.namespace == namespace)

    if model_type:
        query = query.where(Model.model_type == model_type)

    if capability:
        query = query.where(Model.capability == capability)

    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Model.model_identifier.contains(search_term),
                Model.description.contains(search_term),
            )
        )

    # Get total count before pagination
    count_subquery = query.subquery()
    count_query = select(func.count()).select_from(count_subquery)
    total_count = session.exec(count_query).one()

    # Apply sorting
    sort_column = getattr(Model, sort_by)
    if order == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()
    query = query.order_by(sort_column)

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute the query
    models = session.exec(query).all()

    # Retrieve the most recent timestamp (data_updated)
    max_timestamp_query = select(func.max(Model.timestamp))
    data_updated = session.exec(max_timestamp_query).one()

    return ModelsPublic(
        models=models,
        total_count=total_count,
        limit=limit,
        skip=skip,
        data_updated=data_updated,
    )
