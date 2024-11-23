from django.urls import path
from .views import MachineList,MachineDetail

urlpatterns = [
    path('machine/', MachineList.as_view()),
    path('machine_detail/<int:pk>', MachineDetail.as_view())
]
