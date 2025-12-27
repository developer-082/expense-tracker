from django import forms
from .models import Expense, Category

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description']

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 500px'
            }),
            # TUZATILDI: DecimalField o'rniga NumberInput ishlatildi
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Summani kiriting'
            }),
            # description to'g'ri edi, lekin style qo'shdik
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Izoh'
            })
        }
 
    def __init__(self, *args, **kwargs):
        user1 = kwargs.pop('user', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)
        if user1:
            self.fields['category'].queryset = Category.objects.filter(user=user1)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            # TUZATILDI: CharField o'rniga TextInput ishlatildi
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kategoriya nomi'
            })
        }
 
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
