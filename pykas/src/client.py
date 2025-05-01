import grpc
from pykas.protos import rpc_pb2_grpc, rpc_pb2

class KaspaRPC:
    def __init__(self, host="127.0.0.1:16110"):
        self.channel = grpc.insecure_channel(host)
        self.stub = rpc_pb2_grpc.RPCStub(self.channel)

    def get_info(self):
        return self.stub.GetInfo(rpc_pb2.GetInfoRequest())

    def get_peers(self):
        return self.stub.GetConnectedPeerInfo(rpc_pb2.GetConnectedPeerInfoRequest())

    def close(self):
        self.channel.close()
