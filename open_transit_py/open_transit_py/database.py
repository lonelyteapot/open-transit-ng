from uuid import UUID
from open_transit_py.util import PlaceholderError
import sqlalchemy
import sqlalchemy.exc
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


def make_engine(url):
    try:
        return sqlalchemy.create_engine(url)
    except sqlalchemy.exc.SQLAlchemyError as exc:
        raise PlaceholderError("Failed to create db engine", exc)


def check_connection(engine) -> bool:
    try:
        with engine.connect():
            pass
    except sqlalchemy.exc.DatabaseError as exc:
        raise PlaceholderError("Failed to connect to the database", exc)
    return True


class Base(DeclarativeBase):
    pass


class Network(Base):
    __tablename__ = "network"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))


class Route(Base):
    __tablename__ = "route"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))
    network_id: Mapped[UUID] = mapped_column(ForeignKey("network.id"))
