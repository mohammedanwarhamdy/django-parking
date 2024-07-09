from django.urls import path,include
from . import  views


app_name="parking"
urlpatterns = [
    path('', views.all_transactions, name="parking"),path("edit_ip/<int:id>",views.edit_ip,name="edit_ip"),path("delete/<int:id>",views.destroy,name="destroy"),path("subscriber",views.all_subscriber,name="subscriber"),path("delete_subscriber/<int:id>",views.delete_subscriber,name="delete_subscriber"),path("edit_subscriber/<int:id>",views.edit_subscriber,name="edit_subscriber"),path('devices/',views.all_devices,name="devices"),path('counting',views.Counting,name="counting"),path('reports',views.reports,name="reports"),path('settings',views.Counting_settings,name="settings"),path('signup',views.signup,name="signup")]