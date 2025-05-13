from django.contrib import admin
from dj_doc_vault.billing.models import StripeCustomer

admin.site.register(StripeCustomer)
