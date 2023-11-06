import logging
from concurrent import futures

import grpc
import connection_pb2_grpc
from services import ConnectionService

logger = logging.getLogger("connection")
logger.setLevel(logging.INFO)

def serve():
    # initialize gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    connection_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionService(), server)

    logger.info("Server is starting on port 5005...")
    server.add_insecure_port("[::]:5005")
    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(grace=5)

if __name__ == "__main__":
    serve()
