from django.shortcuts import render

from leadapp.serializers import AcademicSerializer, ContactSerializer, LeadSerializer
from .models import Lead, Contact, AcademicReq
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .utils import get_agent

# Create your views here.

class GetUnclaimed(APIView):
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated)

    def get(self, request):
        try:
            leads = Lead.objects.filter(
                Q(claimed_by=None)
                or Q(claimed_by="")
            ).all()
            serialized = LeadSerializer(leads, many=True)
        except Lead.DoesNotExist:
            return Response(
                {
                    "error": "no unclaimed leads"
                },
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            serialized.data,
            status=status.HTTP_202_ACCEPTED
        )
        
class NewLead(APIView):

    def post(self, request):
        new_data = request.data

        basic = LeadSerializer(data=new_data)
        if basic.is_valid():
            basic.claimed_by = None
            basic.save()
        else:
            return Response({"error": str(basic.errors)}, status=status.HTTP_400_BAD_REQUEST)
        
        contact = ContactSerializer(data=new_data)
        if contact.is_valid():
            contact.prospect = basic.id
            contact.save()
        else:
            return Response({"error": str(contact.errors)}, status=status.HTTP_400_BAD_REQUEST)

        academic = AcademicSerializer(data=new_data)
        if academic.is_valid():
            academic.prospect = basic.id
            academic.save()
        else:
            return Response({"error": str(academic.errors)}, status=status.HTTP_400_BAD_REQUEST)

        full_data = {
            **basic,
            **contact,
            **academic
        }

        return Response(
            full_data,
            status=status.HTTP_201_CREATED
        )