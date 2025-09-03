from django import forms
from .models import Review

class OrderForm(forms.Form):
    name = forms.CharField(
        max_length=100, label="Ваше ім’я",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20, label="Телефон",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label="Адреса доставки",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1})
    )




class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }