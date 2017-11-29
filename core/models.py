from __future__ import unicode_literals
import uuid
from autoslug import AutoSlugField

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from .managers import PersonManager
from .enums import Status, PersonGroupType
from .fields import TimestampImageField


class Department(models.Model):
    name = models.CharField(max_length=24, unique=True, blank=False, null=False)
    alias = models.UUIDField(
        default=uuid.uuid4, editable=False, db_index=True, unique=True)
    
    def __str__(self):
        name = u"{}".format(self.name)
        return name


class Session(models.Model):
    name = models.CharField(max_length=24, unique=True, blank=False, null=False)
    alias = models.UUIDField(
        default=uuid.uuid4, editable=False, db_index=True, unique=True)
    
    def __str__(self):
        name = u"{}".format(self.name)
        return name



class Person(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=24, unique=True, blank=False, null=False)
    email = models.EmailField(db_index=True, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=24, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('''Whether this user should be treated as active. Unselect this instead of
         deleting accounts.'''))
    # Extended fields
    person_group = models.IntegerField(
        choices=[(choice.value, choice.name.replace("_", " ")) for choice in PersonGroupType], default=PersonGroupType.DEFAULT.value)
    department = models.ForeignKey(
        Department, models.DO_NOTHING, default=None, blank=True, null=True)
    session = models.ForeignKey(
        Session, models.DO_NOTHING, blank=True, null=True)
    profile_image = TimestampImageField(
        upload_to='profiles/pic', blank=True, null=True)
    status = models.IntegerField(
        choices=[(choice.value, choice.name.replace("_", " ")) for choice in Status], default=Status.ACTIVE.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'user_id'
    objects = PersonManager()

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        name = u"{} - {} {}".format(self.user_id, self.first_name,
                                self.last_name,)
        return name.strip()

    def get_full_name(self):
        """ Returns the full name """
        name = u"{} - {} {}".format(self.user_id, self.first_name,
                                self.last_name,)
        return name.strip()
    
    def get_short_name(self):
        return u"{}".format(self.user_id)



class Assignment(models.Model):
    teacher = models.ForeignKey(
        Person, models.DO_NOTHING, blank=False, null=False)
    name = models.CharField(max_length=256, blank=False, null=False)
    department = models.ForeignKey(
        Department, models.DO_NOTHING, default=None, blank=True, null=True, related_name="assignment_department")
    session = models.ForeignKey(
        Session, models.DO_NOTHING, blank=True, null=True, related_name="assignment_session")
    description = models.TextField(blank=True, null=True)
    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)
    clone = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(
        choices=[(choice.value, choice.name.replace("_", " ")) for choice in Status], default=Status.PENDING.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        name = u"{} / {}".format(self.name, self.teacher,)
        return name.strip()

    class Meta:
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')


class StudentAssignment(models.Model):
    student = models.ForeignKey(
        Person, models.DO_NOTHING, blank=False, null=False, related_name='assignment_student')
    assigned_by = models.ForeignKey(
        Person, models.DO_NOTHING, blank=True, null=True, related_name='assignment_assigned_by')
    assignment = models.ForeignKey(
        Assignment, models.DO_NOTHING, blank=False, null=False, related_name="assignment_of_student")
    deadline = models.DateField()
    alias = models.UUIDField(
        default=uuid.uuid4, editable=False, db_index=True, unique=True)
    clone = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    container_name = models.CharField(max_length=256, blank=True, null=True)
    container_tag = models.CharField(max_length=128, blank=True, null=True)
    github_url = models.CharField(max_length=1000, blank=True, null=True)
    status = models.IntegerField(
        choices=[(choice.value, choice.name.replace("_", " ")) for choice in Status], default=Status.PENDING.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('student assignment')
        verbose_name_plural = _('student assignments')

        unique_together = (('student', 'assignment'), )

    def __str__(self):
        return self.get_name()

    def get_name(self):
        name = u"{} / {} / {}".format(self.assignment, self.student, self.deadline)
        return name
