from .models import devices
from django import forms

class edit_ipform(forms.ModelForm):
    class Meta:
        model=devices
        fields=["IP","su_net","gate_way","Device_name"]
