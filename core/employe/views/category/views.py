from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse_lazy

from core.employe.models import Category
from core.employe.forms import CategoryForm
from core.employe.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin

# implementamos mixin


class CategoryListView(ValidatePermissionRequiredMixin, ListView):
    # declaramos el permiso requeirdo para acceder a esta vista
    permission_required = ('employe.change_category')
    # -> le indicamos nuestro modelo a utilizar
    model = Category
    # -> le indicamos cual es la plantilla
    template_name = 'category/list.html'
    # -> nombre del context o objeto que hara referencia a esta vista
    context_object_name = 'categories'

    # -> Decoradores permiten alterar de manera dicamica la funcionalidad de un metodo
    # -> csrf_exempt realiza una exepcion que le permite a terceros ver que contiene post
    # -> evitando el algoritmo de seguridad de django
    @method_decorator(csrf_exempt)
    # si el usuario no esta logeado, con un decorador verificara por medio de login_required
    @method_decorator(login_required)
    # -> metodo dispatch
    # -> Este metodo se ejecuta justo antes del comienzo, antes de que se haga la llamada a una vista
    # -> Y se encarga de redireccionar dependiendo el metodo de peticion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def get_queryset(self):
    #     return Category.objects.filter(name__startswith='b')

    # -> Sobreescritura del metodo post en una vista basada en clase
    # Este metodo tiene un sistema de seguridad de django que no permitira que ninguna aplicacion
    # externa pueda ver el metodo post, pero django puede exeptuar este metodo utilizando
    # csrf_exempt que para este metodo post, el sistema de seguridad de django lo va a ignorar

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Category.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'

            # -> para poder saber los parametros que me llegan, utilizo la peticion por POST
            # -> y automaticamente accedo a las variables que me devuelve el metodo POST
            # data = Category.objects.get(pk=request.POST['id']).toJSON()
            # data['name'] = cat.name
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # -> para querer devolver mas de un elemento de un context se define un metodo
    def get_context_data(self, **kwargs):
        # -> creo mi diccionario para que me devuelva diferentes elementos
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categorias'
        context['create_url'] = reverse_lazy('erp:category-create')
        context['list_url'] = reverse_lazy('erp:category-list')
        context['entity'] = 'Listado de Categorias'
        # Tambien le podemos cambiar el object_list para hacer referencia a otra entidad
        # remplazando la anterior "context_object_name"
        # context['categories'] = Product.objects.all()
        return context


class CategoryCreateView(ValidatePermissionRequiredMixin, CreateView):
    # declaramos el permiso requeirdo para acceder a esta vista
    permission_required = 'employe.add_category'
    # si el usuario no tiene el permiso, redireccionalo a la listado de categoria
    url_redirect = reverse_lazy('erp:category-list')
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = url_redirect

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Categoria'
        context['entity'] = 'Crear una Categoria'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class CategoryUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    # declaramos el permiso requeirdo para acceder a esta vista
    permission_required = 'employe.change_category'
    # si el usuario no tiene el permiso, redireccionalo a la listado de categoria
    url_redirect = reverse_lazy('erp:category-list')
    model = Category
    form_class = CategoryForm
    template_name = "category/create.html"
    success_url = url_redirect

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # para que django no piense que se va a crear un nuevo registro
        # con el metodo dispatch vamos a tomar la instancia actual y le vamos a
        # indicar a django que es un registro que se quiere actualizar
        # por el metodo post
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # -> recuperamos la variable action en mi metodo pos, para indicarle que es lo que va hacer
            print(request.POST)
            action = request.POST['action']
            if action == 'edit':
                # recuperamos los datos completos del formulario
                # form = CategoryForm(request.POST)
                # tambien podemos utilizar get_form(), hace exactamente lo mismo
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        print(self.object)
        print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Categoria'
        context['list_url'] = self.success_url
        context['entity'] = 'Actuliazar Categoria'
        context['action'] = 'edit'
        return context


class CategoryDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    # declaramos el permiso requeirdo para acceder a esta vista
    permission_required = 'employe.delete_category'
    # si el usuario no tiene el permiso, redireccionalo a la listado de categoria
    url_redirect = reverse_lazy('erp:category-list')
    model = Category
    template_name = 'category/delete.html'
    success_url = url_redirect

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # tomamos la instancia actual a eliminar
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # utilizamos el metodo delete del orm de django para eliminar el registro
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar una Categoria'
        context['list_url'] = self.success_url
        context['entity'] = 'Eliminar Categoria'
        return context

# Este vista me permitira verificar si mi formulario es valido o no


class CategoryFormView(IsSuperuserMixin, FormView):
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('erp:category-list')

    # si el formulario trabaja de manera correcta, trabajamos con el metodo form_valid
    def form_valid(self, form):
        # print(form.is_valid())
        # print(form)
        return super().form_valid(form)

    # Para ver el error, utilzamos form_invalid
    def form_invalid(self, form):
        # print(form.is_valid())
        # print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Form | Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:category-list')
        context['action'] = 'add'
        return context
