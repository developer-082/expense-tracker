from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expanses')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    dascription = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
