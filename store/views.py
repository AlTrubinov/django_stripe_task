from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Item
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY




class SuccessView(TemplateView):
    template_name = 'success.html'
 


class CancelView(TemplateView):
    template_name = 'cancel.html'


class HomePageView(ListView):
    model = Item
    context_object_name = "items"
    template_name = 'home.html'


class ItemPageView(DetailView):
    model = Item
    context_object_name = "item"
    template_name = 'item.html'

    def get_context_data(self, **kwargs):
        context = super(ItemPageView, self).get_context_data(**kwargs)
        context.update({
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs['pk'])
        YOUR_DOMAIN = settings.DOMAIN
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            metadata={
                'item_id': item.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_name = session['customer_details']['name']
        item = session['metadata']['item_id']
        # Отправляем сообщение о успешной оплате в консоль
        print(f'Пользователь {customer_name} оплатил товар: {item}. Можно отправлять.')
        print(session)

    return HttpResponse(status=200)
