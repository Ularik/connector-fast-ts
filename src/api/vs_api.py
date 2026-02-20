from src.database import AsyncSessionVS
from fastapi import APIRouter
from src.schemas.payload import Payload
from sqlalchemy.orm import selectinload, joinedload, with_loader_criteria
from sqlalchemy import select
from src.schemas.vs_schemas import PersonSchema, CardsSchema, StatementSchema
from src.models.vs_models import Cards, Person, Statement

router = APIRouter()


@router.post("/get-driver-doc")
async def get_driver_doc(payload: Payload):
    """
    { "subject": { "pin": "21710198200951" }, "requested_groups": ["person_driver_doc"], "paging": { "limit": 10, "offset": 0 } }
    """
    subject = {key: val.upper() for key, val in payload.subject.items()}
    async with AsyncSessionVS() as session:
        stmt = (
            select(Person, Statement, Cards)
            .select_from(Person).filter_by(**subject)
            .join(Person.statement)
            .join(Statement.cards).options(
                joinedload(Statement.address)
            )
            .filter(
                Statement.date_created.is_not(None),
                Cards.status != "INVALID",
            )
            .distinct()
        )

        result = await session.execute(stmt)
        result = result.all()
        data = {
            "statements": {}
        }
        for pers, state, card in result:
            if "person" not in data:
                data["person"] = PersonSchema.model_validate(pers)
            if state.id not in data["statements"]:
                data["statements"][state.id] = StatementSchema.model_validate(state).model_dump()
                data["statements"][state.id]["cards"] = [CardsSchema.model_validate(card)]
            elif state.id in data:
                data["statements"][state.id]["cards"].append(CardsSchema.model_validate(card))
        return data