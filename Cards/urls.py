from django.urls import path
from .views import *

urlpatterns = [
    path('cards/create', create_card),
    path('cards/one', one_card),
    path('cards/all', all_card),
    path('cards/all_filter_page', all_filter_page_card),
    path('cards/update', update_card),
    path('cards/delete', delete_card),
]
