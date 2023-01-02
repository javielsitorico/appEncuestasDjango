import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Pregunta

def crearPregunta(textoPregunta, dias):
    # Creamos una pregunta con el texto dado y un numero de dias que sera la diferencia
    # de dias entre la fecha de publicacion y el dia de hoy. La diferencia sera negativa
    # si es una pregunta antigua
    tiempo = timezone.now() + datetime.timedelta(days=dias)
    return Pregunta.object.create(textoPregunta=textoPregunta, fechaPublicacion=tiempo)

class ModeloPreguntasTests(TestCase):
    # El nombre de los metodos debe empezar por test
    def test_publicadaRecientemente_preguntaFuturo(self):
        tiempo = timezone.now() + datetime.timedelta(days=30)
        pregunta = Pregunta(fechaPublicacion=tiempo)
        self.assertIs(pregunta.publicadaRecientemente(), False)
    
    def test_publicadaRecientemente_preguntaAnitgua(self):
        tiempo = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        pregunta = Pregunta(fechaPublicacion=tiempo)
        self.assertIs(pregunta.publicadaRecientemente(), True)
    
    def test_publicadaRecientemente_preguntaReciente(self):
        tiempo = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pregunta = Pregunta(fechaPublicacion=tiempo)
        self.assertIs(pregunta.publicadaRecientemente(), False)

class VistaIndexTests(TestCase):
    def test_sinPreguntas(self):
        # Si no existe la pregunta, mostramos un texto bonito
        respuesta = self.client.get(reverse('encuestas:index'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Todavía no hay encuestas')
        self.assertQuerysetEqual(respuesta.contexto['listaPreguntasRecientes'], [])

    def test_preguntaAntigua(self):
        # Las preguntas que tengan una fecha de publicacion anterior salen en el index
        pregunta = crearPregunta('Pregunta antigua', -30)
        respuesta = self.client.get(reverse('encuestas:index'))
        self.assertQuerysetEqual(respuesta.context['listaPreguntasRecientes'], [pregunta])
    
    def test_preguntaFuturo(self):
        # Las preguntas con una fecha de publicacion en un futuro, no aparecen
        # en la pagina principal
        crearPregunta('Pregunta futuro', 30)
        respuesta = self.client.get(reverse('encuestas:index'))
        self.assertContains(respuesta, 'Todavía no hay encuestas')
        self.assertQuerysetEqual(respuesta.contexto['listaPreguntasRecietes'], [])
    
    def test_preguntas_futuroAntigua(self):
        pregunta = crearPregunta('Pregunta antigua', -30)
        crearPregunta('Pregunta futuro', 30)
        respuesta = self.client.get(reverse('encuestas:index'))
        self.assertQuerysetEqual(respuesta.context['listaPreguntasRecientes'], [pregunta])

    def test_variasPreguntasAntiguas(self):
        pregunta1 = crearPregunta('Pregunta antigua 1', -30)
        pregunta2 = crearPregunta('Pregunta antigua 2', -10)
        respuesta = self.client.get(reverse('encuestas:index'))
        self.assertQuerysetEqual(respuesta.context['listaPreguntasRecientes'], [pregunta1, pregunta2])
    
class VistaDetallesTests(TestCase):
    def test_preguntaFuturo(self):
        preguntaFuturo = crearPregunta('Pregunta futuro', 30)
        url = reverse('polls:detail', args=(preguntaFuturo.id,))
        respuesta = self.client.get(url)
        self.assertEqual(respuesta.status_code, 404)
    
    def test_preguntaAntigua(self):
        preguntaAntigua = crearPregunta('Pregunta antigua', -5)
        url = reverse('encuestas:detalles', args=(preguntaAntigua.id))
        respuesta = self.client.get(url)
        self.assertContains(respuesta, preguntaAntigua.textoPregunta)

# Django te proporciona un cliente para hacer tests (a nivel de vistas)
# Se puede usar para eso este fichero tests.py o la shell de python