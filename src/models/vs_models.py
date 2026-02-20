import datetime

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, BigInteger, ForeignKey, DATETIME, Boolean, BINARY


class Person(Base):
    __tablename__ = 'person'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    dob: Mapped[datetime.datetime] = mapped_column(DATETIME, nullable=True)
    first_name_cyr: Mapped[str] = mapped_column(String(255), nullable=True)
    first_name_lat: Mapped[str] = mapped_column(String(255), nullable=True)
    gender: Mapped[int] = mapped_column(Integer, nullable=True)
    last_name_cyr: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name_lat: Mapped[str] = mapped_column(String(255), nullable=True)
    middle_name_cyr: Mapped[str] = mapped_column(String(255), nullable=True)
    middle_name_lat: Mapped[str] = mapped_column(String(255), nullable=True)
    pin: Mapped[str] = mapped_column(String(255), nullable=True)

    # relations
    statement: Mapped[list["Statement"]] = relationship("Statement")


class Statement(Base):
    __tablename__ = 'statement'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    categories_1: Mapped[str] = mapped_column(String(255), nullable=True)
    categories_2: Mapped[str] = mapped_column(String(255), nullable=True)
    date_created: Mapped[datetime.datetime] = mapped_column(DATETIME, nullable=True)
    # address_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("public."))
    person_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("public.person.id"))
    address_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("public.address.id"))
    address: Mapped["Address"] = relationship("Address")
    cards: Mapped[list["Cards"]] = relationship("Cards")


class Cards(Base):
    __tablename__ = 'cards'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(50))
    photo: Mapped[bytes] = mapped_column(BINARY, nullable=True)
    date_issue: Mapped[datetime.datetime] = mapped_column(DATETIME, nullable=True)
    date_expire: Mapped[datetime.datetime] = mapped_column(DATETIME, nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=True)
    type: Mapped[str] = mapped_column(String(255), nullable=True)
    statement_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("public.statement.id"))
    issue_country_id: Mapped[int] = mapped_column(Integer, ForeignKey("public.country.id"))
    # last_deprivation_id


class Address(Base):
    __tablename__ = 'address'
    __table_args__ = {
        'schema': 'public',
        'extend_existing': True
    }

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    print_cyr: Mapped[str] = mapped_column(String(255), nullable=True)
    print_lat: Mapped[str] = mapped_column(String(255), nullable=True)
