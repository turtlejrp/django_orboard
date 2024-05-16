from django import forms
from .models import Loss

class LossForm(forms.ModelForm):

    
    class Meta:
        model = Loss
        fields = ("problem","lossType","duration","create_at_time","create_at_date")
        widgets = {
            'create_at_date':forms.DateInput(format='%d-%m-%Y',attrs={'type':'date'}),
        }
    





