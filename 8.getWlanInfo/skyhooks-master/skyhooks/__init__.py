import os
from datetime import timedelta


def get_version_string():
    return open(os.path.join(os.path.dirname(__file__), 'version.txt'),
                                                    'r').read().strip()


def get_version():
    return tuple(int(i) for i in get_version_string().split('.'))

__version__ = get_version_string()


class IOLoop(object):
    """Wrapper for native ioloop/event loop/reactor instances.
    """

    # Stores the last greenlet spawned, only used for Gevent
    _last_greenlet = None

    # Stores the last Deferred object, only used for Twisted Matrix
    _last_deferred = None

    def __init__(self, system_type):
        self.system = system_type.lower()

        if self.system == 'tornado':
            from tornado import ioloop
            self._loop = ioloop.IOLoop.instance()

        elif self.system == 'gevent':
            from gevent import Greenlet
            self._greenlet = Greenlet

        elif self.system == 'twisted':
            from twisted import reactor
            self._reactor = reactor

    def add_callback(self, callback, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        if self.system == 'tornado':
            self._loop.add_callback(lambda: callback(*args, **kwargs))

        elif self.system == 'gevent':
            self._last_greenlet = self._greenlet.spawn(callback, *args,
                                                       **kwargs)

        elif self.system == 'twisted':
            self._last_deferred = self._reactor.callLater(0, callback, *args,
                                                          **kwargs)

    def add_timeout(self, callback, when, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        if self.system == 'tornado':
            if isinstance(when, int):
                when = timedelta(seconds=when)

            self._loop.add_timeout(when, lambda: callback(*args, **kwargs))

        elif self.system == 'gevent':
            if isinstance(when, timedelta):
                when = when.seconds

            self._last_greenlet = self._greenlet.spawn_later(when, callback,
                                                             *args, **kwargs)

        elif self.system == 'twisted':
            if isinstance(when, timedelta):
                when = when.seconds

            self._last_deferred = self._reactor.callLater(when, callback,
                                                          *args, **kwargs)
