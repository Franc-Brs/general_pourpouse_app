"""
Mapping for the chiamate app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from chiamate import views


router = DefaultRouter()
router.register('chiamate', views.ChiamateViewSet)

app_name = 'chiamate'

urlpatterns = [
    path('', include(router.urls)),
]
