from django.apps import apps


def get_stripe_customer_model():
    return apps.get_model("dj_doc_vault_billing.StripeCustomer")
