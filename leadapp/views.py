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

class ViewClaimed(APIView):
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated)

    def get(self, request):
        '''
        View to get all leads claimed by user:
        '''

        agent = get_agent(request.user)
        
        queryset_basic = Lead.objects.filter(claimed_by = agent).all()
        serialized_basic = LeadSerializer(queryset_basic, many=True)

        # For other types:

        # queryset_contact = Contact.objects.filter(claimed_by = agent).all()
        # serialized_contact = ContactSerializer(queryset_contact, many=True)

        # queryset_academic = AcademicReq.objects.filter(claimed_by = agent).all()
        # serialized_academic = AcademicSerializer(queryset_academic, many=True)
        

        # return_data = {
        #     **serialized_basic.data,
        #     **serialized_contact.data,
        #     **serialized_academic.data
        # }

        return Response(
            serialized_basic.data,
            status=status.HTTP_302_FOUND
        )

class GetIndClaimed(APIView):
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated)

    def get(self, request):
        '''
        View to get all leads claimed by user:
        '''

        agent = get_agent(request.user)
        
        queryset_basic = Lead.objects.get(pk=id)
        if agent != queryset_basic.claimed_by:
            return Response(
                {
                    "error": "You are not authorised to view this lead."
                },
                status = status.HTTP_401_UNAUTHORIZED
            )

        serialized_basic = LeadSerializer(queryset_basic, many=True)

        # For other types:

        queryset_contact = Contact.objects.filter(claimed_by = agent).all()
        serialized_contact = ContactSerializer(queryset_contact, many=True)

        queryset_academic = AcademicReq.objects.filter(claimed_by = agent).all()
        serialized_academic = AcademicSerializer(queryset_academic, many=True)
        

        return_data = {
            **serialized_basic.data,
            **serialized_contact.data,
            **serialized_academic.data
        }

        return Response(
            return_data,
            status=status.HTTP_302_FOUND
        )


    

class ClaimLead(APIView):
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated)
    
    def post(self, request, id:int):
        '''
        View to claim a Lead:
        '''
        agent = get_agent(request.user)
        lead = Lead.objects.get(pk=id)
        lead.claimed_by = agent
        
        contact = Contact.objects.filter(prospect = lead).all()
        for item in contact:
            item.claimed_by = agent
            item.save()

        academic = AcademicReq.objects.filter(prospect = lead).all()
        for item in academic:
            item.claimed_by = agent
            item.save()

        lead.save()
        serialized = LeadSerializer(lead)
        return Response(
            serialized.data,
            status=status.HTTP_200_OK
        )

