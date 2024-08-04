from django.contrib import admin
from pos.models import (FonePayPayment, InvoiceSummary, Payment, Settings,
                        StripePayment, Ticket)

admin.site.register(Ticket)
admin.site.register(InvoiceSummary)
admin.site.register(FonePayPayment)
admin.site.register(Payment)
admin.site.register(Settings)

admin.site.register(StripePayment)
