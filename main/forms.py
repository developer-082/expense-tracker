from django import forms
from .models import Expense, Category

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description']

        widgets = {
            'category': forms.Select(attrs={
                'class':'form-control',
                'style': 'max-width: 500px'
            }),
            'amount': forms.DecimalField(max_digits=12, decimal_places=2),
            'description': forms.TextInput()
        }
 
    def __init__(self, *args, **kwargs):
        user1 = kwargs.pop('user', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)
        if user1:
            self.fields['category'].queryset = Category.objects.filter(user = user1)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.CharField(max_length=100)
        }
 
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
