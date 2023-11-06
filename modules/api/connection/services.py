import logging
from datetime import timedelta
from typing import Any, Dict, List, cast

from google.protobuf.timestamp_pb2 import Timestamp

from models import Location, Person
from sqlalchemy.sql import text
from db import Session
import connection_pb2_grpc
import connection_pb2

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("connection")


class ConnectionService(connection_pb2_grpc.ConnectionServiceServicer):
    def FindContacts(self, request: connection_pb2.FindContactMessage, context):
        db_session = Session()
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        locationQuery = db_session.query(Location)
        locationQuery.filter(
            Location.person_id == request.person_id,
            Location.creation_time < request.start_date.ToDatetime(),
            Location.creation_time >= request.end_date.ToDatetime(),
        )
        locations = locationQuery.all()

        # Cache all users in memory for quick lookup
        person_map: Dict[str, Person] = {
            person.id: person for person in db_session.query(Person).all()
        }

        # Prepare arguments for queries
        data: List[Any] = []
        for location in locations:
            data.append(
                {
                    "person_id": request.person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": request.meters,
                    "start_date": request.start_date.ToDatetime().strftime("%Y-%m-%d"),
                    "end_date": (
                        request.end_date.ToDatetime() + timedelta(days=1)
                    ).strftime("%Y-%m-%d"),
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id

        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        result: List[connection_pb2.ConnectionMessage] = []
        for line in tuple(data):
            result_proxy = db_session.execute(query, line)
            for row_proxy in result_proxy:
                (exposed_person_id, location_id, lat, long, exposed_time) = row_proxy
                timestamp = Timestamp()
                timestamp.FromDatetime(exposed_time)

                locationMessasge = connection_pb2.LocationMessage(
                    id = cast(int, location_id),
                    person_id = cast(int, exposed_person_id),
                    latitude=str(lat),
                    longitude=str(long),
                    creation_time=timestamp,
                )

                person = person_map[exposed_person_id]
                personMessage = connection_pb2.PersonMessage(
                    id=person.id,
                    first_name=person.first_name,
                    last_name=person.last_name,
                )

                result.append(
                    connection_pb2.ConnectionMessage(
                        person=personMessage,
                        location=locationMessasge,
                    )
                )
        Session.remove()
        return connection_pb2.ConnectionResponse(connections=result)
