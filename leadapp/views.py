from django.shortcuts import render

from leadapp.serializers import AcademicSerializer, ContactSerializer, LeadSerializer
from .models import Lead, Contact, AcademicReq
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .helpers import get_agent

# Create your views here.


class GetUnclaimed(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''
        View to get all leads claimed by user:
        '''

        agent = get_agent(request.user)

        queryset_basic = Lead.objects.filter(claimed_by=agent).all()
        serialized_basic = LeadSerializer(queryset_basic, many=True)

        return Response(
            serialized_basic.data,
            status=status.HTTP_302_FOUND
        )


class GetIndClaimed(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''
        View to get individual leads claimed by user:
        '''

        agent = get_agent(request.user)

        queryset_basic = Lead.objects.get(pk=id)
        if agent != queryset_basic.claimed_by:
            return Response(
                {
                    "error": "You are not authorised to view this lead."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        serialized_basic = LeadSerializer(queryset_basic, many=True)

        # For other types:

        queryset_contact = Contact.objects.filter(claimed_by=agent).first()
        serialized_contact = ContactSerializer(queryset_contact)

        queryset_academic = AcademicReq.objects.filter(claimed_by=agent).first()
        serialized_academic = AcademicSerializer(queryset_academic)

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        '''
        View to claim a Lead:
        '''
        ret_key = request.data.get('id')
        agent = get_agent(request.user)
        lead = Lead.objects.get(pk=ret_key)
        lead.claimed_by = agent

        contact = Contact.objects.filter(prospect=lead).first()
        contact.claimed_by = agent
        contact.save()

        academic = AcademicReq.objects.filter(prospect=lead).first()
        academic.claimed_by = agent
        academic.save()

        lead.save()
        serialized = LeadSerializer(lead)
        return Response(
            serialized.data,
            status=status.HTTP_200_OK
        )
