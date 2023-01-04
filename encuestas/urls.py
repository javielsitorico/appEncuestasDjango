from django.urls import path
from . import views

# Hay que añadir un 'namespace' en caso de que en el proyecto hubiera mas de una aplicaion y 
# algunas vistas se llamaran igual que otras

app_name = 'encuestas'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetallesView.as_view(), name='detalles'),
    path('<int:pk>/resultados', views.ResultadosView.as_view(), name='resultados'),
    path('<int:idPregunta>/votar', views.votar, name='votar'),
    # path('<int:idPregunta>/responder', views.responder, name='responder'),
]