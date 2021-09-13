from django.db.models import query
from django.db.models.query import QuerySet
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .forms import ContactForm
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from form import forms
from django.views.generic.detail import DetailView
from .serializers import StudentSerilizer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin

from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveDestroyAPIView
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from .models import student
from form import models

from rest_framework.views import APIView

from rest_framework.response import Response

from form import serializers

# Create your views here.


class ContactForm(FormView):
    template_name = "form/contact.html"
    form_class = ContactForm

    def form_valid(self,form):
        print(form.cleaned_data['name'])
        print(form.cleaned_data['surname'])
        print(form.cleaned_data['msg'])
        return HttpResponse({'msg':'created'})
    
class listView(ListView):
    model = student
    template_name = 'form/student.html'
    context_object_name = 'stu'
    ordering = ['name']
    
    def dispatch(self, request, *args, **kwargs):
        print(request.GET,kwargs,args)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return student.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Boss'] = self.model.objects.filter(name='Ritik')
        return context
    
    # def get_template_names(self):
    #     if self.request.COOKIES['user'] == 'ritik':
    #         template_name = 'form/contact.html'
    #     else:
    #         template_name = self.template_name
    #     return[template_name]


class Detailview(DetailView):
    model = student
    template_name = 'form/DetailofObj.html'
    context_object_name = "student"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = self.model.objects.all()
        print("Value is ",self.get_object().name ,self.object)
        print(self.model.objects.all())
        return context


def cachee(request):
    if cache.get("stu_list"):
        payload = cache.get("stu_list")
        print(cache.ttl("stu_list"))
        db = "redis"
    else:
        stu_list = student.objects.all()
        payload = []
        for i in stu_list:
            payload.append(i.name)
        cache.set("stu_list",payload)
        db = 'sqlite'

    return JsonResponse({'status':200,'db':db,'payload':payload})


class ApiView(APIView):
    def get(self,request,pk=None, format = None):
        if pk:
            stu_data = student.objects.get(id = pk)
            stu_serilize_data = StudentSerilizer(stu_data)
            return Response(stu_serilize_data.data)
            
        stu_data = student.objects.all()
        stu_serilize_data = StudentSerilizer(stu_data,many= True)
        return Response(stu_serilize_data.data)
# class genricView(ListModelMixin,GenericAPIView,CreateModelMixin,RetrieveModelMixin):
class genricView(CreateModelMixin,GenericAPIView,RetrieveModelMixin):
    queryset = student.objects.all()
    serializer_class = StudentSerilizer
    lookup_field = 'name'       # Model me jis coloumn se compare kerna chahte ho oska name (name likha he mtlb name se compare kere ga )

    lookup_url_kwarg='name'     # To change the name whatever we pass in url (  default is  pk <int:pk> But if you want to change then you can use <int:id>
                                # set lookup_url_kwarg ='id')\

    
    # def get_queryset(self):
    #     return student.objects.filter(name = 'Ritik')
    # def get_object(self):
    #     queryset = self.get_queryset()
    #     filter = {}
    #     for field in self.multiple_lookup_fields:
    #         filter[field] = self.kwargs[field]

    #     obj = get_object_or_404(queryset, **filter)
    #     self.check_object_permissions(self.request, obj)
    #     return obj

    def get_object(self):
        print(self.kwargs)
        return   get_object_or_404(student, name= self.kwargs['name'])   # student.objects.get(name = self.kwargs['name'])

    def get(self,request,*args,**kwargs):
        print(self.get_object())
        return self.retrieve(request, *args,**kwargs)
    
    # def filter_queryset(self, queryset):
    #     filter_backends = [CategoryFilter]

    #     if 'geo_route' in self.request.query_params:
    #         filter_backends = [GeoRouteFilter, CategoryFilter]
    #     elif 'geo_point' in self.request.query_params:
    #         filter_backends = [GeoPointFilter, CategoryFilter]

    #     for backend in list(filter_backends):
    #         queryset = backend().filter_queryset(self.request, queryset, view=self)

    #     return queryset


    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save()

class Listapiview(RetrieveAPIView,UpdateAPIView):
    queryset = student.objects.all()
    serializer_class = StudentSerilizer
