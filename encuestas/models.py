import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

class Pregunta(models.Model):
    textoPregunta = models.CharField(max_length=255)
    fechaPublicacion = models.DateTimeField('fecha de publicacion')
    # Las clases Field de models pueden recibir un parametro opcional
    # que es un nombre que le puedes dar al campo en caso de querer un nombre 
    # mas descriptivo que el nombre de la propia variable

    # La funcion __str__ se usa en python para devolver los valores de una clase
    # (o los que elijamos) como un string. Es una convencion llamarlo '__str__'
    # Usar este metodo ayuda a Django con funciones que trae por defecto
    def __str__(self):
        return self.textoPregunta

    @admin.display(
        boolean=True,
        ordering='fechaPublicacion',
        description='Publicada Recientemente',
    )

    def publicadaRecientemente(self):
        ahora = timezone.now()
        return ahora - datetime.timedelta(days = 1) <= self.fechaPublicacion <= ahora
    
class Eleccion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    textoEleccion = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.textoEleccion

# Antes de hacer una migracion (makemigration), se puede usar el comando sqlmigrate
# para ver los comandos que python ejecutaria en tu base de datos antes de ejecutarlos
# de verdad

# El comando migrate ejecuta las migraciones que no han sido ejecutadas aun

# Las migraciones te permiten cambiar los modelos de tu aplicacion cuando quieras

# Una vez tenemos creados los modelos, podemos usar la API que nos ofrece Django para
# gestionar la base de datos y los datos en si

# Esta API nos ofrece muchos metodos y palabras clave que podemos usar para consultar
# las bases de datos de una manera simple y rapida. EL método get nops permite consultar
# lo que le pidamos. Ejemplo:
# Pregunta.objects.get(fechaPublicacion__year=current_year)
# el __year (es una keyword) nos permite saber el año de la fecha introducida en la base de datos
# Se usan las doble _ para acceder a campos de la base de datos
# Otro ejemplo:
# Pregunta.objects.get(pk=1)
# La keyword pk nos permite acceder a las claves primarias de manera rapida