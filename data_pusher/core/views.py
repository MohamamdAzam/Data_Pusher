import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from .models import Account
from .tasks import send_data_to_destination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='5/s', method='POST', block=True)
def handle_incoming_data(request):
    if request.content_type != 'application/json':
        return Response({'success': False, 'message': 'Invalid Data'}, status=400)

    token = request.headers.get('CL-X-TOKEN')
    if not token:
        return Response({'success': False, 'message': 'Unauthenticated'}, status=401)

    account = Account.objects.filter(app_secret_token=token).first()
    if not account:
        return Response({'success': False, 'message': 'Unauthenticated'}, status=401)

    data = request.data  # Use `request.data` with @api_view instead of `json.loads(request.body)`
    for destination in account.destinations.all():
        send_data_to_destination.delay(destination.id, data)

    return Response({'success': True, 'message': 'Data Received'})
