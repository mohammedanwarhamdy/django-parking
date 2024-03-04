from django.db import models
class devices(models.Model):
    IP=models.GenericIPAddressField(verbose_name="IP Address")
    serial=models.CharField(max_length=30,verbose_name="serial number",blank=True,null=True)
    Device_name=models.CharField(max_length=60,verbose_name="Device Name",blank=True,null=True)

    su_net = models.GenericIPAddressField(verbose_name="subnet mask",blank=True,null=True)
    gate_way = models.GenericIPAddressField(verbose_name="Gateway ip",blank=True,null=True)



    def __str__(self):
        return self.IP



