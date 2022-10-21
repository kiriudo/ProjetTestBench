from django import forms

class productform(forms.Form):
    product = forms.CharField(label = 'product')
