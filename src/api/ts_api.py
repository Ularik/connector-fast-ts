from src.database import AsyncSessionTs
from src.models.ts_models import Car, CarHistory, PersonInfo, RelationEntity, RefCarBrand, RefCarModel
from fastapi import APIRouter
from sqlalchemy import select
from src.schemas.payload import Payload


router = APIRouter()


# 21710198200951 pin
# 12205199501354
# KLAJF69VDYK480790   - vin
@router.post('/get-car', tags=["cars"])
async def get_car(payload: Payload):
    """
    { "subject": { "pin": "21710198200951" }, "requested_groups": ["person_cars"], "paging": { "limit": 10, "offset": 0 } }
    """
    subject = {key: val.upper() for key, val in payload.subject.items()}

    async with AsyncSessionTs() as session:
        stmt = (
            select(CarHistory.car_id,
                   CarHistory.vin,
                   CarHistory.dfrom,
                   CarHistory.dto,
                   RefCarBrand.name.label("brand"),
                   RefCarModel.name.label("model")
                   ).select_from(PersonInfo).filter_by(**subject)
        )

        stmt = (stmt
            .join(PersonInfo.relation_entity)
            .join(RelationEntity.car_history).where(CarHistory.dfrom != CarHistory.dto)
            .outerjoin(CarHistory.car_model)
            .outerjoin(RefCarModel.car_brand)

        )
        result = await session.execute(stmt)
        result = result.all()
        data = {}
        for res in result:
            if res.vin in data:
                car_data: dict = data[res.vin]
                car_data['periods']: list[dict] = [{'dfrom': res.dfrom, 'dto': res.dto} , *car_data['periods']]
            else:
                data[res.vin] = {'periods': [{'dfrom': res.dfrom, 'dto': res.dto}]}
            data[res.vin]['brand'] = res.brand
            data[res.vin]['model'] = res.model


    return data


