from django.urls import path
from .views import RegisterView, CustomLogoutView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout_user/', CustomLogoutView.as_view(), name='logout_user'),

]
