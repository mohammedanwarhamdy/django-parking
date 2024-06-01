from .models import devices,subscriber
from django import forms
from django.contrib.admin import widgets

class edit_ipform(forms.ModelForm):
    class Meta:
        model=devices
        fields=["IP","su_net","gate_way","Device_name"]
class add_subscriber(forms.ModelForm):

    class Meta:
        model=subscriber


        fields = ['name', 'card', 'valid_from', 'valid_to', 'packege','subscriberid']
        widgets = {
            'valid_from': forms.TextInput(attrs={'type': 'date'}),
            'valid_to': forms.TextInput(attrs={'type': 'date'}),
        }


