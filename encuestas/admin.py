from django.contrib import admin
from .models import Pregunta, Eleccion

# class PreguntaAdmin(admin.ModelAdmin):
#     campos = ['fechaPublicacion', 'textoPregunta']
# Se pueden personalizar los formularios que tenemos en el sitio del admin
# Podemos estructurar los campos, elegir cuales aparecen, etc...

# Se puede usar StackedInLine o TabularInLine (Tabular es una manera mas compacta)
class EleccionInsertada(admin.TabularInline):
    model = Eleccion
    extra = 1

class PreguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Texto de la pregunta', {'fields': ['textoPregunta']}),
        ('Información de la fecha', {'fields': ['fechaPublicacion']}),
    ]
    # Podemos hacer que las elecciones se añadan una vez creas la pregunta:
    inlines = [EleccionInsertada]
    # Con el list_display podemos elegir que datos se muestran en la pagina de inicio del admin
    list_display = ('textoPregunta', 'fechaPublicacion', 'publicadaRecientemente')
    # list_filter añade un filtro en el lateral que filtra los resultados dependiendo del tipo de dato que sean
    # En este caso al filtrar por fecha, puedes elegir que tan antigua es la pregunta
    list_filter = ['fechaPublicacion']

# Hay un metodo que se puede usar para decorar (@admin.display()). Para usarlo se aplica en el modelo
# del que queremos hacer que tenga un formato

admin.site.register(Pregunta, PreguntaAdmin)

# Puedes añadir todos los modelos que quieras a la pagina del administrador
# para gestionarlos
# admin.site.register(Eleccion)