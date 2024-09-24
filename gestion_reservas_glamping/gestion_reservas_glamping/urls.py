"""
URL configuration for gestion_reservas_glamping project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pag_admin import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('protected/', views.glamping_crear, name='protected'),
    path('protected/creados/', views.glampings_index, name='glampings_index'),
    path('protected/<int:glamping_id>/',views.glamping_actualizar,name ='glamping_actualizar'),
    path('protected/eliminar/<int:glamping_id>',views.glamping_eliminar,name = 'glamping_eliminar'),
    path('api/glamping/', views.GlampingList.as_view(), name='glamping-list'),
    path('crear-reserva/', views.crear_reserva, name='crear_reserva'),
    path('fechas-ocupadas/', views.fechas_ocupadas, name='fechas_ocupadas'),
    path('todas_fechas-ocupadas/', views.todas_fechas_ocupadas, name='todas_fechas_ocupadas'),
    path('api/glamping/<int:pk>/', views.GlampingDetail.as_view(), name='glamping-detail'),
    path('create-payment/', views.create_payment, name='create-payment'),
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
