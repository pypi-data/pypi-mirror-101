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
from .service import Service
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from flask_socketio import emit


class Devices(Service):
    """ kitica Devices Endpoint.

    ...

    Methods
    ----------
    GET
        Handles the GET Requests.
        Returns specific device/devices specified by the parameter/parameters.
    """

    args = {
        'platformName': fields.Str(required=False,
                                   validate=validate.OneOf(Service.PLATFORMS)
                                   ),
        'server': fields.String(required=False),
        'deviceId': fields.Int(required=False),
        'status': fields.Str(required=False,
                             validate=validate.OneOf(Service.STATUS))
    }

    @use_kwargs(args)
    def put(self, server):
        """Fetches all the devices affiliated with the server host.

        Host IP should be whitelisted in the config.yaml.
        """
        exists = self._parse_server(server)
        if exists is not None:
            return exists, 400
        query = 'SELECT deviceName,deviceId,platformName,udid,server,systemPort,'\
            + 'mjpegServerPort,platformVersion,wdaPort,currentTestCase,previousTestCase,'\
            + 'previousTestStatus FROM device WHERE server IN(\"'\
            + str(server) + '\"' + ',"")'
        devices = self._fetch(query)
        if devices is not None:
            return devices
        return None

    @use_kwargs(args)
    def post(self, deviceId=None, platformName=None, status=None):
        """Devices GET Request Handler.

        Handles GET Requests from [/devices] endpoint.

        Parameters
        ----------
        deviceId : str
            The device's Id given by the database.
        platformName : str, optional
            Device's platform name, should be one of the supported devices
            listed in the config.yaml.
        status : str, optional
            Device's Status on the pool.
        """
        # Ignore all parameter given when deviceId is passed.
        print(self.get_servers())
        if deviceId is not None:
            devices = self.get_device_by_id(deviceId)
        else:
            if platformName is not None:
                query = 'SELECT * FROM device WHERE platformName=\"' \
                     + platformName + '\"'
                if status is not None:
                    query += (' AND status=\"' + str(status) + '\"')
                devices = self._fetch(query)
            else:
                if status is not None:
                    query = ('SELECT * FROM device WHERE status=\"'
                             + str(status) + '\"'
                             )
                    devices = self._fetch(query)
                else:
                    devices = self._fetch('SELECT * FROM device')
        if devices == [] or devices is None:
            return "No Device Found."
        return devices

    @use_kwargs(args)
    def get(self, deviceId=None, platformName=None, status=None):
        """Devices GET Request Handler.

        Handles GET Requests from [/devices] endpoint.

        Parameters
        ----------
        deviceId : str
            The device's Id given by the database.
        platformName : str, optional
            Device's platform name, should be one of the supported devices
            listed in the config.yaml.
        status : str, optional
            Device's Status on the pool.
        """
        # Ignore all parameter given when deviceId is passed.
        print(self.get_servers())
        if deviceId is not None:
            devices = self.get_device_by_id(deviceId)
        else:
            if platformName is not None:
                query = 'SELECT * FROM device WHERE platformName=\"' \
                     + platformName + '\"'
                if status is not None:
                    query += (' AND status=\"' + str(status) + '\"')
                devices = self._fetch(query)
            else:
                if status is not None:
                    query = ('SELECT * FROM device WHERE status=\"'
                             + str(status) + '\"'
                             )
                    devices = self._fetch(query)
                else:
                    devices = self._fetch('SELECT * FROM device')
        if devices == [] or devices is None:
            return "No Device Found."
        return devices
