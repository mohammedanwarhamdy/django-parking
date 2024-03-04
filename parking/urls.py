from django.urls import path,include
from . import  views

app_name="parking"
urlpatterns = [
    path('',views.all_devices),path("edit_ip/<int:id>",views.edit_ip,name="edit_ip"),path("delete/<int:id>",views.destroy,name="destroy")]