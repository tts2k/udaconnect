import logging
from typing import Any, List

from sqlalchemy.dialects.postgresql import insert

from app.models import Location
from app.schemas import LocationSchema
from app.db import db_session
from geoalchemy2.functions import ST_Point

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location_consumer")


class LocationService:
    # @staticmethod
    # def retrieve(location_id) -> Location:
    #     location, coord_text = (
    #         db.session.query(Location, Location.coordinate.ST_AsText())
    #         .filter(Location.id == location_id)
    #         .one()
    #     )
    #
    #     # Rely on database to return text form of point to reduce overhead of conversion in app code
    #     location.wkt_shape = coord_text
    #     return location

    @staticmethod
    def create(locations: List[Any]) -> bool:
        try:
            for location in locations:
                validation_results: Any = LocationSchema().validate(location.value)
                logger.info("something")
                if validation_results:
                    logger.warning(
                        f"Unexpected data format in payload: {validation_results}"
                    )
                    continue
                stmt = insert(Location).values(
                    person_id=location.value["person_id"],
                    coordinate=ST_Point(
                        location.value["latitude"], location.value["longitude"]
                    ),
                )
                stmt = stmt.on_conflict_do_nothing(constraint="location_pkey")
                db_session.execute(stmt)
                logging.info(stmt)
            db_session.commit()
        except Exception as e:
            logger.warning(e)
            db_session.rollback()
            return False

        return True
