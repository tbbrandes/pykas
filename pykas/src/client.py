import grpc
import time
from pykas.src.env import NODE_HOST, NODE_PORT, TLS_SECURE
from pykas.src.logger import get_logger
from pykas.proto import rpc_pb2_grpc, rpc_pb2

logger = get_logger(__name__)

class KaspaClient:
    def __init__(self, max_retries=5, retry_delay=2):
        self.host = NODE_HOST
        self.port = NODE_PORT
        self.tls_secure = TLS_SECURE
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self.channel = self._create_channel()
        self.stub = rpc_pb2_grpc.KaspaServiceStub(self.channel)
        self._wait_for_ready_stub()

    def _create_channel(self):
        target = f"{self.host}:{self.port}"
        if self.tls_secure:
            logger.info("Using secure TLS channel")
            credentials = grpc.ssl_channel_credentials()
            return grpc.secure_channel(target, credentials)
        else:
            logger.warning("Using insecure channel")
            return grpc.insecure_channel(target)

    def _wait_for_ready_stub(self):
        logger.info("Attempting to connect to Kaspa node...")
        for attempt in range(1, self.max_retries + 1):
            try:
                grpc.channel_ready_future(self.channel).result(timeout=5)
                logger.info("gRPC connection established.")
                return
            except grpc.FutureTimeoutError:
                logger.warning(f"Attempt {attempt}/{self.max_retries} failed. Retrying in {self.retry_delay}s...")
                time.sleep(self.retry_delay)

        logger.error("Failed to connect to Kaspa node after multiple attempts.")
        raise ConnectionError("Could not establish connection to gRPC server.")

    def get_block(self, block_hash):
        try:
            request = rpc_pb2.GetBlockRequest(hash=block_hash)
            response = self.stub.GetBlock(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"gRPC Error [GetBlock]: {e.code()} - {e.details()}")
            raise

    def get_transaction(self, tx_hash):
        try:
            request = rpc_pb2.GetTransactionsByHashesRequest(hashes=[tx_hash])
            response = self.stub.GetTransactionsByHashes(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"gRPC Error [GetTransaction]: {e.code()} - {e.details()}")
            raise

    def get_balance(self, address):
        try:
            request = rpc_pb2.BalancesByAddressesRequest(addresses=[address])
            response = self.stub.GetBalanceByAddress(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"gRPC Error [GetBalance]: {e.code()} - {e.details()}")
            raise

    def get_virtual_selected_parent_blue_score(self):
        try:
            request = rpc_pb2.GetVirtualSelectedParentBlueScoreRequest()
            response = self.stub.GetVirtualSelectedParentBlueScore(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"gRPC Error [GetVirtualSelectedParentBlueScore]: {e.code()} - {e.details()}")
            raise

    def close(self):
        if self.channel:
            self.channel.close()
            logger.info("gRPC channel closed.")
