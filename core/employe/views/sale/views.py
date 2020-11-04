from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db import transaction
import json

from core.employe.models import Sale, Product, DetSale
from core.employe.mixins import ValidatePermissionRequiredMixin
from core.employe.forms import SaleForm


class SaleCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('index')
    permission_required = ('employe.add_sale')
    url_redirect = reverse_lazy('index')

    # Desactivamos el sistema de seguridad de django para el envio de post
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                # realizamos una consula haciendo referencia a la variable term que es la que va a solicitar la busqueda
                products = Product.objects.filter(name__icontains=request.POST['term'])
                for product in products[0:10]:
                    item = product.toJSON()
                    item['value'] = product.name
                    data.append(item)

            elif action == 'add':

                # Creamos una transacción atomica para validar si llegara a haber
                # un error en el bloque de codigo interno o externo y se revierte
                # la transacción y así se evita crear el registro
                with transaction.atomic():

                    # recuperamos los valores convertidos a tipo json, utilizando json.loads()
                    vents = json.loads(request.POST['vents'])
                    # insertamos los datos al modelo sale
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()

                    # iteramos los productos para insertar los datos al model detSale
                    for i in vents['products']:
                        det = DetSale()
                        # creamos la primera relacion con el modelo sale
                        det.sale_id = sale.id
                        # creamos la segunda relacion con el modelo Product
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        # guardamos los datos
                        det.save()
            else:
                data['error'] = 'Error de acción, no se pudo localizar la acción actual, notificaselo al desarrollador'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una venta'
        context['entity'] = 'Ventas'
        context['action'] = 'add'
        return context
