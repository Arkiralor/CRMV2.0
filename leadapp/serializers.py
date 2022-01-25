from rest_framework import serializers
from .models import *

# Create your serializers here:


class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = '__all__'


class AcademicSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcademicReq
        fields = '__all__'
