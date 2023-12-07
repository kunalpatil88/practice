from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='customuser-create'),
    path('export_custom_users_csv/', ExportCustomUsersCSV.as_view(), name='export_custom_users_csv'),

]