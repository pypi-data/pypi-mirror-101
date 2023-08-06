import os
from unittest import mock

from django.conf import settings
from django.test import TestCase
from swapper import load_model

from .utils import CreateConnectionsMixin, SshServer

Config = load_model('config', 'Config')
Device = load_model('config', 'Device')
Credentials = load_model('connection', 'Credentials')
DeviceConnection = load_model('connection', 'DeviceConnection')


class TestSsh(CreateConnectionsMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mock_ssh_server = SshServer(
            {'root': cls._TEST_RSA_PRIVATE_KEY_PATH}
        ).__enter__()
        cls.ssh_server.port = cls.mock_ssh_server.port

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.mock_ssh_server.__exit__()

    def test_connection_connect(self):
        ckey = self._create_credentials_with_key(port=self.ssh_server.port)
        dc = self._create_device_connection(credentials=ckey)
        dc.connect()
        self.assertTrue(dc.is_working)
        with mock.patch('logging.Logger.info') as mocked_logger:
            dc.connector_instance.exec_command('echo test')
            mocked_logger.assert_has_calls(
                [mock.call('Executing command: echo test'), mock.call('test\n')]
            )

    def test_connection_failed_command(self):
        ckey = self._create_credentials_with_key(port=self.ssh_server.port)
        dc = self._create_device_connection(credentials=ckey)
        dc.connector_instance.connect()
        with self.assertRaises(Exception):
            with mock.patch('logging.Logger.error') as mocked_logger:
                dc.connector_instance.exec_command('wrongcommand')
                mocked_logger.assert_has_calls(
                    [
                        mock.call('/bin/sh: 1: wrongcommand: not found'),
                        mock.call('Unexpected exit code: 127'),
                    ]
                )

    @mock.patch('scp.SCPClient.putfo')
    def test_connection_upload(self, putfo_mocked):
        ckey = self._create_credentials_with_key(port=self.ssh_server.port)
        dc = self._create_device_connection(credentials=ckey)
        dc.connector_instance.connect()
        # needs a binary file to test all lines
        fl = open(os.path.join(settings.BASE_DIR, '../media/floorplan.jpg'), 'rb')
        dc.connector_instance.upload(fl, '/tmp/test')
        putfo_mocked.assert_called_once()
