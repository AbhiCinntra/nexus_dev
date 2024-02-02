from django.urls import path
from .views import *

urlpatterns = [
    path('users/create', create_user),
    path('users/login', login_user),
    path('users/verify', verify_user),
    path('users/one', one_user),
    path('users/all', all_user),
    path('users/all_filter_page', all_filter_page_user),
    path('users/update', update_user),
]
