# librerias
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

# modulos
from core.employe.models import Client
from core.employe.forms import ClientForm
from core.employe.mixins import IsSuperuserMixin


class ClientView(IsSuperuserMixin, TemplateView):
    model = Client
    template_name = 'client/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                print(data)
                for i in Client.objects.all():
                    data.append(i.toJSON())
            # insertar
            elif action == 'add':
                cliente = Client()
                cliente.name = request.POST['name']
                cliente.supername = request.POST['supername']
                cliente.dni = request.POST['dni']
                cliente.birthday = request.POST['birthday']
                cliente.address = request.POST['address']
                cliente.sexo = request.POST['sexo']
                cliente.save()
            # actualizar
            elif action == 'edit':
                cliente = Client.objects.get(pk=request.POST['id'])
                cliente.name = request.POST['name']
                cliente.supername = request.POST['supername']
                cliente.dni = request.POST['dni']
                cliente.birthday = request.POST['birthday']
                cliente.address = request.POST['address']
                cliente.sexo = request.POST['sexo']
                cliente.save()
            # eliminar
            elif action == 'delete':
                cliente = Client.objects.get(pk=request.POST['id'])
                cliente.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            print(data)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['list_url'] = reverse_lazy('erp:client')
        context['entity'] = 'Listado de Clientes'
        context['form'] = ClientForm()
        return context
