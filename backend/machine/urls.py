from django.urls import path
from .views import *

urlpatterns = [
    path('machine/', MachineList.as_view()),
    path('machine_detail/<int:pk>', MachineDetail.as_view()),
    path('machine_daily_record/',Machine_line_record_create.as_view()),
    path('machine_daily_record/<int:pk>',Machine_line_record_view.as_view()),
    path('machine_stat1',Machine_stat1.as_view()),
    path('machine_stat2',Machine_stat2.as_view()),
]
