#!/usr/bin/python3
# This file deals with the Tilt formatted message

import json
from struct import unpack

# Tilt format based on iBeacon format and filter includes Apple iBeacon
# identifier portion (4c000215) as well as Tilt specific uuid preamble (a495)
APPLE_MANUFACTURER_ID   = 0x4c
IBEACONS_ID             = b"\x02\x15"
TILT_ID                 = b"\xa4\x95"

class Tilt(object):
    """
    Class decoding the content of a Tilt advertisement
    """
    def decode(self, packet):
        manufacturer_id = packet.retrieve_last("Manufacturer ID").val if packet.retrieve_last("Manufacturer ID") else None
        payload = packet.retrieve_last("Payload").val if packet.retrieve_last("Payload") else None

        if manufacturer_id == APPLE_MANUFACTURER_ID and payload:
            # See https://en.wikipedia.org/wiki/IBeacon#BLE_Advertisement_Packet_Structure_Byte_Map
            if payload[0:2] == IBEACONS_ID and payload[2:4] == TILT_ID:
                data = {}

                rssi = packet.retrieve_last("rssi").val if packet.retrieve_last("rssi") else None
                mac = packet.retrieve_last("peer").val if packet.retrieve_last("peer") else None

                data['uuid']        = payload[2:18].hex("-")
                data['major']       = unpack('>H', payload[18:20])[0]   # Temperature in degrees F
                data['minor']       = unpack('>H', payload[20:22])[0]   # Specific gravity x1000
                data['tx_power']    = unpack('>b', payload[22:23])[0]   # Weeks since battery change (0-152 when converted to unsigned 8 bit integer) and other TBD operation codes
                data['rssi']        = rssi
                data['mac']         = mac

                return json.dumps(data)
