from django import forms 
from .models import Invite, Table, Oath

class inviteForm(forms.ModelForm):
    class Meta : 
        model = Invite
        fields = ('first_name','name','whatsapp_num','table','last_name', 'statut')


class tableForm(forms.ModelForm):
    class Meta : 
        model = Table
        fields = ('name','number', 'capacite')

class oathForm(forms.ModelForm):
    class Meta : 
        model  = Oath
        fields = ('text','invite')