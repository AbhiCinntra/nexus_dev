from django.urls import path
from .views import *

urlpatterns = [
    # contacts apis
    path('contacts/create', create_contact),
    path('contacts/one', one_contact),
    path('contacts/all', all_contact),
    path('contacts/all_filter_page', all_filter_page_contact),
    path('contacts/update', update_contact),
    path('contacts/delete', delete_contact),
    
    # remarks apis
    path('contacts/remarks/create', create_remarks),
    path('contacts/remarks/all', all_remarks),
]
