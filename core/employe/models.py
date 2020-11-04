from crum import get_current_user
from django.db import models
from datetime import datetime
from core.employe.choices import gender_choices
from config.settings import MEDIA_URL, STATIC_URL
from core.models import BaseModel
from django.forms import model_to_dict


class Category(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Nombre de la Categoria', unique=True)
    desc = models.CharField(max_length=500, verbose_name='Descripcion', null=True, blank=True)

    def __str__(self):
        return self.name.title()

    # implementando la api django-crum
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # obtenemos el usuario asociado en la solicitud actual o anoymusUser si esta vacio
        user = get_current_user()
        # validamos si existe un usuario registrado en la solicitud actual
        if user is not None:
            # validamos si la categoria actual no existe o no tiene un id registrado
            if not self.pk:
                # si no existe, entoces el usurio actual esta creando una nueva categoria
                self.user_creation = user
            else:
                # de lo contrario si existe la categoria actual, entoces el usuario la esta actualizando
                self.user_updated = user
        # guardamos los cambios
        super(Category, self).save()

    # -> definimos un metodo que me permita devolver en formato json los registros de mi modelo
    def toJSON(self):
        # -> forma tradicional de creacion de un diccionario en formaro json
        item = {'id': self.id, 'name': self.name.title(), 'desc': self.desc}
        # -> forma practica de formateo de json utilizando el metodo 'model_to_dict'
        # item = model_to_dict(self, exclude=['']) -> tambien podemos excluir campos que no queramos que se muestren
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'Categoria'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre del Producto', unique=True)
    cate = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoria')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen del Producto')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de Venta')

    def __str__(self):
        return self.name.title()

    def get_image(self):
        # si tiene una imagen que me retorne la imagen
        if self.image:
            return f'{MEDIA_URL}{self.image}'
        # si no entoces retorname una imagen por defecto
        return f'{STATIC_URL}{"img/sinFoto.png"}'

    def toJSON(self):
        item = model_to_dict(self)
        item['cate'] = self.cate.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'Producto'
        ordering = ['id']


class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    supername = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='DNI')
    birthday = models.DateField(default=datetime.now, verbose_name='Fecha de Nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Direccion')
    sexo = models.CharField(max_length=10, choices=gender_choices, default='S/E', verbose_name='Genero')

    def __str__(self):
        return f'{self.name.title()} {self.supername.title()}'

    def toJSON(self):
        item = model_to_dict(self)
        item['sexo'] = {'id': self.sexo, 'name': self.get_sexo_display()}
        item['birthday'] = self.birthday.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'Cliente'
        ordering = ['id']


class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.cli.name.title()} {self.cli.supername.title()}'

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        db_table = 'Venta'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name.title()

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        db_table = 'DeSale'
        ordering = ['id']


# --> Ejemplo de uso de atributos en django

# class Type(models.Model):
#     types = models.CharField(max_length=100, verbose_name='Tipo de Empleado', unique=True)

#     def __str__(self):
#         return self.types.title()

#     class Meta:
#         verbose_name = 'Tipo de Empleado'
#         verbose_name_plural = 'Tipos de Empleados'
#         db_table = 'Tipo'
#         ordering = ['id']

# class Employe(models.Model):
#     name = models.CharField(max_length=150, verbose_name='Nombre')
#     dni = models.CharField(max_length=10, verbose_name='DNI', unique=True)
#     date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
#     date_creation = models.DateTimeField(auto_now=True)
#     date_update = models.DateTimeField(auto_now_add=True)
#     age = models.PositiveIntegerField(default=0)
#     salary = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
#     state = models.BooleanField(default=True)
#     gender = models.CharField(max_length=20)
#     avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', null=True, blank=True)
#     cvitae = models.ImageField(upload_to='cvitae/%Y/%m/%d', null=True, blank=True)
#     # -> relacion llave foranea
#     types = models.ForeignKey(Type, on_delete=models.CASCADE)
#     # -> relacion de muchos a muchos
#     category = models.ManyToManyField(Category)

#     def __srt__(self):
#         return self.name.title()

#     class Meta:
#         verbose_name = 'Empleado'
#         verbose_name_plural = 'Empleados'
#         db_table = 'Empleado'
#         ordering = ['id']
