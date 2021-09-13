from .models import student
from rest_framework import serializers

class StudentSerilizer(serializers.ModelSerializer):
    class Meta:
        model = student
        fields = ['id','name','surname','address']

