# -*- coding: utf-8 -*-
from django.conf import settings

from .api import get_connection
from .signals import sms_post_send

class SmsMessage(object):
    """
    A sms message
    """

    def __init__(self, body, from_phone=None, to=None, flash=False, connection=None):
        """
        Initialize a single SMS message (which can be sent to multiple recipients)
        """
        self.to = to

        self.from_phone = from_phone or getattr(
            settings, "SENDSMS_DEFAULT_FROM_PHONE", ""
        )
        self.body = body
        self.flash = flash
        self.connection = connection

    def get_connection(self, fail_silently=False):
        if not self.connection:
            self.connection = get_connection(fail_silently=fail_silently)
        return self.connection

    def send(self, fail_silently=False):
        """
        Sends the sms message
        """
        if not self.to:
            # Don't bother creating the connection if there's nobody to send to
            return 0
        res = self.get_connection(fail_silently).send_messages([self])
        sms_post_send.send(
            sender=self, to=self.to, from_phone=self.from_phone, body=self.body
        )
        return res
