from rest_framework import serializers
from .models import CustomUser,FullTime,Contract,Client

class FullTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullTime
        fields = '__all__'
class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields='__all__'
class CustomUserSerializer(serializers.ModelSerializer):
    full_time = FullTimeSerializer(read_only=True)  
    class Meta:
        model = CustomUser
        fields = '__all__' 
class UserSerialializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'