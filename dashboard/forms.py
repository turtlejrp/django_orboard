from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class DateForm(forms.Form):
    date = forms.DateField(widget=DateInput)


class DateModelForm(forms.Form):
    class Meta:
        widget = {'date': DateInput()}
