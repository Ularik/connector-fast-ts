from pydantic import BaseModel


class GetCarsSchema(BaseModel):
    subject: dict[str, str]
    requested_groups: list[str]
    paging: dict[str, int]