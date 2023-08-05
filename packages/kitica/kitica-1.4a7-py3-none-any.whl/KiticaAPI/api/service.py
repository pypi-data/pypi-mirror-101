# -*- coding: utf-8 -*-
#  _     _       _
# | |   (_)  _  (_)
# | |  _ _ _| |_ _  ____ _____
# | |_/ ) (_   _) |/ ___|____ |
# |  _ (| | | |_| ( (___/ ___ |
# |_| \_)_|  \__)_|\____)_____|
#
# kitica DevicePool API
# Created by    : Joshua Kim Rivera
# Date          : September 23 2020 15:16 UTC-8
# Company       : Spiralworks Technologies Inc.
#
from flask_restful import Resource
from flask_socketio import SocketIO, emit
from KiticaAPI.utils import (
    Database,
    Configurations,
    Constants
)


class Service(Resource,
              Database,
              Constants
              ):
    """
    Base API Service Class
    """
    CONFIG = Configurations()._load_config_file()

    def __init__(self):
        pass

    def _parse_server(self, server):
        """
        Parse Server Service Method.

        Asserts Server existence on record.
        Returns None for existing record.
        """
        servers = self.get_servers()
        if server not in servers:
            return {
                'message': f'{server} does not exist',
                'statusCode': -1
            }
        return None

    def _get_servers_device_count(self, servers):
        """
        """
        count = self._fetch('SELECT server, COUNT(DISTINCT deviceId) \
            as deviceCount from device GROUP BY server')
        for server in servers:
            for s_count in count:
                if server['serverAddress'] in s_count.values():
                    server['deviceCount'] = s_count['deviceCount']
                    break
                else:
                    server['deviceCount'] = 0
        return servers

    @staticmethod
    def get_servers():
        db = Database()
        return db._fetch_column_list('SELECT serverAddress FROM servers')
