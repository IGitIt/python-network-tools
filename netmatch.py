#!/usr/bin/env python3

"""netmatch.py - Check if the specified IP is in the specified network.

Usage: netmatch.py ip_address network_address/bits

Example: netmatch.py 192.168.0.1 192.168.0.0/24
"""

__author__ = 'Jerry Wang (jerrywang at gmail)'


import socket
import struct
import sys


program_name = sys.argv[0]


def netmatch(ip, network, slash_bits, debug=False):

    """Return True if ip is in network, False otherwise.  Only works for
    IPv4 addresses."""

    ipaddr = struct.unpack('!L', socket.inet_aton(ip))[0]

    if debug:
        print('ipaddr: %x' % ipaddr)

    netaddr = struct.unpack('!L', socket.inet_aton(network))[0]

    if debug:
        print('netaddr: %x' % netaddr)

    slash_32 = 2**32 - 1   # 255.255.255.255
    host_bits = 2**(32 - int(slash_bits)) - 1

    if debug:
        print('host_bits: %s' % host_bits)

    mask_bits = slash_32 - host_bits

    if debug:
        print('mask_bits: %s' % mask_bits)

    netmask = struct.unpack('!L', struct.pack('!L', mask_bits))[0]

    if debug:
        print('netmask: %x' %netmask)

    return ipaddr & netmask == netaddr


if __name__ == '__main__':

    # If we're not run with two arguments, show a help message and exit
    # with an error.
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    # TODO: Enforce valid IPs and CIDR prefix bit lengths.

    ip_address = sys.argv[1]
    network_address, cidr_prefix_bits = sys.argv[2].split('/')

    print(netmatch(ip_address, network_address, cidr_prefix_bits))
