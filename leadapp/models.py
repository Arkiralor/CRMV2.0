from django.db import models
from django.forms import CharField
from userapp.models import AgentProfile
from .choices import GENDER_CHOICE, FACULTY_CHOICE, STATE_CHOICE
from .validators import PHONE_VALID, PIN_VALID

# Create your models here.


class Lead(models.Model):
    '''
    Basic info from the forms submitted.
    '''

    fname = models.CharField(max_length=16)
    mname = models.CharField(max_length=16, null=True, blank=True)
    lname = models.CharField(max_length=16)
    legacy = models.CharField(max_length=5, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=64)
    phone = models.CharField(max_length=10, validators=[PHONE_VALID])
    email = models.EmailField(max_length=128)
    claimed_by = models.ForeignKey(
        AgentProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        representation = f"{self.fname} {self.lname}"
        return representation


class Contact(models.Model):
    '''
    Contact info from the forms submitted.
    '''
    prospect = models.ForeignKey(Lead, on_delete=models.CASCADE)
    address_1 = models.CharField(max_length=256)
    address_2 = models.CharField(max_length=256)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64, choices=STATE_CHOICE)
    pin_code = models, CharField(max_length=6, validators=[PIN_VALID])
    claimed_by = models.ForeignKey(
        AgentProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        representation = f"{self.prospect}"
        return representation


class AcademicReq(models.Model):
    '''
    Academic preferences info from the forms submitted.
    '''
    prospect = models.ForeignKey(Lead, on_delete=models.CASCADE)
    faculty = models.CharField(max_length=64, choices=FACULTY_CHOICE)
    subject = models.CharField(max_length=64)
    claimed_by = models.ForeignKey(
        AgentProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        representation = f"{self.prospect}"
        return representation
