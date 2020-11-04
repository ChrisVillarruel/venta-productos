from config.wsgi import *
from core.employe.models import Category
import random

# pruebas de querys

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p'
            'q','r','s','t','u','w','x','y','z']

# se creo un ciclo que me permitira insertar 6000 registros de forma aleatoria tomando como referencia a la lista letters
for i in range(1,6000):
    name = ''.join(random.choices(letters, k=5))
    while Category.objects.filter(name=name).exists():
        name = ''.join(random.choices(letters, k=5))
    Category(name=name).save()
    print(f'Guardando registro {i}.')


# # -> select * from Type
# query = Type.objects.all()

# # -> insert
# # -> creamos el objeto Type
# insert = Type()
# # -> seleccionamos un atributo de la tabla, simpre y cuando no sea nulo
# insert.types = 'Presidente'
# # -> guardamos los cambios
# insert.save()


# # -> forma dos de insertar
# insert = Type(types='Presidente').save()

# # -> busqueda por objetos por medio de id o pk del atributo utilizando GET
# consult = Type.objects.get(pk=2)

# # -> para eliminar un registro, con el atributo get, tomamos el registro y lo
# # -> almacenamos en una variable y esa varible la tomamos para eliminar el registros
# consult.delete()

# # -> atributo filter me permite filtrar los datos de la entidad
# # -> contains es en sql like
# obj = Type.objects.filter(types__contains='A')

# # -> atributo startswith, las que comiensen con una letra
# # -> no importa si es mayuscula o minuscula
# obj = Type.objects.filter(types__startswith='p')

# # -> tambien las que terminen con, endswith
# obj = Type.objects.filter(types__endswith='a')

# # -> si queremos un valor exactamente igual, exact
# obj = Type.objects.filter(types__exact='Accionista')

# # -> si se quiere filtrar con solo un par de registros, seria con in
# obj = Type.objects.filter(types__in=['Accionistas', 'Presidente'])

# # -> si queremos contar los resgitros que nostros tenemos seria con count
# obj = Type.objects.filter(types__in=['Accionistas', 'Presidente']).count()

# # -> si queremos ver el codigo en sql se debe de poner al final query
# obj = Type.objects.filter(types__contains='p').query

# # -> metodo exlude, me permite hacer una consulta o filtrado pero me permite
# # -> excluir un registro que no desee ver por medio de su id
# obj = Type.objects.filter(types__contains='p').exclude(id=4)
# obj = Type.objects.filter(types__endswith='a').exclude(id=4)

# # -> Tambien podemos interar el filtrado o objetos orm de django
# for r in Type.objects.filter(types__startswith='P')[:2]:
#     print(r)

# for r in Type.objects.all():
#     print(r)

# # -> ejemplo de subconsulta
# obj = Employe.objects.filter(type_id=1)

# # -> para mas informacion, buscar en la documentacion de django
# # ---> https://docs.djangoproject.com/en/3.1/topics/db/queries/
