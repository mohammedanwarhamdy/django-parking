from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
class devices(models.Model):
    IP=models.GenericIPAddressField(verbose_name="IP Address",blank=True,null=True)
    serial=models.CharField(max_length=30,verbose_name="serial number",blank=True,null=True)
    Device_name=models.CharField(max_length=60,verbose_name="Device Name",blank=True,null=True)

    su_net = models.GenericIPAddressField(verbose_name="subnet mask",blank=True,null=True)
    gate_way = models.GenericIPAddressField(verbose_name="Gateway ip",blank=True,null=True)

    def __str__(self):
        return self.IP
class subscriber(models.Model):
    subscriberid = models.IntegerField(verbose_name='Subscriber Id')
    name=models.CharField(max_length=70,verbose_name="Name",blank=True,null=True)
    card=models.IntegerField(verbose_name='Card Number')
    valid_from=models.DateTimeField(verbose_name="Valid From",blank=True,null=True)
    valid_to=models.DateTimeField(verbose_name="Valid TO",blank=True,null=True)
    packege = models.ForeignKey("packeges", on_delete=models.CASCADE, verbose_name="Packege",null=True,blank=True)
    def __str__(self):
        return self.name
class packeges(models.Model):
    packege_name=models.CharField(max_length=90,null=True,blank=True)
    packege_cost=models.IntegerField(verbose_name="Packege Cost",null=True,blank=True)
    packege_hours=models.IntegerField(verbose_name="Number of Hours",blank=True,null=True)
    def __str__(self):
        return self.packege_name


class transactions(models.Model):

    code=models.IntegerField(verbose_name="Code",blank=True,null=True)
    entry_point=models.CharField(max_length=90,verbose_name="Entry Point",blank=True,null=True)
    entry_time=models.DateTimeField(verbose_name="Entry Time",blank=True,null=True)


    def __str__(self):
        return str(self.code)

class counting(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user", null=True, blank=True)
    exite_time = models.DateTimeField(verbose_name="Exite Time", blank=True, null=True)
    total_time = models.FloatField(verbose_name="Total Time", blank=True, null=True)
    cost = models.FloatField(verbose_name="Cost", blank=True, null=True)
    code = models.IntegerField(verbose_name="Code", blank=True, null=True)
    entry_point = models.CharField(max_length=90, verbose_name="Entry Point", blank=True, null=True)
    entry_time = models.DateTimeField(verbose_name="Entry Time", blank=True, null=True)
    def __str__(self):
        return str(self.User)
