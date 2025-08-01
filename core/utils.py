from catalog.models import ServiceCategory
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from urllib.parse import urlencode
from orders.utils import Cart
from chat.models import Ticket, TicketMessage

def get_base_info(request):
    maincategories = ServiceCategory.objects.filter(parent__isnull=True)
    cart_created = None
    if request.user.is_authenticated:
        ticket, created = Ticket.objects.get_or_create(user=request.user, status='new')
        ticket = Ticket.objects.prefetch_related('messages').get(id=ticket.id)
        cart = request.user.orders.filter(status='new').first()
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        ticket, created = Ticket.objects.prefetch_related('messages').get_or_create(session_key=session_key, status='new')
        ticket = Ticket.objects.prefetch_related('messages').get(id=ticket.id)
        cart = Cart(request)
        cart_created = cart.get_created_date()
    result = {'maincategories': maincategories, 'cart': cart, 'cart_created_at': cart_created, 'chat': ticket}
    return result

def send_activation_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    activation_link = request.build_absolute_uri(
        reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
    )

    subject = 'Підтвердження реєстрації на сайті'

    message = (
        "Вас вітає команда нашого сервісу!\n\n"
        "Дякуємо за реєстрацію на нашому сайті. Щоб завершити створення акаунта, "
        "потрібно підтвердити свою електронну адресу.\n\n"
        "Для цього просто перейдіть за посиланням нижче:\n\n"
        f"{activation_link}\n\n"
        "Це посилання буде дійсним лише протягом обмеженого часу. "
        "Після активації ви зможете повноцінно користуватись усіма можливостями нашого сервісу.\n\n"
        "Якщо ви не реєстрували акаунт на нашому сайті — просто проігноруйте цей лист.\n\n"
        "З найкращими побажаннями,\n"
        "Команда підтримки"
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def send_confirm_email(request, user, new_email):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    query_string = urlencode({'new_email': new_email})
    activation_link = request.build_absolute_uri(
        reverse('change_email_confirm', kwargs={'uidb64': uid, 'token': token})
    ) + '?' + query_string

    subject = 'Підтвердження зміни електронної пошти'

    message = (
        "Вас вітає команда нашого сервісу!\n\n"
        "Ви запросили зміну електронної адреси у вашому акаунті.\n\n"
        "Для підтвердження нової електронної адреси перейдіть за посиланням:\n\n"
        f"{activation_link}\n\n"
        "Якщо ви не робили цей запит, просто ігноруйте цей лист.\n\n"
        "З повагою,\n"
        "Команда підтримки"
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_email] )
