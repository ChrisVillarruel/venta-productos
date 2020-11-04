from django.db import models
from django.conf import settings

# info
# auto_now_add: me permite obtener por una unica vez el registro de la fecha
# auto_now: Este al ir actualizando los datos la fecha va ir cambiando
# related_name: para indicarle a django el nombre de la realción y evitar posibles errores
# settings.AUTH_USER_MODEL: se utiliza para buenas practica de django, que indica que si tenemos un modelo
# user personalizado, debemos hacer referencia al AUTH_USER_MODEL que se personalizo
# abstract: se esta utilizando una abstraccion para poder implementar este modelo, a los demas modelos del sistema


class BaseModel(models.Model):
    user_creation = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_creation',
        null=True,
        blank=True
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_updated',
        null=True,
        blank=True
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
