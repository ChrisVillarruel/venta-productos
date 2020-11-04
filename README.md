# Aplicación: venta-productos

Esta aplicación es la versión estable de [Dashboard-con-django-3](https://github.com/ChrisVillarruel/Dashboard-con-Django-3) que también se encuentra en mi
GitHub por si desea ver la documentación más detallada.

La versión que usted instalara es la última versión (version_1.1.4 del día 2 de noviembre del 2020).
Para más información acceda al repositorio [Dashboard-con-django-3](https://github.com/ChrisVillarruel/Dashboard-con-Django-3/tree/version_1.1.4) en la rama version_1.1.4. 

Esta versión se creó con el fin de que otros desarrolladores puedan acceder y testear la aplicación
instalando todas las dependencias, librerías y APIS que están siendo implementadas en la aplicación
y no haya errores en el momento de probar el código y compilar la aplicación. Dado que la aplicación
aún se encuentra en desarrollo la aplicación aun no puede ser alojada en un dominio web, sin
embargó esta versión ya puede ser testeada de manera local en su computadora dado que gran
parte del proyecto ya es utilizable.

- Herramientas debería de tener instaladas.
  - Python 3 de preferencia la última versión.
  - Deberá de tener instalado el IDE de sqlLiteStdio con la versión más reciente para
poder acceder a la base de datos de la aplicación.

*Por ahora solo contamos con el soporte de SQLite pues es el gestor de base datos que Django utiliza
por defecto.*


## Pasos para la inicializar la aplicación.

- Descargamos o clonamos la aplicación. 
- En cualquier parte de su sistema usted creara un directorio vacío. *Yo creare el directorio en
descargas y nombrare al directorio **“root”***
- Dentro del directorio root, usted moverá o copiara el directorio que se creo al descargar en la aplicación.
- Ahora abriremos la consola de Windows y por pura consola *CMD* nos dirigiremos al directorio que usted
creo en este caso **“root”**.
- Estando dentro de root crearemos un entorno virtual de Python con el siguiente comando.

```bash
python -m venv env
```
- Después de haber creado el entorno virtual desde la consola entraremos al directorio **env** y
del directorio env entramos al directorio **Script**.

- Dentro del directorio Script escribirá el comando ***“activate”*** para activar el entorno **virtual**.

- Ahora desde la misma consola de Windows se regresara al directorio **root**

- Ya estando dentro del directorio root, se dirigirá al directorio donde estan los archivos de la aplicación. 

- Ahora procedemos a escribir el siguiente comando para instalar todas las dependencias,
librerías y APIS que la aplicación necesita para que pueda ser ejecuta de manera local.

```bash
pip install -r requirements/requirements.txt
```
- Después escribirnos el siguiente comando.
```bash
python manage.py runserver 
```
- Si todo salio correcto debera de mostrarle la consola lo siguiente.
```bash
System check identified no issues (0 silenced).
November 03, 2020 - 20:36:27
Django version 3.0.4, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
- Ahora para detener la ejecución con "*ctrl + c*", detiene la ejecución y procedemos a migrar todos los datos del sistema. ***Escriba los siguientes comandos***: 
```bash
python manage.py makemigrations
python manage.py migrate
```
- Al finalizar la migración, inmediatamente después crea un super usuario. ***Escriba el siguiente comando***:
```bash
python manage.py createsuperuser 
```
- Django le solicitara las credenciales para ser un super usuario:
- Después de haber creado el super usuario, procedemos a ejecutar la aplicación:
```bash
python manage.py runserver
```
- Si todo salio correcto la consola le deberá de mostrar lo siguiente:
```bash
System check identified no issues (0 silenced).
November 03, 2020 - 20:36:27
Django version 3.0.4, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

