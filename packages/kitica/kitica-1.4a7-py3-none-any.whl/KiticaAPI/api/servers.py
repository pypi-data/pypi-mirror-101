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
# Date          : March 8 2021 13:43 PST
#
from .service import Service
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from flask_socketio import emit
from flask import request
from ..appsocket import socketio


class Servers(Service):
    """ kitica Devices Endpoint.

    ...

    Methods
    ----------
    GET
        Handles the GET Requests to /hosts/servers.
        Fetches the servers manifest as a list.
    POST
        Handles POST Request to /hosts/servers.
        Inserts new server to the database.
    """
    args = {
        'server': fields.String(required=False),
        'active': fields.Int(required=False),
        'clientType': fields.String(required=False,
                                    validate=validate.OneOf(Service.CLIENTS)
                                    ),
        'deleteKey': fields.String(required=False,
                                   validate=validate.OneOf(Service.CONFIG['admin'])
                                   )
    }

    @use_kwargs(args)
    def delete(self, server, deleteKey):
        """ Servers DELETE Handler.

        Handles DELETE Requests made to /hosts/servers endpoint.

        Returns
        ----------
        data : list
        """
        exists = self._parse_server(server)
        if exists is not None:
            return exists
        else:
            binded = self._fetch_column_list(f'SELECT deviceName FROM device WHERE server=\"{server}\"')
            if binded == []:
                self._update(f'DELETE FROM servers WHERE serverAddress=\"{server}\"')
                socketio.emit('onServerDelete', {'server': f'{server} deleted'})
                return {
                    'message': f'{server} deleted.',
                    'statusCode': '1'
                }
            return {
                'message': f'Unable to Delete Server {server}, remove affiliated Device First',
                'affiliatedDevices': binded,
                'statusCode': -1
            }, 400

    def get(self):
        """ Servers GET Method Handler.

        Handles GET Request made to /hosts/servers endpoint.

        Returns
        ----------
        data : list
            Returns the list of servers whitelisted by the API.
        """
        if request.args.get('complete'):
            servers = self._fetch('SELECT * FROM servers')
            data = self._get_servers_device_count(servers)
            return {
                'servers': data
            }
        else:
            return Service.get_servers()

    @use_kwargs(args)
    def patch(self, server, active, clientType):
        """
        """
        exists = self._parse_server(server)
        if exists is not None:
            return exists, 400
        s_type = self.A_CODE.get(clientType)
        query = f'UPDATE servers SET {s_type}={active}'\
            + f' where serverAddress=\"{server}\"'
        self._update(query)
        socketio.emit('onServerStatusUpdate', {'data': f'{server} Status was Updated'})
        return {
            'statusCode': 1
        }

    @use_kwargs(args)
    def post(self, server):
        """ Servers POST Method Handler.

        Handles POST Request made to /hosts/servers endpoint.

        Parameters
        ----------
        server : str
            The server to be whitelisted, must not be existing.
        """
        servers = Service.get_servers()
        if server not in servers:
            query = f'INSERT INTO servers (serverAddress) VALUES(\"{server}\");'
            self._update(query)
            socketio.emit('onServerAdd', {'data': f'{server} Added'})
            return {
                'message': f'Added {server} to allowed hosts.',
                'statusCode': 1
            }
        else:
            return {
                'message': 'Host already exists.',
                'statusCode': -1
            }, 400
