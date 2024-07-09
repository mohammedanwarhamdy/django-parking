from .models import devices,subscriber,counting_settings
from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
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


class FilterForm(forms.Form):
    user=forms.ModelChoiceField(queryset=User.objects.all(),required=False)
    start_date=forms.DateTimeField(required=True,widget=forms.TextInput(attrs={'type':'datetime-local'}))
    end_date = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={'type': 'datetime-local'}))


class subscriber_tansaction_filter_form(forms.Form):
    user=forms.ModelChoiceField(queryset=User.objects.all(),required=False)
    start_date=forms.DateTimeField(required=True,widget=forms.TextInput(attrs={'type':'datetime-local'}))
    end_date = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={'type': 'datetime-local'}))

class counting_settings_form(forms.ModelForm):
    class Meta:
        model = counting_settings
        fields = [
            "period_of_allowing", "first_period_duration", "second_period_duration",
            "first_period_duration_cost", "second_period_duration_cost",
            "rest_period_duration_cost_perhoure", "enable_night_mode",
            "n_starttime", "n_endtime", "night_modeCost","min_period_tocost",
        ]
        widgets = {
            'enable_night_mode': forms.CheckboxInput(),
            'n_starttime': forms.TextInput(attrs={'type': 'time'}),
            'n_endtime': forms.TextInput(attrs={'type': 'time'}),
        }