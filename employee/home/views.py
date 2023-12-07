# views.py
import csv
import os
import csv as csv_module
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import CustomUser, FullTime, Contract, Client
from django.contrib.auth.hashers import make_password
from .serializers import CustomUserSerializer,UserSerialializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
class CreateUserView(APIView):
    def post(self, request, format=None):
        request.data['password'] = make_password(request.data.get('password'))
        userdata = CustomUserSerializer(data=request.data)
        if userdata.is_valid():
            user = userdata.save()
            role = userdata.validated_data.get('role')

            if role == 'fulltime':
                branch_name = request.data.get('branch_name')
                if not branch_name:
                    user.delete()
                    return Response({'error': 'Branch name is required for full-time users.'}, status=status.HTTP_400_BAD_REQUEST)
                FullTime.objects.create(user=user, branch_name=branch_name)

            elif role == 'contract':
                start_date = request.data.get('start_date')
                end_date = request.data.get('end_date')
                if not start_date or not end_date:
                    user.delete()
                    return Response({'error': 'Start date and end date are required for contract users.'}, status=status.HTTP_400_BAD_REQUEST)
                Contract.objects.create(user=user, start_date=start_date, end_date=end_date)

            elif role == 'client':
                city_name = request.data.get('city_name')
                if not city_name:
                    user.delete()
                    return Response({'error': 'City name is required for client users.'}, status=status.HTTP_400_BAD_REQUEST)
                Client.objects.create(user=user, city_name=city_name)
            return Response(userdata.data, status=status.HTTP_201_CREATED)

        return Response(userdata.errors, status=status.HTTP_400_BAD_REQUEST)

class ExportCustomUsersCSV(View):
    def get(self, request, *args, **kwargs):
        folder_path = 'C:/custom_model/employee/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_name = f"custom_users_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)


            writer.writerow([ 'Username', 'Email', 'Name', 'branch_name'])

            data = CustomUser.objects.select_related('fulltime').values('username', 'name', 'email', 'fulltime__branch_name')
            for item in data:
                my_list = list(item.values())

                writer.writerow(my_list)

        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        response.write(f'The CSV file has been saved. Download it from: {file_path}')

        return response
