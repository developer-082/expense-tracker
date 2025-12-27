from django.shortcuts import render
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.utils import timezone
from datetime import timedelta

# Create your views here.
@login_required
def statistics(request):
    today = timezone.now().date()
    week = today - timedelta(days = 7)

    bugungi_harajatlar = Expense.objects.filter(user = request.user, created_at = today).order_by('created_at')
    bugungi_harajatlar_summasi = Expense.objects.filter(user = request.user, created_at = today).aggregate(Sum('amount'))

    haftalik_harajatlar = Expense.objects.filter(user = request.user, created_at__gte = week).order_by('created_at')
    haftalik_harajatlar_summasi = Expense.objects.filter(user = request.user, created_at__gte = week).aggregate(Sum('amount'))

    oylik_harajatlar = Expense.objects.filter(user = request.user, created_at__month = today.month, created_at__year = today.year).order_by('created_at')
    oylik_harajatlar_summasi = Expense.objects.filter(user = request.user, created_at__month = today.month, created_at__year = today.year).aggregate(Sum('amount'))
    
    categories = Category.objects.filter(user = request.user).annotate(total = Sum('expenses__amount'))

    data = {
        'today_expenses': bugungi_harajatlar,
        'today': bugungi_harajatlar_summasi,
        'week_expenses': haftalik_harajatlar,
        'week': haftalik_harajatlar_summasi,
        'month_expenses': oylik_harajatlar,
        'month': oylik_harajatlar_summasi,

        'categories': categories
        
    }

    return render(request, 'statistics.html', context = data)