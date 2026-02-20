from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime
import base64


class CardsSchema(BaseModel):
    id: int
    number: str
    photo: bytes | None
    date_issue: datetime | None
    date_expire: datetime | None
    status: str | None
    type: str | None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("photo")
    def serialize_photo(self, value: bytes | None) -> str | None:
        if value is None:
            return None
        return base64.b64encode(value).decode("ascii")


class StatementSchema(BaseModel):
    id: int
    categories_1: str | None
    categories_2: str | None
    date_created: datetime | None
    address: "AddressSchema"

    model_config = ConfigDict(from_attributes=True)


class AddressSchema(BaseModel):
    print_cyr: str
    print_lat: str

    model_config = ConfigDict(from_attributes=True)


class PersonSchema(BaseModel):
    id: int
    dob: datetime | None
    first_name_cyr: str | None
    first_name_lat: str | None
    last_name_cyr: str | None
    last_name_lat: str | None
    middle_name_cyr: str | None
    middle_name_lat: str | None
    gender: int | None
    pin: str | None

    model_config = ConfigDict(from_attributes=True)