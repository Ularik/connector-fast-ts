from src.database import AsyncSessionTs
from src.models.ts_models import (Car, CarHistory, PersonInfo,
                                  RelationEntity, RefCarBrand, RefCarModel, CarGovPlate, GovPlate)
from fastapi import APIRouter, Body
from sqlalchemy import select
from src.api.ts_schemas import GetCarsSchema


router = APIRouter()


# 21710198200951 pin
# 12205199501354
# KLAJF69VDYK480790   - vin
@router.post('/get-car', tags=["cars"])
async def get_car(payload: GetCarsSchema = Body(openapi_examples={
    "1": {
        "summary": "base example",
        "description": "base example",
        "value": {
            "subject": {"pin": "21710198200951"},
            "requested_groups": ["person_cars"],
            "paging": { "limit": 10, "offset": 0 }
        }
    }
})):
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
                   RefCarModel.name.label("model"),
                   GovPlate.full_number
                   ).select_from(PersonInfo).filter_by(**subject)
        )

        stmt = (stmt
            .join(PersonInfo.relation_entity)
            .join(RelationEntity.car_history)
            .outerjoin(CarHistory.car_model)
            .outerjoin(CarHistory.car_gov_plate)
            .outerjoin(CarGovPlate.gov_plate)
            .outerjoin(RefCarModel.car_brand)

        )
        result = await session.execute(stmt)
        result = result.all()
        data = {}
        for res in result:
            if res.vin in data:
                car_data: dict = data[res.vin]
                car_data['periods']: list[dict] = [{'dfrom': res.dfrom,
                                                    'dto': res.dto, "gov_plate": res.full_number} , *car_data['periods']]
            else:
                data[res.vin] = {'periods': [{'dfrom': res.dfrom, 'dto': res.dto, "gov_plate": res.full_number}]}
            cars_data = data[res.vin]
            cars_data['brand'] = res.brand
            cars_data['model'] = res.model


    return data


