import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Location, Person
from app.udaconnect.schemas import LocationSchema 
from geoalchemy2.functions import ST_Point

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        session = db.session()
        location, coord_text = (
            session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        session = db.session()
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        session.add(new_location)
        session.commit()

        return new_location


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        session = db.session()
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        session.add(new_person)
        session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        session = db.session()
        person = session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        session = db.session()
        return session.query(Person).all()
