from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .api.payments import PaymentAPI
from .api.tickets import InvoiceSummaryAPI, TicketAPI, stripe_call_back

router = SimpleRouter()

router.register('payments', PaymentAPI, basename='Payment')
router.register('tickets', TicketAPI, basename='Ticket')
router.register('invoices', InvoiceSummaryAPI, basename='Invoice Summary')

urlpatterns = [
    path('', include(router.urls)),
    path('stripe/callback/', stripe_call_back),
]
