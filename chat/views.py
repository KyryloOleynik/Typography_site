from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Ticket, TicketMessage
from core.utils import get_base_info

# Create your views here.
@require_POST
def send_message(request):
    message = request.POST.get('message', '').strip()

    if not message:
        return JsonResponse({'error': 'Повідомлення не може бути порожнім.'}, status=400)

    if request.user.is_authenticated:
        ticket = request.user.tickets.filter(status='new').first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
        ticket = Ticket.objects.filter(session_key=request.session.session_key, status='new').first()

    if not ticket:
        return JsonResponse({'error': 'Активний чат не знайдено.'}, status=404)

    message_obj = TicketMessage.objects.create(ticket=ticket, user=request.user if request.user.is_authenticated else None, message=message)

    return JsonResponse({'message': message_obj.message, 'message_time': message_obj.created_at.isoformat(), 'message_id': message_obj.id})

def upload_chat(request):
    if request.method == "GET":
        ticket = get_base_info(request).get('chat')
        if not ticket:
            return JsonResponse({'error': 'Чат не знайдено'}, status=404)

        data = {
            'messages': [
                {
                    'message': message.message,
                    'role': message.role,
                    'created_at': message.created_at_iso,
                    'id': message.id,
                }
                for message in ticket.messages.all()
            ]
        }
        return JsonResponse(data)