import datetime
import hashlib
import os

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from sendsms.message import SmsMessage

# class VerifyCode(models.Model):

#     verify_code = models.CharField(null=True, blank=True, max_length=4)

#     phone_number = models.CharField(null=True, blank=True, unique=True, max_length=16)

#     class Meta:
#         db_table = 'verifycode'

class PhoneNumberUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email,
                     password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            username=username, email=email, phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, phone_number,
                    email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, phone_number, email, password,
                                 **extra_fields)

    def create_superuser(self, username, phone_number, email, password,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, phone_number, email, password,
                                 **extra_fields)


class PhoneNumberAbstactUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    objects = PhoneNumberUserManager()

    class Meta:
        abstract = True


class PhoneToken(models.Model):
    phone_number = PhoneNumberField(blank=True, null=True)
    otp = models.CharField(blank=True, null=True, max_length=6)
    attempts = models.IntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        db_table = 'phone_token'

    def __str__(self):
        return "{} - {}".format(self.phone_number, self.otp)

    @classmethod
    def create_otp_for_number(cls, number):
        # The max otps generated for a number in a day are only 10.
        # Any more than 10 attempts returns False for the day.
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        otps = cls.objects.filter(phone_number=number, timestamp__range=(today_min, today_max))
        if otps.count() <= getattr(settings, 'PHONE_LOGIN_ATTEMPTS', 10):
            otp = cls.generate_otp(length=getattr(settings, 'PHONE_LOGIN_OTP_LENGTH', 6))
            phone_token = PhoneToken(phone_number=number, otp=otp)
            phone_token.save()
            from_phone = getattr(settings, 'SENDSMS_FROM_NUMBER')
            message = SmsMessage(
                body=render_to_string(
                    "otp_sms.txt",
                    {"otp": otp, "id": phone_token.id}
                ),
                from_phone=from_phone,
                to=[number]

            )
            message.send()
            return phone_token
        else:
            return False

    @classmethod
    def generate_otp(cls, length=6):
        hash_algorithm = getattr(settings, 'PHONE_LOGIN_OTP_HASH_ALGORITHM', 'sha256')
        m = getattr(hashlib, hash_algorithm)()
        m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
        m.update(os.urandom(16))
        otp = str(int(m.hexdigest(), 16))[-length:]
        return otp
