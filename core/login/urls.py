from django.urls import path
from core.login.views import *

app_name = 'user'

urlpatterns = [
    path('', LoginFormView.as_view(), name='user-login'),
    path('logout/', LogoutRedirectView.as_view(), name='user-logout'),
]
