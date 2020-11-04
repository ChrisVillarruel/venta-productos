from datetime import datetime

from django.forms import *

from core.employe.models import Category, Product, Client, Sale


class CategoryForm(ModelForm):

    # -> utilizamos un metodo init para que al inicializar mi formulario me
    # -> integre de manera automatica los widgets que son comunes en mi formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -> realizamos una iteracion de mis campos visibles con la variable self, que hace
        # -> referencia a todos mis formularios de categoria
        for formulario in self.visible_fields():
            formulario.field.widget.attrs['class'] = 'form-control'
            formulario.field.widget.attrs['autocomplete'] = 'off'

        # -> le agregamos un autofocus a mi formulario name
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        # exclude = [''] -> puedo excluir formularios
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese una categoria',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    'rows': 3,
                    'cols': 3,
                }
            )
        }
        exclude = ['user_creation', 'user_updated']

    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) < 6:
            # add_error me permite hacer validaciones adicionales a la que tiene el formulario
            # hacinedo referencia con self, agregamos un error colocando como parametro
            # el componente al que quiero que le llegue el error y el mensaje de error
            # self.add_error('name', 'El nombre de la categoria debe de tener por lo menos mas 6 caracteres.')

            # ValidationError este tipo de validacion es cuando se detecta un error en cualquiera de
            # los formularios, sin especificar el componente al que yo quiero que dispare el error
            raise forms.ValidationError('El nombre de la categoria debe de tener por lo menos mas 6 caracteres.')
        return cleaned


class ProductForm(ModelForm):

    # definimos un metodo que se ejecutara siempre que el formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # iteramos los widgets mas comunes y reptibles y sean apliacdos al todos los formularios
        for formulario in self.visible_fields():
            formulario.field.widget.attrs['class'] = 'form-control'
            formulario.field.widget.attrs['autocomplete'] = 'off'
        # -> le agregamos un autofocus a mi formulario name
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre de un Producto'
                }
            ),
        }


class ClientForm(ModelForm):

    # definimos un metodo que se ejecutara siempre que el formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # iteramos los widgets mas comunes y reptibles y sean apliacdos al todos los formularios
        for formulario in self.visible_fields():
            formulario.field.widget.attrs['class'] = 'form-control'
            formulario.field.widget.attrs['autocomplete'] = 'off'
        # -> le agregamos un autofocus a mi formulario name
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del Cliente',
                }
            ),
            'supername': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos del Cliente',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese el dni del Cliente',
                }
            ),
            'birthday': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'sexo': Select()
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TestForm(Form):
    # con jquery
    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    # con el plugin select2
    search = ModelChoiceField(queryset=Category.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%',
    }))

class SaleForm(ModelForm):

    # definimos un metodo que se ejecutara siempre que el formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # iteramos los widgets mas comunes y reptibles y sean apliacdos al todos los formularios
        for formulario in self.visible_fields():
            formulario.field.widget.attrs['class'] = 'form-control'
            formulario.field.widget.attrs['autocomplete'] = 'off'

        self.fields['cli'].widget.attrs['class'] = 'form-control select2'

        # forma dos para crear un formulario
        self.fields['date_joined'].widget.attrs = {
            'autocomplete': 'off',
            'class': 'form-control datetimepicker-input',
            'id': 'date_joined',
            'data-target': '#date_joined',
            'data-toggle': 'datetimepicker'
        }

        self.fields['subtotal'].widget.attrs = {
            'class': 'form-control',
            'disabled': True,
        }

        self.fields['total'].widget.attrs = {
            'class': 'form-control',
            'disabled': True,
        }

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={
                'style': 'width: 100%',
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                }
            ),
            'iva': TextInput()
        }
