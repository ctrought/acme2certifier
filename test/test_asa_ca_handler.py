#!/usr/bin/python
# -*- coding: utf-8 -*-
""" unittests for openssl_ca_handler """
# pylint: disable=C0415, R0904, W0212
import sys
import os
import unittest
from unittest.mock import patch, Mock
import requests
import base64

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class TestACMEHandler(unittest.TestCase):
    """ test class for cgi_handler """

    def setUp(self):
        """ setup unittest """
        import logging
        from examples.ca_handler.asa_ca_handler import CAhandler
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_a2c')
        self.cahandler = CAhandler(False, self.logger)
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.maxDiff = None

    def test_001_default(self):
        """ default test which always passes """
        self.assertEqual('foo', 'foo')

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._config_load')
    def test_055__enter__(self, mock_cfg):
        """ test enter  called """
        mock_cfg.return_value = True
        self.cahandler.__enter__()
        self.assertTrue(mock_cfg.called)

    def test_038_poll(self):
        """ test polling """
        self.assertEqual(('Method not implemented.', None, None, 'poll_identifier', False), self.cahandler.poll('cert_name', 'poll_identifier', 'csr'))

    def test_039_trigger(self):
        """ test polling """
        self.assertEqual(('Method not implemented.', None, None), self.cahandler.trigger('payload'))


    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_002_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'CAhandler': {'api_host': 'api_host'}}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_load()
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_user not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_password not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_key not set', lcm.output)
        self.assertEqual('api_host', self.cahandler.api_host)
        self.assertFalse(self.cahandler.api_user)
        self.assertFalse(self.cahandler.api_password)
        self.assertFalse(self.cahandler.api_key)
        self.assertFalse(self.cahandler.ca_bundle)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(10, self.cahandler.request_timeout)
        self.assertEqual(30, self.cahandler.cert_validity_days)

    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_003_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'CAhandler': {'api_user': 'api_user'}}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_load()
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_host not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_password not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_key not set', lcm.output)
        self.assertFalse(self.cahandler.api_host)
        self.assertEqual('api_user', self.cahandler.api_user)
        self.assertFalse(self.cahandler.api_password)
        self.assertFalse(self.cahandler.api_key)
        self.assertFalse(self.cahandler.ca_bundle)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(10, self.cahandler.request_timeout)
        self.assertEqual(30, self.cahandler.cert_validity_days)

    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_004_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'CAhandler': {'api_password': 'api_password'}}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_load()
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_host not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_user not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_key not set', lcm.output)
        self.assertFalse(self.cahandler.api_host)
        self.assertFalse(self.cahandler.api_user)
        self.assertEqual('api_password', self.cahandler.api_password)
        self.assertFalse(self.cahandler.api_key)
        self.assertFalse(self.cahandler.ca_bundle)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(10, self.cahandler.request_timeout)
        self.assertEqual(30, self.cahandler.cert_validity_days)

    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_005_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'CAhandler': {'api_key': 'api_key'}}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_load()
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_host not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_user not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_password not set', lcm.output)
        self.assertFalse(self.cahandler.api_host)
        self.assertFalse(self.cahandler.api_user)
        self.assertFalse(self.cahandler.api_password)
        self.assertEqual('api_key', self.cahandler.api_key)
        self.assertFalse(self.cahandler.ca_bundle)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(10, self.cahandler.request_timeout)
        self.assertEqual(30, self.cahandler.cert_validity_days)

    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_006_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'CAhandler': {'api_host': 'api_host', 'api_user': 'api_user', 'api_password': 'api_password', 'api_key': 'api_key'}}
        self.cahandler._config_load()
        self.assertEqual('api_host', self.cahandler.api_host)
        self.assertEqual('api_user', self.cahandler.api_user)
        self.assertEqual('api_password', self.cahandler.api_password)
        self.assertEqual('api_key', self.cahandler.api_key)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(10, self.cahandler.request_timeout)
        self.assertEqual(30, self.cahandler.cert_validity_days)

    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_007_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'foo': 'bar'}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_load()
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_host not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_user not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_password not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_key not set', lcm.output)
        self.assertFalse(self.cahandler.api_host)
        self.assertFalse(self.cahandler.api_user)
        self.assertFalse(self.cahandler.api_password)
        self.assertFalse(self.cahandler.api_key)
        self.assertFalse(self.cahandler.ca_bundle)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(10, self.cahandler.request_timeout)
        self.assertEqual(30, self.cahandler.cert_validity_days)

    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_008_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'CAhandler': {'request_timeout': 20}}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_load()
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_host not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_user not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_key not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_password not set', lcm.output)
        self.assertFalse(self.cahandler.api_host)
        self.assertFalse(self.cahandler.api_user)
        self.assertFalse(self.cahandler.api_password)
        self.assertFalse(self.cahandler.api_key)
        self.assertFalse(self.cahandler.ca_bundle)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(20, self.cahandler.request_timeout)
        self.assertEqual(30, self.cahandler.cert_validity_days)

    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_008_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'CAhandler': {'request_timeout': 'aa'}}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_load()
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_host not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_user not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_key not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_password not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): request_timeout not an integer', lcm.output)
        self.assertFalse(self.cahandler.api_host)
        self.assertFalse(self.cahandler.api_user)
        self.assertFalse(self.cahandler.api_password)
        self.assertFalse(self.cahandler.api_key)
        self.assertFalse(self.cahandler.ca_bundle)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(10, self.cahandler.request_timeout)
        self.assertEqual(30, self.cahandler.cert_validity_days)

    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_009_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'CAhandler': {'cert_validity_days': 10}}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_load()
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_host not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_user not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_key not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_password not set', lcm.output)
        # self.assertIn('ERROR:test_a2c:CAhandler._config_load(): request_timeout not an integer', lcm.output)
        self.assertFalse(self.cahandler.api_host)
        self.assertFalse(self.cahandler.api_user)
        self.assertFalse(self.cahandler.api_password)
        self.assertFalse(self.cahandler.api_key)
        self.assertFalse(self.cahandler.ca_bundle)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(10, self.cahandler.request_timeout)
        self.assertEqual(10, self.cahandler.cert_validity_days)

    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_010_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'CAhandler': {'cert_validity_days': 'aa'}}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_load()
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_host not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_user not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_key not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_password not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): cert_validity_days not an integer', lcm.output)
        self.assertFalse(self.cahandler.api_host)
        self.assertFalse(self.cahandler.api_user)
        self.assertFalse(self.cahandler.api_password)
        self.assertFalse(self.cahandler.api_key)
        self.assertFalse(self.cahandler.ca_bundle)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(10, self.cahandler.request_timeout)
        self.assertEqual(30, self.cahandler.cert_validity_days)

    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_011_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'CAhandler': {'ca_bundle': 'aa'}}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_load()
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_host not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_user not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_key not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_password not set', lcm.output)
        self.assertFalse(self.cahandler.api_host)
        self.assertFalse(self.cahandler.api_user)
        self.assertFalse(self.cahandler.api_password)
        self.assertFalse(self.cahandler.api_key)
        self.assertEqual('aa', self.cahandler.ca_bundle)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(10, self.cahandler.request_timeout)
        self.assertEqual(30, self.cahandler.cert_validity_days)

    @patch('examples.ca_handler.asa_ca_handler.load_config')
    def test_012_config_load(self, mock_config_load):
        """ test _config_load """
        mock_config_load.return_value = {'CAhandler': {'ca_bundle': 'False'}}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.cahandler._config_load()
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_host not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_user not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_key not set', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._config_load(): api_password not set', lcm.output)
        self.assertFalse(self.cahandler.api_host)
        self.assertFalse(self.cahandler.api_user)
        self.assertFalse(self.cahandler.api_password)
        self.assertFalse(self.cahandler.api_key)
        self.assertFalse(self.cahandler.ca_bundle)
        self.assertFalse(self.cahandler.proxy)
        self.assertEqual(10, self.cahandler.request_timeout)
        self.assertEqual(30, self.cahandler.cert_validity_days)

    @patch.object(requests, 'post')
    def test_013__api_post(self, mock_req):
        """ test _api_post() """
        mockresponse = Mock()
        mockresponse.status_code = 'status_code'
        mockresponse.json = lambda: {'foo': 'bar'}
        mock_req.return_value = mockresponse
        self.assertEqual(('status_code', {'foo': 'bar'}), self.cahandler._api_post('url', 'data'))

    @patch('requests.post')
    def test_014__api_post(self, mock_req):
        """ test _api_post() """
        mockresponse = Mock()
        mockresponse.status_code = 'status_code'
        mockresponse.json = "aaaa"
        mock_req.return_value = mockresponse
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual(('status_code', "'str' object is not callable"), self.cahandler._api_post('url', 'data'))
        self.assertIn("ERROR:test_a2c:CAhandler._api_post() returned error: 'str' object is not callable", lcm.output)

    @patch('requests.post')
    def test_15__api_post(self, mock_req):
        """ test _api_post(= """
        self.cahandler.api_host = 'api_host'
        self.cahandler.auth = 'auth'
        mock_req.side_effect = Exception('exc_api_post')
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual((500, 'exc_api_post'), self.cahandler._api_post('url', 'data'))
        self.assertIn('ERROR:test_a2c:CAhandler._api_post() returned error: exc_api_post', lcm.output)

    @patch.object(requests, 'get')
    def test_016__api_get(self, mock_req):
        """ test _api_get() """
        mockresponse = Mock()
        mockresponse.status_code = 'status_code'
        mockresponse.json = lambda: {'foo': 'bar'}
        mock_req.return_value = mockresponse
        self.assertEqual(('status_code', {'foo': 'bar'}), self.cahandler._api_get('url'))

    @patch('requests.get')
    def test_018__api_get(self, mock_req):
        """ test _api_get() """
        mockresponse = Mock()
        mockresponse.status_code = 'status_code'
        mockresponse.json = "aaaa"
        mock_req.return_value = mockresponse
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual(('status_code', "'str' object is not callable"), self.cahandler._api_get('url'))
        self.assertIn("ERROR:test_a2c:CAhandler._api_get() returned error: 'str' object is not callable", lcm.output)

    @patch('requests.get')
    def test_019__api_get(self, mock_req):
        """ test _api_get() """
        self.cahandler.api_host = 'api_host'
        self.cahandler.auth = 'auth'
        mock_req.side_effect = Exception('exc_api_get')
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual((500, 'exc_api_get'), self.cahandler._api_get('url'))
        self.assertIn('ERROR:test_a2c:CAhandler._api_post() returned error: exc_api_get', lcm.output)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_get')
    def test_020__issuers_list(self, mock_get):
        """ test _issuers_list()"""
        mock_get.return_value = (200, 'content')
        self.assertEqual('content', self.cahandler._issuers_list())

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_get')
    def test_021__profiles_list(self, mock_get):
        """ test _profiles_list()"""
        self.cahandler.ca_name = 'ca_name'
        mock_get.return_value = (200, 'content')
        self.assertEqual('content', self.cahandler._profiles_list())

    @patch('examples.ca_handler.asa_ca_handler.csr_san_get')
    @patch('examples.ca_handler.asa_ca_handler.csr_cn_get')
    def test_022__csr_cn_get(self, mock_cn, mock_san):
        """ test _csr_cn_get() """
        mock_cn.return_value = 'cn'
        mock_san.return_value = ['san0', 'san1']
        self.assertEqual('cn', self.cahandler._csr_cn_get('csr'))
        self.assertFalse(mock_san.called)

    @patch('examples.ca_handler.asa_ca_handler.csr_san_get')
    @patch('examples.ca_handler.asa_ca_handler.csr_cn_get')
    def test_023__csr_cn_get(self, mock_cn, mock_san):
        """ test _csr_cn_get() """
        mock_cn.return_value = None
        mock_san.return_value = ['dns:san0', 'dns:san1']
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual('san0', self.cahandler._csr_cn_get('csr'))
        self.assertIn('INFO:test_a2c:CAhandler._csr_cn_get(): CN not found in CSR', lcm.output)
        self.assertIn('INFO:test_a2c:CAhandler._csr_cn_get(): CN not found in CSR. Using first SAN entry as CN: san0', lcm.output)
        self.assertTrue(mock_san.called)

    @patch('examples.ca_handler.asa_ca_handler.csr_san_get')
    @patch('examples.ca_handler.asa_ca_handler.csr_cn_get')
    def test_024__csr_cn_get(self, mock_cn, mock_san):
        """ test _csr_cn_get() """
        mock_cn.return_value = None
        mock_san.return_value = None
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual(None, self.cahandler._csr_cn_get('csr'))
        self.assertIn('INFO:test_a2c:CAhandler._csr_cn_get(): CN not found in CSR', lcm.output)
        self.assertIn('ERROR:test_a2c:CAhandler._csr_cn_get(): CN not found in CSR. No SAN entries found', lcm.output)
        self.assertTrue(mock_san.called)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuers_list')
    def test_025_issuer_verify(self, mock_list):
        """ _issuer_verify() """
        self.cahandler.ca_name = 'ca_name'
        mock_list.return_value = {'issuers': ['1', '2', 'ca_name']}
        self.assertFalse(self.cahandler._issuer_verify())

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuers_list')
    def test_026_issuer_verify(self, mock_list):
        """ _issuer_verify() """
        self.cahandler.ca_name = 'ca_name'
        mock_list.return_value = {'issuers': ['1', '2', '3']}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual('CA ca_name not found', self.cahandler._issuer_verify())
        self.assertIn('ERROR:test_a2c:CAhandler.enroll(): CA ca_name not found', lcm.output)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuers_list')
    def test_027_issuer_verify(self, mock_list):
        """ _issuer_verify() """
        self.cahandler.ca_name = 'ca_name'
        mock_list.return_value = {'foo': 'bar'}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual('Malformed response', self.cahandler._issuer_verify())
        self.assertIn('ERROR:test_a2c:CAhandler.enroll(): "Malformed response. "issuers" key not found', lcm.output)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._profiles_list')
    def test_025_profile_verify(self, mock_list):
        """ _profile_verify() """
        self.cahandler.profile_name = 'profile_name'
        mock_list.return_value = {'profiles': ['1', '2', 'profile_name']}
        self.assertFalse(self.cahandler._profile_verify())

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._profiles_list')
    def test_026_profile_verify(self, mock_list):
        """ _profile_verify() """
        self.cahandler.profile_name = 'profile_name'
        mock_list.return_value = {'profiles': ['1', '2', '3']}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual('Profile profile_name not found', self.cahandler._profile_verify())
        self.assertIn('ERROR:test_a2c:CAhandler.enroll(): Profile profile_name not found', lcm.output)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._profiles_list')
    def test_027_profile_verify(self, mock_list):
        """ _profile_verify() """
        self.cahandler.ca_name = 'ca_name'
        mock_list.return_value = {'foo': 'bar'}
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual('Malformed response', self.cahandler._profile_verify())
        self.assertIn('ERROR:test_a2c:CAhandler.enroll(): "Malformed response. "profiles" key not found', lcm.output)

    @patch('examples.ca_handler.asa_ca_handler.uts_to_date_utc')
    @patch('examples.ca_handler.asa_ca_handler.uts_now')
    def test_028__validity_dates_get(self, mock_now, mock_utc):
        """ test _validity_dates_get() """
        mock_now.return_value = 10
        mock_utc.side_effect = ['date1', 'date2']
        self.assertEqual(('date1', 'date2'), self.cahandler._validity_dates_get())
        self.assertTrue(mock_now.called)

    @patch('examples.ca_handler.asa_ca_handler.convert_byte_to_string')
    @patch('examples.ca_handler.asa_ca_handler.cert_der2pem')
    @patch('examples.ca_handler.asa_ca_handler.b64_decode')
    def test_029__pem_cert_chain_generate(self, mock_dec, mock_d2p, mock_b2s):
        """ test _pem_cert_chain_generate() """
        mock_b2s.return_value = 'cert'
        self.assertEqual('certcert', self.cahandler._pem_cert_chain_generate(['cert', 'chain']))

    def test_030__pem_cert_chain_generate(self):
        """ test _pem_cert_chain_generate() """
        cert_list = ['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']
        result = """-----BEGIN CERTIFICATE-----
MIIF7DCCBFSgAwIBAgIKB/8cQ9wAI3UbITANBgkqhkiG9w0BAQsFADBaMQswCQYD
VQQGEwJERTERMA8GA1UECgwIT3BlblhQS0kxDDAKBgNVBAsMA1BLSTEqMCgGA1UE
AwwhT3BlblhQS0kgRGVtbyBJc3N1aW5nIENBIDIwMjMwMjA0MB4XDTIzMDIwNTA2
NDY0MloXDTI0MDIwNTA2NDY0MlowazETMBEGCgmSJomT8ixkARkWA29yZzEYMBYG
CgmSJomT8ixkARkWCE9wZW5YUEtJMR8wHQYKCZImiZPyLGQBGRYPVGVzdCBEZXBs
b3ltZW50MRkwFwYDVQQDDBBhY21lMS5keW5hbW9wLmRlMIIBIjANBgkqhkiG9w0B
AQEFAAOCAQ8AMIIBCgKCAQEAre1jtb8Xjqr49QH3fWe2kH+yDk3NXfxHyOmKcNcB
ke68WMRB5Irrdj15JfAsXxu9psLVEOJgvdOLOnUbhN57uBLHwMAC1LH6HruYuCqt
baSezgJIYIEACvtQmIy6BIvigqwX31eLkA7kk7YXeJCnvrr461t/uZkhmaXZM9+G
4asSj6fT0ffA7OVVqewDdE+d2VgCjPlH9uqPMOVK2m/AQj+jEVV/IV2znngZmkAs
mYi6h2Wg08vEzTMyvhZIEma3xo6M9g9VIsTQP/ETxxhAAgzEQ0Jlz90rOioZK7mk
x8xH1fLlhyfX53vqcEbva5evy1YMGEs0XZPYu2B6Oya9WQIDAQABo4ICITCCAh0w
gYcGCCsGAQUFBwEBBHsweTBRBggrBgEFBQcwAoZFaHR0cDovL3BraS5leGFtcGxl
LmNvbS9kb3dubG9hZC9PcGVuWFBLSV9EZW1vX0lzc3VpbmdfQ0FfMjAyMzAyMDQu
Y2VyMCQGCCsGAQUFBzABhhhodHRwOi8vb2NzcC5leGFtcGxlLmNvbS8wHwYDVR0j
BBgwFoAU0f8PWcniVXltJeA6q7wYtyJrNFAwDAYDVR0TAQH/BAIwADBWBgNVHR8E
TzBNMEugSaBHhkVodHRwOi8vcGtpLmV4YW1wbGUuY29tL2Rvd25sb2FkL09wZW5Y
UEtJX0RlbW9fSXNzdWluZ19DQV8yMDIzMDIwNC5jcmwwEwYDVR0lBAwwCgYIKwYB
BQUHAwEwDgYDVR0PAQH/BAQDAgWgMIGoBgNVHSAEgaAwgZ0wgZoGAyoDBDCBkjAr
BggrBgEFBQcCARYfaHR0cDovL3BraS5leGFtcGxlLmNvbS9jcHMuaHRtbDArBggr
BgEFBQcCARYfaHR0cDovL3BraS5leGFtcGxlLmNvbS9jcHMuaHRtbDA2BggrBgEF
BQcCAjAqGihUaGlzIGlzIGEgY29tbWVudCBmb3IgcG9saWN5IG9pZCAxLjIuMy40
MBsGA1UdEQQUMBKCEGFjbWUxLmR5bmFtb3AuZGUwHQYDVR0OBBYEFA3AUTV0pg0f
sd3Cd6/BskOEB9MVMA0GCSqGSIb3DQEBCwUAA4IBgQB0xnnl6BJDXrbTQr7TdkRP
mcCDFUmi8aVTYozbQ8EKxIYEPsfzxOFbSG/wn+4Sjz7HqvzqxyisfTopqWrvpqIh
lXOEFMnNYTDO4LzCd81Dcs4czjoIRxRTisgNCvWR9hbeH9HzdRT1UF/c4VxxLEON
SsGHksoXa+G4u7XmPwD4dTUIP49Mmj2a28z/viG8KftcjAEo1S7OB+/xyPeVDYrg
agMR31a69pI+yuQa0J66O/LJQrzjWf6wHToQErQPcEBtDxY2wx3hROMtdla9lUEU
8XLb3e9zByZwOfDhFpw8iYkJx/BUZlsmIKaZSpYVS+0D5LI1R5PENhT/2gRxaA31
RiNLK/E8CSU7MMadqImkFLkDHU2x+2SRENwvoOEUAOewjVlhB1pK0r5WEye2lBjl
8cUa+8qhIrAOqggApQ7eCQq7v2bL08VxKz5baOhKfLZ9u4MH6q52pnqXmll0W7JX
rJSbam5r3YoSelm94VwVyaSkfd+LT4YMAP7GDDvtT6Y=
-----END CERTIFICATE-----
"""
        self.assertEqual(result, self.cahandler._pem_cert_chain_generate(cert_list))

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._pem_cert_chain_generate')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_get')
    def test_031___issuer_chain_get(self, mock_req, mock_pem):
        """ test _issuer_chain_get() """
        mock_req.return_value = ('code', {'certs': ['bar', 'foo']})
        mock_pem.return_value = 'issuer_chain'
        self.cahandler.ca_name = 'ca_name'
        self.assertEqual('issuer_chain', self.cahandler._issuer_chain_get())
        self.assertTrue(mock_pem.called)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._pem_cert_chain_generate')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_get')
    def test_032___issuer_chain_get(self, mock_req, mock_pem):
        """ test _issuer_chain_get() """
        mock_req.return_value = ('code', {'foobar': ['bar', 'foo']})
        mock_pem.return_value = 'issuer_chain'
        self.cahandler.ca_name = 'ca_name'
        self.assertFalse(self.cahandler._issuer_chain_get())
        self.assertFalse(mock_pem.called)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_post')
    @patch('examples.ca_handler.asa_ca_handler.convert_byte_to_string')
    @patch('examples.ca_handler.asa_ca_handler.cert_der2pem')
    @patch('examples.ca_handler.asa_ca_handler.b64_decode')
    @patch('examples.ca_handler.asa_ca_handler.csr_san_byte_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._validity_dates_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._csr_cn_get')
    @patch('examples.ca_handler.asa_ca_handler.csr_pubkey_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuer_chain_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._profile_verify')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuer_verify')
    def test_033_enroll(self, mock_iv, mock_pv, mock_icg, mock_cpg, mockccg, mock_vdg, mock_csbg, mock_b64, mock_d2p, mock_b2s, mock_post):
        """ test enroll() """
        mock_iv.return_value = None
        mock_pv.return_value = None
        mock_icg.return_value = 'issuer_chain'
        mock_vdg.return_value = ('date1', 'date2')
        mock_post.return_value = (200, 'cert')
        mock_b2s.return_value = 'bcert'
        self.assertEqual((None, 'bcertissuer_chain', 'cert', None), self.cahandler.enroll('csr'))
        self.assertTrue(mock_iv.called)
        self.assertTrue(mock_pv.called)
        self.assertTrue(mock_icg.called)
        self.assertTrue(mock_cpg.called)
        self.assertTrue(mockccg.called)
        self.assertTrue(mock_vdg.called)
        self.assertTrue(mock_csbg.called)
        self.assertTrue(mock_b64.called)
        self.assertTrue(mock_post.called)
        self.assertTrue(mock_b2s.called)
        self.assertTrue(mock_d2p.called)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_post')
    @patch('examples.ca_handler.asa_ca_handler.convert_byte_to_string')
    @patch('examples.ca_handler.asa_ca_handler.cert_der2pem')
    @patch('examples.ca_handler.asa_ca_handler.b64_decode')
    @patch('examples.ca_handler.asa_ca_handler.csr_san_byte_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._validity_dates_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._csr_cn_get')
    @patch('examples.ca_handler.asa_ca_handler.csr_pubkey_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuer_chain_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._profile_verify')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuer_verify')
    def test_034_enroll(self, mock_iv, mock_pv, mock_icg, mock_cpg, mockccg, mock_vdg, mock_csbg, mock_b64, mock_d2p, mock_b2s, mock_post):
        """ test enroll() """
        mock_iv.return_value = 'mock_iv'
        mock_pv.return_value = None
        mock_icg.return_value = 'issuer_chain'
        mock_vdg.return_value = ('date1', 'date2')
        mock_post.return_value = ('code', 'cert')
        mock_b2s.return_value = 'bcert'
        self.assertEqual(('mock_iv', None, None, None), self.cahandler.enroll('csr'))
        self.assertTrue(mock_iv.called)
        self.assertFalse(mock_pv.called)
        self.assertFalse(mock_icg.called)
        self.assertFalse(mock_cpg.called)
        self.assertFalse(mockccg.called)
        self.assertFalse(mock_vdg.called)
        self.assertFalse(mock_csbg.called)
        self.assertFalse(mock_b64.called)
        self.assertFalse(mock_post.called)
        self.assertFalse(mock_b2s.called)
        self.assertFalse(mock_d2p.called)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_post')
    @patch('examples.ca_handler.asa_ca_handler.convert_byte_to_string')
    @patch('examples.ca_handler.asa_ca_handler.cert_der2pem')
    @patch('examples.ca_handler.asa_ca_handler.b64_decode')
    @patch('examples.ca_handler.asa_ca_handler.csr_san_byte_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._validity_dates_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._csr_cn_get')
    @patch('examples.ca_handler.asa_ca_handler.csr_pubkey_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuer_chain_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._profile_verify')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuer_verify')
    def test_035_enroll(self, mock_iv, mock_pv, mock_icg, mock_cpg, mockccg, mock_vdg, mock_csbg, mock_b64, mock_d2p, mock_b2s, mock_post):
        """ test enroll() """
        mock_iv.return_value = None
        mock_pv.return_value = 'mock_pv'
        mock_icg.return_value = 'issuer_chain'
        mock_vdg.return_value = ('date1', 'date2')
        mock_post.return_value = ('code', 'cert')
        mock_b2s.return_value = 'bcert'
        self.assertEqual(('mock_pv', None, None, None), self.cahandler.enroll('csr'))
        self.assertTrue(mock_iv.called)
        self.assertTrue(mock_pv.called)
        self.assertFalse(mock_icg.called)
        self.assertFalse(mock_cpg.called)
        self.assertFalse(mockccg.called)
        self.assertFalse(mock_vdg.called)
        self.assertFalse(mock_csbg.called)
        self.assertFalse(mock_b64.called)
        self.assertFalse(mock_post.called)
        self.assertFalse(mock_b2s.called)
        self.assertFalse(mock_d2p.called)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_post')
    @patch('examples.ca_handler.asa_ca_handler.convert_byte_to_string')
    @patch('examples.ca_handler.asa_ca_handler.cert_der2pem')
    @patch('examples.ca_handler.asa_ca_handler.b64_decode')
    @patch('examples.ca_handler.asa_ca_handler.csr_san_byte_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._validity_dates_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._csr_cn_get')
    @patch('examples.ca_handler.asa_ca_handler.csr_pubkey_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuer_chain_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._profile_verify')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuer_verify')
    def test_036_enroll(self, mock_iv, mock_pv, mock_icg, mock_cpg, mockccg, mock_vdg, mock_csbg, mock_b64, mock_d2p, mock_b2s, mock_post):
        """ test enroll() """
        mock_iv.return_value = None
        mock_pv.return_value = None
        mock_icg.return_value = 'issuer_chain'
        mock_vdg.return_value = ('date1', 'date2')
        mock_post.return_value = (500, 'cert')
        mock_b2s.return_value = 'bcert'
        self.assertEqual(('Enrollment failed', None, None, None), self.cahandler.enroll('csr'))
        self.assertTrue(mock_iv.called)
        self.assertTrue(mock_pv.called)
        self.assertTrue(mock_icg.called)
        self.assertTrue(mock_cpg.called)
        self.assertTrue(mockccg.called)
        self.assertTrue(mock_vdg.called)
        self.assertTrue(mock_csbg.called)
        self.assertFalse(mock_b64.called)
        self.assertTrue(mock_post.called)
        self.assertFalse(mock_b2s.called)
        self.assertFalse(mock_d2p.called)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_post')
    @patch('examples.ca_handler.asa_ca_handler.convert_byte_to_string')
    @patch('examples.ca_handler.asa_ca_handler.cert_der2pem')
    @patch('examples.ca_handler.asa_ca_handler.b64_decode')
    @patch('examples.ca_handler.asa_ca_handler.csr_san_byte_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._validity_dates_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._csr_cn_get')
    @patch('examples.ca_handler.asa_ca_handler.csr_pubkey_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuer_chain_get')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._profile_verify')
    @patch('examples.ca_handler.asa_ca_handler.CAhandler._issuer_verify')
    def test_037_enroll(self, mock_iv, mock_pv, mock_icg, mock_cpg, mockccg, mock_vdg, mock_csbg, mock_b64, mock_d2p, mock_b2s, mock_post):
        """ test enroll() """
        mock_iv.return_value = None
        mock_pv.return_value = None
        mock_icg.return_value = 'issuer_chain'
        mock_vdg.return_value = ('date1', 'date2')
        mock_post.return_value = (500, 'cert')
        mock_b2s.return_value = 'bcert'
        mock_cpg.return_value = None
        with self.assertLogs('test_a2c', level='INFO') as lcm:
            self.assertEqual(('Enrollment failed', None, None, None), self.cahandler.enroll('csr'))
        self.assertIn('ERROR:test_a2c:CAhandler._enrollment_dic_create(): public key not found', lcm.output)
        self.assertTrue(mock_iv.called)
        self.assertTrue(mock_pv.called)
        self.assertTrue(mock_icg.called)
        self.assertTrue(mock_cpg.called)
        self.assertFalse(mockccg.called)
        self.assertFalse(mock_vdg.called)
        self.assertFalse(mock_csbg.called)
        self.assertFalse(mock_b64.called)
        self.assertFalse(mock_post.called)
        self.assertFalse(mock_b2s.called)
        self.assertFalse(mock_d2p.called)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_post')
    @patch('examples.ca_handler.asa_ca_handler.cert_serial_get')
    def test_039_revoke(self, mock_serial, mock_post):
        """ test revoke() """
        self.cahandler.ca_name = 'ca_name'
        mock_serial.return_value = 'serial'
        mock_post.return_value = ('code', None)
        self.assertEqual(('code', None, None), self.cahandler.revoke('cert'))
        self.assertTrue(mock_serial.called)
        self.assertTrue(mock_post.called)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_post')
    @patch('examples.ca_handler.asa_ca_handler.cert_serial_get')
    def test_040_revoke(self, mock_serial, mock_post):
        """ test revoke() """
        self.cahandler.ca_name = 'ca_name'
        mock_serial.return_value = 'serial'
        mock_post.return_value = ('code', {'message': 'message'})
        self.assertEqual(('code', 'urn:ietf:params:acme:error:serverInternal', 'message'), self.cahandler.revoke('cert'))
        self.assertTrue(mock_serial.called)
        self.assertTrue(mock_post.called)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_post')
    @patch('examples.ca_handler.asa_ca_handler.cert_serial_get')
    def test_041_revoke(self, mock_serial, mock_post):
        """ test revoke() """
        self.cahandler.ca_name = 'ca_name'
        mock_serial.return_value = 'serial'
        mock_post.return_value = ('code', {'Message': 'Message'})
        self.assertEqual(('code', 'urn:ietf:params:acme:error:serverInternal', 'Message'), self.cahandler.revoke('cert'))
        self.assertTrue(mock_serial.called)
        self.assertTrue(mock_post.called)

    @patch('examples.ca_handler.asa_ca_handler.CAhandler._api_post')
    @patch('examples.ca_handler.asa_ca_handler.cert_serial_get')
    def test_042_revoke(self, mock_serial, mock_post):
        """ test revoke() """
        self.cahandler.ca_name = 'ca_name'
        mock_serial.return_value = 'serial'
        mock_post.return_value = ('code', {'foo': 'bar'})
        self.assertEqual(('code', 'urn:ietf:params:acme:error:serverInternal', 'Unknown error'), self.cahandler.revoke('cert'))
        self.assertTrue(mock_serial.called)
        self.assertTrue(mock_post.called)

if __name__ == '__main__':

    unittest.main()
