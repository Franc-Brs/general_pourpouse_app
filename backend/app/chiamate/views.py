"""
Views for the chiamate APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Chiamate
from chiamate import serializers


class ChiamateViewSet(viewsets.ModelViewSet):
    """
    View for manage chiamate APIs.
    """
    serializer_class = serializers.ChiamateSerializer
    queryset = Chiamate.objects.all().order_by('id')
    # needs to use token auth
    authentication_classes = (TokenAuthentication,)
    # needs to be auth
    permission_classes = (IsAuthenticated,)
