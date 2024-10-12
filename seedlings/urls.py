from django.urls import path
from seedlings.views import SeedlingList

urlpatterns = (
    path('', SeedlingList.as_view(), name='list'),
)