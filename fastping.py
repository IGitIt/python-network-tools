#!/usr/bin/env python3

"""fastping.py - Parallel ping for Linux, Solaris, and Mac OS X.

Usage: fastping.py host1 [host2] [host3] [...]

Example: fastping.py www.yahoo.com www.aol.com www.microsoft.com 192.168.0.1
"""

__author__ = 'Jerry Wang (jerrywang at gmail)'


import os
import sys
import threading


def linux_ping(host, timeout=5):

    """Ping a host from a Linux system.  If no timeout is specified,
    default to 5 seconds."""

    # The ping (from the iputils package) that ships with Linux
    # distributions doesn't let you exit immediately after receiving the
    # first reply packet.
    return os.system('/bin/ping -w %d %s >/dev/null 2>&1' % (timeout, host))


def solaris_ping(host, timeout=5):

    """Ping a host from a Solaris system.  If no timeout is specified,
    default to 5 seconds."""

    return os.system('/usr/sbin/ping %s %d >/dev/null 2>&1' % (host, timeout))


def macosx_ping(host, timeout=5):

    """Ping a host from a Mac OS X system.  If no timeout is specified,
    default to 5 seconds."""

    return os.system('/sbin/ping -o -t %d %s >/dev/null 2>&1' % (timeout, host))


class PingHost(threading.Thread):

    """A target host to ping."""

    def __init__(self, host, ping=linux_ping, timeout=5):
        threading.Thread.__init__(self)
        self.host = host
        self.ping = ping
        self.timeout = timeout
        self.status = 1
    def run(self):
        self.status = self.ping(self.host, self.timeout)


def fastping(hosts, timeout=5):

    """Ping a list of hosts in parallel and return a list of two lists:
    a "good" list (hosts that responded to ping) and a "bad" list (all
    other hosts).  If no timeout is specified, default to 5 seconds.
    """

    platform = os.uname()[0]

    if   platform == 'Linux':
        ping = linux_ping
    elif platform == 'SunOS':
        ping = solaris_ping
    elif platform == 'Darwin':
        ping = macosx_ping
    else:
        raise Exception(
            "{platform} is not supported.".format(platform=platform)
        )

    ping_threads = []

    for host in hosts:
        ping_thread = PingHost(host, ping, timeout)
        ping_thread.start()
        ping_threads.append(ping_thread)

    good = []
    bad  = []

    for ping_thread in ping_threads:
        ping_thread.join()
        if ping_thread.status == 0:
            good.append(ping_thread.host)
        else:
            bad.append(ping_thread.host)

    return [good, bad]


if __name__ == '__main__':

    # If we're run without any arguments, show a help message and exit
    # with an error.
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    # Treat each argument as a host and try to ping all of them in parallel.
    good_hosts, bad_hosts = fastping(sys.argv[1:])

    # Show the results.
    print('GOOD: %s' % ' '.join(good_hosts))
    print('BAD:  %s' % ' '.join(bad_hosts))
