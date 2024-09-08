from app.models import Barber,Shift,Client
from django.forms import ModelForm, TextInput
from django import forms
import re

class BarberForm(ModelForm):
    class Meta:
        model=Barber
        fields=['fio','rank','position']

        widgets={
            'fio':TextInput(attrs={
                'class':'input',
                'placeholder':'ФИО',
                'required':'required',
                'tabindex':'1'
            }),
            'rank':TextInput(attrs={
                'class':'input',
                'placeholder':'Разряд',
                'required':'required',
                'tabindex':'2'
            }),
            'position':TextInput(attrs={
                'class':'input',
                'placeholder':'Должность',
                'required':'required',
                'tabindex':'3'
            })
        }

    def clean_fio(self):
        fio = self.cleaned_data['fio']
        pattern = r'^[A-Za-zА-Яа-яЁё\s]+$'  # Регулярное выражение для проверки ФИО
        if not re.match(pattern, fio):
            raise forms.ValidationError('Поле ФИО должно содержать только буквы.')
        return fio
    
    def clean_position(self):
        position = self.cleaned_data['position']
        pattern = r'^[A-Za-zА-Яа-яЁё\s-]{1,50}$'  # Регулярное выражение для проверки должности
        if not re.match(pattern, position):
            raise forms.ValidationError('Поле должность должно содержать только буквы и разделительные символы (пробел или дефис).')
        return position
   
    
class ShiftForm(ModelForm):
    barber = forms.ModelChoiceField(queryset=Barber.objects.all(), empty_label=None, widget=forms.Select(attrs={
        'class': 'input',
        'required': 'required',
        'tabindex': '1'
    }))
    date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'input',
        'required': 'required',
        'tabindex': '2',
        'type': 'date',
    }))

    class Meta:
        model = Shift
        fields = ['barber', 'date']

class ClientForm(ModelForm):
    shift = forms.ModelChoiceField(queryset=Shift.objects.all(), empty_label=None, widget=forms.Select(attrs={
        'class': 'input',
        'required': 'required',
        'tabindex': '2',
    }))

    class Meta:
        model = Client
        fields = ['name', 'shift']

        widgets={
            'name':TextInput(attrs={
                'class':'input',
                'placeholder':'Имя',
                'required':'required',
                'tabindex':'1'
            })
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.isalpha():
            raise forms.ValidationError('Имя должно содержать только буквы.')
        return name