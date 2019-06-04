from django.urls import path
from .views import SignUp, edit_profile

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]