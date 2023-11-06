from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp

from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from app.udaconnect.services import LocationService, PersonService
from app.config import CONNECTION_SRV_URL
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List
from app.udaconnect.connection_pb2 import FindContactMessage
from app.udaconnect.connection_pb2_grpc import ConnectionServiceStub, grpc

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

# grpc client initialization
channel = grpc.insecure_channel(CONNECTION_SRV_URL)
client = ConnectionServiceStub(channel)


@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> List[Connection]:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: int = int(request.args.get("distance", 5))

        start_date_ts = Timestamp()
        start_date_ts.FromDatetime(start_date)
        end_date_ts = Timestamp()
        end_date_ts.FromDatetime(end_date)

        grpcRequest = FindContactMessage(
            person_id=int(person_id),
            start_date=start_date_ts,
            end_date=end_date_ts,
            meters=distance,
        )
        connectionResponse = client.FindContacts(grpcRequest)

        results: List[Connection] = []
        for connection in connectionResponse.connections:
            location = Location(
                id=connection.location.id,
                person_id=connection.location.person_id,
                creation_time=connection.location.creation_time.ToDatetime(),
            )
            location.set_wkt_with_coords(
                connection.location.latitude, connection.location.longitude
            )
            person = Person(
                id=connection.person.id,
                first_name=connection.person.first_name,
                last_name=connection.person.last_name,
            )
            results.append(Connection(person=person, location=location))

        return results
