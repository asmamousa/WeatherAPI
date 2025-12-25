from django import forms

class WeatherForm(forms.Form):
    city = forms.CharField(max_length=50)