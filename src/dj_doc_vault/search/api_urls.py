from django.urls import path

from dj_doc_vault.search import api_views

app_name = "dj_doc_vault-search"

urlpatterns = [
    path(
        "search/",
        api_views.search_view,
        name="search",
    ),
]
