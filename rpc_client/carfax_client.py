import grpc

from config import settings
from rpc_client.base_client import BaseRpcClient, T
from rpc_client.gen.python.carfax.v1 import carfax_pb2, carfax_pb2_grpc

class CarfaxRcpClient(BaseRpcClient[carfax_pb2_grpc.CarfaxServiceStub]):
    def __init__(self):
        super().__init__(server_url=settings.RPC_CARFAX_URL)

    async def __aenter__(self):
        await self.connect()
        return self

    def _create_stub(self, channel: grpc.aio.Channel) -> T:
        return carfax_pb2_grpc.CarfaxServiceStub(channel)

    async def buy_carfax(self, source: str, vin: str, user_external_id: str, success_url:str, cancel_url: str) -> carfax_pb2.BuyCarfaxResponse:
        data = carfax_pb2.BuyCarfaxRequest(source=source, vin=vin, user_external_id=user_external_id, success_url=success_url, cancel_url=cancel_url)
        return await self._execute_request(self.stub.BuyCarfax, data)

    async def get_all_carfaxes_for_user(self, user_external_id: str, source: str) -> carfax_pb2.GetAllCarfaxesForUserResponse:
        data = carfax_pb2.GetAllCarfaxesForUserRequest(user_external_id=user_external_id, source=source)
        return await self._execute_request(self.stub.GetAllCarfaxesForUser, data)

    async def get_carfax_by_vin(self, vin: str, source: str, user_external_id: str) -> carfax_pb2.GetCarfaxByVinResponse:
        data = carfax_pb2.GetCarfaxByVinRequest(vin=vin, source=source, user_external_id=user_external_id)
        return await self._execute_request(self.stub.GetCarfaxByVin, data)

    async def is_vin_exists(self, vin: str) -> carfax_pb2.IsVinExistsResponse:
        data = carfax_pb2.IsVinExistsRequest(vin=vin)
        return await self._execute_request(self.stub.IsVinExists, data)