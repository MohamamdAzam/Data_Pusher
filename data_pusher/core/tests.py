from celery import shared_task
import requests
from .models import Destination

@shared_task
def send_data_to_destination(destination_id, data):
    destination = Destination.objects.get(id=destination_id)
    headers = destination.headers
    response = requests.request(destination.http_method, destination.url, json=data, headers=headers)
    return response.status_code
