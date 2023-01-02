from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Eleccion, Pregunta
from django.utils import timezone

# Las vistas son unas funciones que llamara la aplicacion al recibir urls
# haciendo un HttpRequest

# def index(request):
#     listaPreguntasRecientes = Pregunta.objects.order_by('-fechaPublicacion')[:5]
#     contexto = {
#         'listaPreguntasRecientes': listaPreguntasRecientes,
#     }
#     # El contexto es el conjunto de variables que le pasamos al metodo
#     # para que renderice el template con ellas

#     # Se puede devolver un HttpResponse o usar el metodo render que tambien
#     # devuelve un objeto del mismo tipo, pero nos ahorramos usar algunos imports

#     # template = loader.get_template('encuestas/index.html')
#     # return HttpResponse(template.render(contexto, request))
#     return render(request, 'encuestas/index.html', contexto)

# def detalles(request, idPregunta):
#     # Todo este bloque de codigo se puede abreviar usando get_object_or_404:
#     # try:
#     #     pregunta  = Pregunta.objects.get(pk=idPregunta)
#     # except Pregunta.DoesNotExist:
#     #     raise Http404('La pregunta no existe :(')
#     # return render(request, 'encuestas/detalles.html', {'pregunta': pregunta})
#     # -------------------
#     pregunta = get_object_or_404(Pregunta, pk=idPregunta)
#     return render(request, 'encuestas/detalles.html', {'pregunta': pregunta})
#     # Tambien se puede usar get_list_or_404 en vez de get_object_or_404, la diferencia es que 
#     # uno usa get y otro usa filter. Devuelve un 404 si la lista esta vacia

# def resultados(request, idPregunta):
#     pregunta = get_object_or_404(Pregunta, pk=idPregunta)
#     return render(request, 'encuestas/resultados.html', {'pregunta': pregunta})

# # Como las vistas detalles y resultados son muy cortas y parecidas, se pueden compactar
# # Para esto se puede usar el sistema de views genericas:

class IndexView(generic.ListView):
    template_name = 'encuestas/index.html'
    context_object_name = 'listaPreguntasRecientes'

    def get_queryset(self):
        return Pregunta.objects.filter(fechaPublicacion__lte=timezone.now()).order_by('-fechaPublicacion')[:5]

class DetallesView(generic.DetailView):
    model = Pregunta
    template_name = 'encuestas/detalles.html'

    def get_queryset(self):
        return Pregunta.objects.filter(fechaPublicacion__lte = timezone.now())

class ResultadosView(generic.DetailView):
    model = Pregunta
    template_name = 'encuestas/resultados.html'

# ListView y DetailView son dos vistas genericas que nos ofrece django
# En concreto, una te muestra una lista de objetos y la otra los detalles de un objeto
# que le pases

# Las vistas genericas necesitan saber sobre que modelo van a trabajar, y esto se le indica
# con el atributo 'model'
# La vista detallada espera recibir desde la url la pk del objeto, es por eso que en urls.py hemos
# cambiado de idPregunta a pk
# A estas vistas tambien hay que indicarle el nombre del template con template_name, aunque tambien
# se puede usar el nombre por defecto que genera django automaticamente



def votar(request, idPregunta):
    pregunta = get_object_or_404(Pregunta, pk=idPregunta)
    try:
        opcionElegida = pregunta.eleccion_set.get(pk=request.POST['eleccion'])
    except (KeyError, Eleccion.DoesNotExist):
        # Si no existe, volvemos al formulario
        return render(request, 'encuestas/detalles.html', {
            'pregunta': pregunta,
            'mensageError': "La opción elegida no es válida.",
        })
    else:
        opcionElegida.votos += 1
        opcionElegida.save()
        # Hay que devolver la respuesta una vez se han tratado correctamente los datos POST
        return HttpResponseRedirect(reverse('encuestas:resultados', args=(pregunta.id,)))