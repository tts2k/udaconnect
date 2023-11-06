from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Union

from app import db

from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property


class Person(db.Model):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)


class Location(db.Model):
    __tablename__ = "location"

    id = Column(BigInteger, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.id), nullable=False)
    coordinate = Column(Geometry("POINT"), nullable=False)
    creation_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    _wkt_shape: Union[str, None] = None

    @property
    def wkt_shape(self) -> Union[str, None]:
        # Persist binary form into readable text
        if self._wkt_shape:
            return self._wkt_shape

        shape = to_shape(self.coordinate)
        if shape is None:
            return None
        # normalize WKT returned by to_wkt() from shapely and ST_AsText() from DB
        self._wkt_shape = shape.to_wkt().replace("POINT ", "ST_POINT")
        return self._wkt_shape

    @wkt_shape.setter
    def wkt_shape(self, v: str) -> None:
        self._wkt_shape = v

    def set_wkt_with_coords(self, lat: str, long: str) -> str:
        self._wkt_shape = f"ST_POINT({lat} {long})"
        return self._wkt_shape

    @hybrid_property
    def longitude(self) -> Union[str, None]:
        coord_text = self.wkt_shape
        if coord_text is None:
            return None
        return coord_text[coord_text.find(" ") + 1 : coord_text.find(")")]

    @hybrid_property
    def latitude(self) -> Union[str, None]:
        coord_text = self.wkt_shape
        if coord_text is None:
            return None
        return coord_text[coord_text.find("(") + 1 : coord_text.find(" ")]


@dataclass
class Connection:
    location: Location
    person: Person
