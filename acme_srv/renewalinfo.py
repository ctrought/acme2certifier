# -*- coding: utf-8 -*-
""" Nonce class """
from __future__ import print_function
from typing import Dict
from acme_srv.db_handler import DBstore
from acme_srv.message import Message
from acme_srv.helper import string_sanitize, certid_hex_get, uts_to_date_utc, error_dic_get, load_config, uts_now, cert_serial_get, cert_aki_get


class Renewalinfo(object):
    """ Nonce handler """

    def __init__(self, debug: bool = False, srv_name: str = None, logger: object = None):
        self.debug = debug
        self.logger = logger
        self.server_name = srv_name
        self.path_dic = {'renewalinfo': '/acme/renewal-info/'}
        self.dbstore = DBstore(self.debug, self.logger)
        self.message = Message(self.debug, self.server_name, self.logger)
        self.renewaltreshold_pctg = 85
        self.retry_after_timeout = 86400
        self.renewal_force = False
        self.err_msg_dic = error_dic_get(self.logger)

    def __enter__(self):
        """ Makes ACMEHandler a Context Manager """
        self._config_load()
        return self

    def __exit__(self, *args):
        """ cose the connection at the end of the context """

    def _config_load(self):
        """" load config from file """
        self.logger.debug('Certificate._config_load()')
        config_dic = load_config()

        if 'Renewalinfo' in config_dic:

            self.renewal_force = config_dic.getboolean('Renewalinfo', 'renewal_force', fallback=False)

            if 'renewaltreshold_pctg' in config_dic['Renewalinfo']:
                try:
                    self.renewaltreshold_pctg = float(config_dic['Renewalinfo']['renewaltreshold_pctg'])
                except Exception as err_:
                    self.logger.error('acme2certifier Renewalinfo._config_load() renewaltreshold_pctg parsing error: %s', err_)

            if 'retry_after_timeout' in config_dic['Renewalinfo']:
                try:
                    self.retry_after_timeout = int(config_dic['Renewalinfo']['retry_after_timeout'])
                except Exception as err_:
                    self.logger.error('acme2certifier Renewalinfo._config_load() retry_after_timeout parsing error: %s', err_)

    def _cert_table_update(self):
        """ add serial and aki to certificate table """
        self.logger.debug('Renewalinfo._cert_table_update()')

        certificate_list = self.dbstore.certificates_search('serial', None, operant='is', vlist=['id', 'name', 'cert', 'cert_raw', 'serial', 'aki'])

        update_cnt = 0
        for cert in certificate_list:
            if cert['cert_raw']:
                serial = cert_serial_get(self.logger, cert['cert_raw'], hexformat=True)
                aki = cert_aki_get(self.logger, cert['cert_raw'])
                data_dic = {'serial': serial, 'aki': aki, 'name': cert['name'], 'cert_raw': cert['cert_raw'], 'cert': cert['cert']}
                self.dbstore.certificate_add(data_dic)
                update_cnt += 1

        self.logger.debug('Renewalinfo._cert_table_update(%s) - done', update_cnt)

    def _lookup(self, certid_hex: str) -> Dict[str, str]:
        """ lookup expiry dates based on renewal info """
        self.logger.debug('Renewalinfo._lookup()')

        try:
            result_dic = self.dbstore.certificate_lookup('renewal_info', certid_hex, ('id', 'name', 'cert', 'cert_raw', 'expire_uts', 'issue_uts', 'created_at'))
        except Exception as err_:
            self.logger.critical('acme2certifier database error in Renewalinfo._lookup(): %s', err_)
            result_dic = None

        return result_dic

    def _renewalinfo_get(self, certid_hex: str) -> Dict[str, str]:
        """ create dictionary containing renwal infor data """
        self.logger.debug('Renewalinfo.get()')

        # lookup database for certificate data
        cert_dic = self._lookup(certid_hex)

        if 'expire_uts' in cert_dic and cert_dic['expire_uts']:

            # we may need to set issue_uts to cover some cornercases
            if 'issue_uts' not in cert_dic or not cert_dic['issue_uts']:
                cert_dic['issue_uts'] = uts_now()

            # for debugging trigger immediate renwal
            if self.renewal_force:
                self.logger.debug('Renewalinfo.get() - force renewal')
                cert_dic['expire_uts'] = uts_now() + 86400
                start_uts = int(cert_dic['expire_uts'] - (365 * 86400))
            else:
                start_uts = int((cert_dic['expire_uts'] - cert_dic['issue_uts']) * self.renewaltreshold_pctg / 100) + cert_dic['issue_uts']

            renewalinfo_dic = {
                'suggestedWindow': {
                    'start': uts_to_date_utc(start_uts),
                    'end': uts_to_date_utc(cert_dic['expire_uts'])
                }
            }

        else:
            renewalinfo_dic = {}

        return renewalinfo_dic

    def renewalinfo_string_get(self, url: str) -> str:
        """ get renewal string from url"""
        self.logger.debug('Renewalinfo.renewal_string_get()')

        # we need to workaround a strange issue in win-acme
        url = url.replace(f'{self.server_name}{self.path_dic["renewalinfo"].rstrip("/")}', '')
        url = url.lstrip('/')

        # sanitize renewal_info string
        renewalinfo_string = string_sanitize(self.logger, url)

        self.logger.debug('Renewalinfo.renewal_string_get() - renewalinfo_string: %s', renewalinfo_string)
        return renewalinfo_string

    def get(self, url: str) -> Dict[str, str]:
        """ get renewal information """
        self.logger.debug('Renewalinfo.get()')

        # shousekeeping - add serial and aki to certificate table
        self._cert_table_update()

        # parse renewalinfo
        renewalinfo_string = self.renewalinfo_string_get(url)

        (mda, certid_hex) = certid_hex_get(self.logger, renewalinfo_string)

        response_dic = {}
        # we cannot verify the AKI thus we accept any value
        if mda:
            # get renewal window datas
            rewalinfo_dic = self._renewalinfo_get(certid_hex)
            if rewalinfo_dic:
                response_dic['code'] = 200
                # filter certificate and decode it
                response_dic['data'] = rewalinfo_dic
                # order status is processing - ratelimiting
                response_dic['header'] = {'Retry-After': f'{self.retry_after_timeout}'.format()}
            else:
                response_dic['code'] = 404
                response_dic['data'] = self.err_msg_dic['malformed']
        else:
            response_dic['code'] = 400
            response_dic['data'] = self.err_msg_dic['malformed']

        return response_dic

    def update(self, content: str) -> Dict[str, str]:
        """ update renewalinfo request """
        self.logger.debug('Renewalinfo.update()')

        # check message
        (code, _message, _detail, _protected, payload, _account_name) = self.message.check(content)

        response_dic = {}
        if code == 200 and 'certid' in payload and 'replaced' in payload:

            (_mda, certid_hex) = certid_hex_get(self.logger, payload['certid'])

            cert_dic = self._lookup(certid_hex)

            if cert_dic and payload['replaced']:
                cert_dic['replaced'] = True
                cert_id = self.dbstore.certificate_add(cert_dic)

                if cert_id:
                    response_dic['code'] = 200
                else:
                    response_dic['code'] = 400
            else:
                response_dic['code'] = 400
        else:
            response_dic['code'] = 400

        return response_dic
