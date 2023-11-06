from app.udaconnect.connection_pb2 import FindContactMessage
from app.udaconnect.connection_pb2_grpc import ConnectionServiceStub, grpc
from app.config import CONNECTION_SRV_URL

channel = grpc.insecure_channel(CONNECTION_SRV_URL)
client = ConnectionServiceStub(channel)

grpcRequest = FindContactMessage(
    person_id=1,
    end_date={"seconds": 1609261200 },
    start_date={"seconds": 1577811600 },
    meters=5,
)
connectionResponse = client.FindContacts(grpcRequest)
