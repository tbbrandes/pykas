import unittest
from unittest.mock import patch, MagicMock
from pykas.src.client import KaspaClient

@patch("pykas.src.client.grpc.secure_channel")  # mock channel constructor
@patch("pykas.src.client.rpc_pb2_grpc.KaspaServiceStub")  # mock stub class
class TestKaspaClient(unittest.TestCase):

    def setUp(self):
        self.fake_response = MagicMock()

    def test_get_virtual_selected_parent_blue_score(self, mock_stub_class, mock_channel):
        mock_stub = MagicMock()
        mock_stub.GetVirtualSelectedParentBlueScore.return_value = self.fake_response
        mock_stub_class.return_value = mock_stub

        client = KaspaClient()
        result = client.get_virtual_selected_parent_blue_score()
        self.assertEqual(result, self.fake_response)
        client.close()

    def test_get_block(self, mock_stub_class, mock_channel):
        mock_stub = MagicMock()
        mock_stub.GetBlock.return_value = self.fake_response
        mock_stub_class.return_value = mock_stub

        client = KaspaClient()
        result = client.get_block("abc123")
        self.assertEqual(result, self.fake_response)
        client.close()

    def test_get_transaction(self, mock_stub_class, mock_channel):
        mock_stub = MagicMock()
        mock_stub.GetTransactionsByHashes.return_value = self.fake_response
        mock_stub_class.return_value = mock_stub

        client = KaspaClient()
        result = client.get_transaction("tx456")
        self.assertEqual(result, self.fake_response)
        client.close()

    def test_get_balance(self, mock_stub_class, mock_channel):
        mock_stub = MagicMock()
        mock_stub.GetBalanceByAddress.return_value = self.fake_response
        mock_stub_class.return_value = mock_stub

        client = KaspaClient()
        result = client.get_balance("kaspa:abc")
        self.assertEqual(result, self.fake_response)
        client.close()
