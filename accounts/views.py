from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView

class RegisterView(CreateView):
    """
    Представление для регистрации пользователя.
    Использует встроенную форму UserCreationForm.
    После успешной регистрации перенаправляет пользователя на страницу логина.
    """
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')
