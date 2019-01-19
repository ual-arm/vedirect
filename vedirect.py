#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, serial, argparse

class vedirect:

    def __init__(self, serialport, timeout):
        self.serialport = serialport
        self.ser = serial.Serial(serialport, 19200, timeout=timeout)
        self.header1 = '\r'
        self.header2 = '\n'
        self.hexmarker = ':'
        self.delimiter = '\t'
        self.key = ''
        self.value = ''
        self.bytes_sum = 0;
        self.state = self.WAIT_HEADER       # global state
        # global checksum state (used for stopping sum of bytes for checksum value)
        self.stateTmp = self.WAIT_HEADER    
        self.dict = {}


    (HEX, WAIT_HEADER, IN_KEY, IN_VALUE, IN_CHECKSUM) = range(5)
    
    def getInt(self, default=0):
        try:
            return int(nb)
        except Exception:
            return default
        return default
            
    def input(self, byte):
        if byte == self.hexmarker and self.state != self.IN_CHECKSUM:
            self.state = self.HEX
            
        
        if self.state == self.WAIT_HEADER:
            self.bytes_sum += ord(byte)
            if byte == self.header1:
                self.state = self.WAIT_HEADER
            elif byte == self.header2:
                self.state = self.IN_KEY

            return None
        elif self.state == self.IN_KEY:
            self.bytes_sum += ord(byte)
            if byte == self.delimiter:
                if (self.key == 'Checksum'):
                    # Checksum detected (now get value and stop byte count)
                    self.stateTmp = self.IN_CHECKSUM 
                    self.state = self.IN_VALUE
                else:
                    self.state = self.IN_VALUE
            else:
                self.key += byte
            return None
        elif self.state == self.IN_VALUE:
            # stopping byte count only for checksum value)
            if self.stateTmp != self.IN_CHECKSUM:
                self.bytes_sum += ord(byte)
                
            if byte == self.header1:
                if self.stateTmp != self.IN_CHECKSUM:
                    self.state = self.WAIT_HEADER
                    self.dict[self.key] = self.value;
                    self.key = '';
                    self.value = '';
                 else:
                    self.state = self.IN_CHECKSUM
                    self.stateTmp = self.WAIT_HEADER
                    
            else:
                self.value += byte
            return None
        elif self.state == self.IN_CHECKSUM:
            
            # convert value to int
            self.value = self.getInt(self.value)
            
            self.state = self.WAIT_HEADER
            if ((self.bytes_sum+self.value) % 256 == 0):
                self.bytes_sum = 0
                return self.dict
            else:
                print 'Malformed packet'
                self.bytes_sum = 0
            self.key = ''
            self.value = ''
            
        elif self.state == self.HEX:
            self.bytes_sum = 0
            if byte == self.header2:
                self.state = self.WAIT_HEADER
        else:
            raise AssertionError()

    def read_data(self):
        while True:
            byte = self.ser.read(1)
            packet = self.input(byte)

    def read_data_single(self):
        while True:
            byte = self.ser.read(1)
            packet = self.input(byte)
            if (packet != None):
                return packet
            

    def read_data_callback(self, callbackFunction):
        while True:
            byte = self.ser.read(1)
            if byte:
                packet = self.input(byte)
                if (packet != None):
                    callbackFunction(packet)
            else:
                break


def print_data_callback(data):
    print data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process VE.Direct protocol')
    parser.add_argument('--port', help='Serial port')
    parser.add_argument('--timeout', help='Serial port read timeout', type=int, default='60')
    args = parser.parse_args()
    ve = vedirect(args.port, args.timeout)
    ve.read_data_callback(print_data_callback)
    #print(ve.read_data_single())
    

