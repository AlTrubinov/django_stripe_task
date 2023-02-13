from django.contrib import admin
from django.urls import path
from store.views import (
    CreateCheckoutSessionView,
    HomePageView,
    ItemPageView,
    SuccessView,
    CancelView,
    stripe_webhook,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', HomePageView.as_view(), name='home-page'),

    path('item/<pk>/', ItemPageView.as_view(), name='item-page'),
    path('buy/<pk>/', CreateCheckoutSessionView.as_view(),
    name='buy-page'),

    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),

    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success', SuccessView.as_view(), name='success'),
]
