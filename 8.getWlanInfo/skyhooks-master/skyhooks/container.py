"""Container object for registering hook callbacks, and maintaining hook
pointers in a persistence layer (e.g. MongoDB) with TTLs.
"""

import logging
from skyhooks import IOLoop


class WebhookContainer(object):
    callbacks = {}

    def __init__(self, config=None, **kwargs):

        self.logger = logging.getLogger('skyhooks')

        if config is None:
            config = {}
        config.update(kwargs)

        if 'url' not in config:
            raise AttributeError('Please provide a webhook URL')

        if 'system_type' not in config:
            raise AttributeError('Please set the system_type to either gevent '
                                 'or tornado')

        elif config['system_type'] == 'twisted':
            raise NotImplemented('Twisted Matrix support is planned for the'
                                 ' future')

        self.config = config
        self.url = config['url']
        self.ioloop = IOLoop(config['system_type'])

        if self.config.get('auto_renew', True):
            if 'renew_seconds' not in self.config:
                self.config['renew_seconds'] = 120

            self.queue_renew_all()

    @property
    def backend(self):
        """Property with lazyloaded Backend instance
        """

        if not hasattr(self, '_backend'):
            backend_path = 'skyhooks.backends.%s' % (self.config.get('backend',
                                                             'mongodb'))
            backend_module = __import__(name=backend_path, globals=globals(),
                   locals=locals(), fromlist="*")
            self._backend = backend_module.Backend(self.config, self.ioloop)

        return self._backend

    def _query_callback(self, doc, error, action):

        if error:
            self.logger.error('Webhook %s error: %s', action, error)

    def register(self, keys, callback):

        if type(keys) in (list, tuple):
            keys = zip(keys)

        for key, value in keys.iteritems():
            if key not in self.callbacks:
                self.callbacks[key] = {}

            if value not in self.callbacks[key]:
                self.callbacks[key][value] = []

            self.callbacks[key][value].append(callback)

        callback_wrapper = lambda doc, error: self._query_callback(
                                                doc, error, 'registration')

        self.logger.info('Registering webhook for %s %s', keys, self.url)
        self.backend.update_hooks(keys, self.url, callback_wrapper)

    def unregister(self, keys, callback):

        if type(keys) in (list, tuple):
            keys = zip(keys)

        deleted_keys = {}
        for key, value in keys.iteritems():
            if key in self.callbacks and value in self.callbacks[key]:
                self.callbacks[key][value].remove(callback)

                if len(self.callbacks[key][value]) is 0:
                    del self.callbacks[key][value]

                    if key not in deleted_keys:
                        deleted_keys[key] = {}

                    deleted_keys[key] = value

                self.logger.info('Removing callback for %s %s %s' % (key,
                                                                     value,
                                                                     self.url))

        if deleted_keys:
            callback_wrapper = lambda doc, error: self._query_callback(
                                                    doc, error, 'removal')

            self.logger.info('Removing webhook for %s %s', deleted_keys,
                                                           self.url)

            self.backend.remove_hooks(deleted_keys, self.url, callback_wrapper)

    def notify(self, keys, data):

        if type(keys) in (list, tuple):
            keys = zip(keys)

        notified = []
        for key, value in keys.iteritems():
            if key in self.callbacks and value in self.callbacks[key]:
                notified.append(True)

                for callback in self.callbacks[key][value]:
                    self.ioloop.add_callback(lambda cb=callback: cb(data))
            else:
                notified.append(False)

        return all(notified)

    def queue_renew_all(self, *args, **kwargs):

        self.logger.info('Queued webhook renewal cycle.')
        self.ioloop.add_timeout(self.renew_all, self.config['renew_seconds'])

    def renew_all(self):

        keys = dict((k, v.keys()) for (k, v) in self.callbacks.iteritems())
        if keys:
            self.logger.info('Renewing webhooks.')
            self.logger.debug('%d callbacks registered in skyhooks.' % (
                         sum(len(v) for v in self.callbacks.itervalues())))
            self.backend.update_hooks(keys, callback=self.queue_renew_all,
                                      url=self.url)
        else:
            self.logger.info('No webhooks to renew.')
            self.queue_renew_all()
