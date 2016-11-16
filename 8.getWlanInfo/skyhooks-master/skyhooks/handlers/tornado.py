"""Tornado web handlers for webhook POST requests.
"""

from __future__ import absolute_import

from tornado.web import RequestHandler
from tornado.escape import json_decode, json_encode


class WebhookHandler(RequestHandler):
    """Handle webhook post backs from celery tasks and route to websockets
    via registered callbacks.
    """

    def post(self):
        payload = json_decode(self.request.body)
        data = payload['data']
        keys = payload['keys']

        self.application.webhook_container.logger.info("Received webhook "
                                                       "postback for %s",
                                                                     keys)

        if not self.application.webhook_container.notify(keys, data):
            self.set_status(404)
            return

        # Celery compatible "hook" response, good enough for our purposes
        self.content_type = 'application/json'
        self.write(json_encode({"status": "ok"}))
