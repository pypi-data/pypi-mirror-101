#!/usr/bin/env python
# Python class to connect to an E3/DC system through the internet portal
#
# Copyright 2017 Francesco Santini <francesco.santini@gmail.com>
# Licensed under a MIT license. See LICENSE for details

import socket
from _rscpLib import rscpFrame, rscpEncode, rscpFrameDecode, rscpDecode, rscpFindTag
from _RSCPEncryptDecrypt import RSCPEncryptDecrypt
import time
import datetime

PORT = 5033
BUFFER_SIZE=1024*32

class RSCPAuthenticationError(Exception):
    pass

class CommunicationError(Exception):
    pass


class E3DC_RSCP_local:
    """A class describing an E3DC system, used to poll the status from the portal
    """
    def __init__(self, username, password, ip, key):
        self.username = username
        self.password = password
        self.ip = ip
        self.key = key
        self.socket = None
        self.encdec = None
        self.processedData = None
        
    def _send(self, plainMsg):
        sendData = rscpFrame( rscpEncode( plainMsg ) )
        encData = self.encdec.encrypt(sendData)
        self.socket.send(encData)

    def _receive(self):
        data = self.socket.recv(BUFFER_SIZE)
        decData = rscpDecode( self.encdec.decrypt(data) )[0]
        return decData
    
    def sendCommand(self, plainMsg):
        self.sendRequest(plainMsg) # same as sendRequest but doesn't return a value
        
    def sendRequest(self, plainMsg):
        self._send(plainMsg)
        receive = self._receive()
        if receive[1] == 'Error':
            raise CommunicationError
        return receive
        
    def connect(self):
        if self.socket is not None:
            self.disconnect()
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, PORT))
        self.processedData = None

        self.encdec = RSCPEncryptDecrypt(self.key)

        decData = self.sendRequest ( ('RSCP_REQ_AUTHENTICATION', 'Container', [
            ('RSCP_AUTHENTICATION_USER', 'CString', self.username),
            ('RSCP_AUTHENTICATION_PASSWORD', 'CString', self.password)]) )
        
        if decData[1] == 'Error':
            self.socket.close()
            raise RSCPAuthenticationError("Invalid username or password")
        
    def disconnect(self):
        self.socket.close()
        self.socket = None
    
    def isConnected(self):
        return self.socket is not None
    

