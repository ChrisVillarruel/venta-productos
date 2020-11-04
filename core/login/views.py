from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, HttpResponseRedirect
from django.views.generic import FormView, RedirectView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
import config.settings as setting


class LoginFormView(LoginView):
    template_name = 'login.html'

    # verificamos si estamos logeados por medio de nuestra instancia actual de dispatch
    def dispatch(self, request, *args, **kwargs):
        # validamos si mi usuario esta logeado
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        print(request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesión'
        return context


class LoginFormView2(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    # verificamos si estamos logeados por medio de nuestra instancia actual de dispatch
    def dispatch(self, request, *args, **kwargs):
        # preguntamos si hay un usuario actual logeado
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    # validamos si los formularios son correctos
    def form_valid(self, form):
        """ Login me va a permitir iniciar sesion, con la instancia actual y el usuario que se obtuvo al quererce logear """
        login(self.request, form.get_user())
        return redirect('erp:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesión'
        return context


class LogoutRedirectView(RedirectView):
    pattern_name = 'user:user-login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
