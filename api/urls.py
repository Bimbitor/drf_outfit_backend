from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [


    path('prendas/', views.PrendaListCreate.as_view()),
    path('combinaciones/', views.CombinacionListCreate.as_view()),
    path('prendas/<int:id>/', views.PrendasRetrieveUpdateDestroy.as_view()),
    path('combinaciones/<int:id>/', views.CombinacionRetrieveUpdateDestroy.as_view()),

    path('procesar-imagen/', views.ProcesarImagenView.as_view(), name='procesar-imagen'),
    path('weather/', views.WeatherAPIView.as_view(), name='weather'),
    path('consultar-chatgpt/', views.ConsultarChatGPTView.as_view(), name='consultar_chatgpt'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
