"""FormView URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from form import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stu_data',views.ViewsetStudent,basename = 'student')
router.register('stu_model_Viewset',views.studentModelViewset,basename = 'stu_model_Viewset')
router.register('stu_read_only',views.studentReadOnly,basename = 'stu_read_only')  
urlpatterns = [
    path('admin/', admin.site.urls),
    path('start/',views.ContactForm.as_view()),
    path('list/',views.listView.as_view()),
    path('cache/',views.cachee),
    path('detail/<int:id>',views.Detailview.as_view(),name='detail'),
    path('apiView/',views.ApiView.as_view()),
    path('apiView/<int:pk>',views.ApiView.as_view()),
    path('genric/<slug:name>',views.genricView.as_view()),
    path('listapiV/<int:pk>',views.Listapiview.as_view()),
    path("",include(router.urls)),
]
