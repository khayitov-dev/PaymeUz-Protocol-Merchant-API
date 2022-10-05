from django.urls import path
from .views import PaymentView, checkout_view


urlpatterns = [
    path('pay/', PaymentView.as_view()), # EndPointUrl ga shu manzilni kiritng, agar local da foydalanmoqchi bolsez, ngrok ishlating.
    path('checkout/', checkout_view),
]