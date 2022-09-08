from api import container_pb2
from api import container_pb2_grpc
import docker

class Container(container_pb2_grpc.ContainerServicer):
    def __init__(self):
        self.client = docker.from_env()

    def create(self, request, context):
        # wataame-networkで作成済みのDockerネットワークを取得
        docknet = self.client.networks.get(request.docknetid)
        
        # コマンドなし/デタッチモードでコンテナ実行
        cont = self.client.containers.run(
            request.image,
            '',
            detach=True,
            network=docknet.name,
            name=request.name
        )
        message = cont.id
        return container_pb2.CreateReply(message=message)

    def start(self, request, context):
        cont = self.client.containers.get(request.id)
        cont.start()
        message = "ID:" + request.id + " started."
        return container_pb2.StartReply(message=message)

    def stop(self, request, context):
        cont = self.client.containers.get(request.id)
        cont.stop()
        message = "ID:" + request.id + " stopped."
        return container_pb2.StopReply(message=message)

    def delete(self, request, context):
        cont = self.client.containers.get(request.id)
        cont.remove()
        message = "ID:" + request.id + " deleted."
        return container_pb2.DeleteReply(message=message)

    def getStatus(self, request, context):
        cont = self.client.containers.get(request.id)
        status = cont.status
        return container_pb2.StatusReply(message=status)

    def getIP(self, request, context):
        cont = self.client.containers.get(request.id)
        docknet = self.client.networks.get(request.docknetid)
        ip = cont.attrs['NetworkSettings']['Networks'][str(docknet.name)]['IPAddress']
        return container_pb2.IPReply(message=ip)