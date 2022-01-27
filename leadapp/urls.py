from django.urls import path
from views import GetUnclaimed, NewLead, ViewClaimed, GetIndClaimed, ClaimLead

# Include your URLs here:

urlpatterns = [
    path('all/', GetUnclaimed.as_view(), name='unclaimed_views'),       #GET
    path('new/', NewLead.as_view(), name='add_lead'),                   # POST
    path('claimed/', ViewClaimed.as_view(), name='claimed_leads'),      # GET
    path('<int:id>/', GetIndClaimed.as_view(), name='view_claimed'),    # GET
    path('<int:id>/claim', ClaimLead.as_view(), name='claim'),          # POST
]