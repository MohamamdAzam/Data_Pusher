from django.urls import path
from .views import handle_incoming_data

urlpatterns = [
    path('incoming_data/', handle_incoming_data, name='incoming_data'),
]
