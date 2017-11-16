# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

from .enums import PersonGroupType

logger = logging.getLogger(__name__)


class PersonManager(BaseUserManager):

    def _create_user(self, user_id, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        user = self.model(user_id=user_id, is_staff=is_staff, is_active=True, is_superuser=is_superuser,
                          last_login=now, person_group=PersonGroupType.DEFAULT.value, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, password=None, **extra_fields):
        return self._create_user(user_id, password, False, False, **extra_fields)

    def create_superuser(self, user_id, password, **extra_fields):
        return self._create_user(user_id, password, True, True, **extra_fields)
