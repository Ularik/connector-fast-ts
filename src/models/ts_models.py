import datetime
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, BigInteger, ForeignKey, DATETIME


class Car(Base):
    __tablename__ = 'car'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year: Mapped[str] = mapped_column(String(30), nullable=True)
    arest_pledge: Mapped[list["ArestPledge"]] = relationship("ArestPledge", back_populates='car', uselist=True)


class ArestPledge(Base):
    __tablename__ = 'arest_pledge'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[int] = mapped_column(Integer)
    dfrom: Mapped[datetime.datetime] = mapped_column(DATETIME)
    dto: Mapped[datetime.datetime] = mapped_column(DATETIME, nullable=True)
    car_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('public.car.id'))
    car = relationship("Car", back_populates="arest_pledge")


class CarHistory(Base):
    __tablename__ = 'car_history'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey('public.car.id'))
    car: Mapped["Car"] = relationship('Car')
    gov_unit_id: Mapped[int] = mapped_column("gov_unit", Integer, ForeignKey('public.gov_unit.id'))
    gov_unit = relationship("GovUnit")
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("public.relation_entity.id"))
    car_model_id: Mapped[int] = mapped_column("car_model", ForeignKey('public.ref_car_model.id'))
    car_model: Mapped["RefCarModel"] = relationship("RefCarModel")

    vin: Mapped[str] = mapped_column(String(30))
    dfrom: Mapped[datetime.datetime] = mapped_column(DATETIME)
    dto: Mapped[datetime.datetime] = mapped_column(DATETIME)


class RefCarModel(Base):
    __tablename__ = 'ref_car_model'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    car_brand_id: Mapped[int] = mapped_column("car_brand", Integer, ForeignKey("public.ref_car_brand.id"))
    car_brand: Mapped["RefCarBrand"] = relationship("RefCarBrand")


class RefCarBrand(Base):
    __tablename__ = 'ref_car_brand'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


class GovUnit(Base):
    __tablename__ = 'gov_unit'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class PersonInfo(Base):
    __tablename__ = 'person_info'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    relation_entity: Mapped[list["RelationEntity"]] = relationship("RelationEntity", back_populates="person")
    pin: Mapped[int] = mapped_column(Integer, nullable=True)


class RelationEntity(Base):
    __tablename__ = 'relation_entity'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    person_id: Mapped[int] = mapped_column("person", Integer, ForeignKey("public.person_info.id"))
    person = relationship("PersonInfo")
    car_history = relationship("CarHistory")