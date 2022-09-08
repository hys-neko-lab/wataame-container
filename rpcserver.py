from concurrent import futures
import grpc
from api import container_pb2_grpc
import container

def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    container_pb2_grpc.add_ContainerServicer_to_server(container.Container(), server)
    server.add_insecure_port('[::]:8082')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run()