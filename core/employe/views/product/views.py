# librerias
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse_lazy

# modulos
from core.employe.models import Product
from core.employe.forms import ProductForm
from core.employe.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin


class ProductListView(ValidatePermissionRequiredMixin, ListView):
    permission_required = ('employe.change_product')
    model = Product
    template_name = 'product/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('erp:product-create')
        context['entity'] = 'Listado de Productos'
        return context


class ProductCreateView(ValidatePermissionRequiredMixin, CreateView):
    permission_required = ('employe.add_product')
    url_redirect = reverse_lazy('erp:product-list')
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('erp:product-list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = ProductForm(request.POST)
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = 'Error al guardar los datos'
            else:
                data['error'] = 'Error de comunicación con el servidor'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Categoria'
        context['list_url'] = self.success_url
        context['entity'] = 'Crear Productos'
        context['action'] = 'add'
        return context


class ProductUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'employe.change_product'
    url_redirect = reverse_lazy('erp:product-list')
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('erp:product-list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'Error de comunicación en el servidor'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Producto'
        context['list_url'] = self.success_url
        context['entity'] = 'Actualizar Producto'
        context['action'] = 'edit'
        return context


class ProductDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    permission_required = 'employe.delete_product'
    url_redirect = reverse_lazy('erp:product-list')
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('erp:product-list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # hacemos referencia a nuestra instancia actual
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            print(request.POST)
            print(request.FILES)
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Producto'
        context['list_url'] = self.success_url
        context['entity'] = 'Eliminar Producto'
        return context
