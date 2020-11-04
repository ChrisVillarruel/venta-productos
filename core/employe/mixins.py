from django.shortcuts import redirect
from datetime import datetime
from django.contrib import messages

# crearemos una vista basada en clases mixin.
# Esta clase nos permitira validar si el usaurio actual es un super usuario
# la ventaja de utilizar este tipo clase es que tiene un valor de prioridad mayor
# al de otras implementaciones, por lo que siempre se ejecutara primero, antes de
# realizar otra acción


class IsSuperuserMixin(object):
    # este metodo me permitira validar si el usuario actual es super

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'En esta sección unicamente puede acceder el administrador')
        return redirect('/login/')

    # tambien podemos podemos definir nuestros contexto exclusivo para un superusuario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return '/login/'
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'Usted no tiene permiso para realizar la siguiente acción.')
        messages.error(request, 'Para aclarar cualquier duda consulte al administrador del sistema.')
        return redirect(self.get_url_redirect())

    # tambien podemos podemos definir nuestros contexto exclusivo para un superusuario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context
