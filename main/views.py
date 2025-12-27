from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm
from django.utils import timezone
from datetime import timedelta

# Create your views here.
@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, user = request.user)
        if form.is_valid():
            category = form.save(commit = False)
            category.user = request.user
            category.save()
            return redirect('categories/')
    else:
        form = CategoryForm(user = request.user)
        return render(request, 'add_category.html', {'form': form})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if category.user != request.user:
        return redirect('categories')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category, user=request.user)
    
    return render(request, 'add_category.html', {'form':form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if category.user != request.user:
        return redirect('categories/')
    
    if request.method == 'POST':
        category.delete()
        return redirect('categories/')
    
    return render(request, 'category_delete.html', {'category':category})

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, user = request.user)
        if form.is_valid():
            expense = form.save(commit = False)
            expense.user = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm(user = request.user)
        return render(request, 'add_expense.html', {'form': form})

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if expense.user != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense, user=request.user)
    
    return render(request, 'add_expense.html', {'form':form})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if expense.user != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        expense.delete()
        return redirect('home')
    
    return render(request, 'expense-delete.html', {'expense':expense})

@login_required
def statistics(request):
    today = timezone.now().date()
    week = today - timedelta(days = 7)

    bugungi_harajatlar = Expense.objects.filter(user = request.user, created_at__date = today).order_by('created_at')
    bugungi_harajatlar_summasi = bugungi_harajatlar.aggregate(Sum('amount'))['amount__sum'] or 0

    haftalik_harajatlar = Expense.objects.filter(user = request.user, created_at__date__gte = week).order_by('created_at')
    haftalik_harajatlar_summasi = haftalik_harajatlar.aggregate(Sum('amount'))['amount__sum'] or 0

    oylik_harajatlar = Expense.objects.filter(user = request.user, created_at__month = today.month, created_at__year = today.year).order_by('created_at')
    oylik_harajatlar_summasi = oylik_harajatlar.aggregate(Sum('amount'))['amount__sum'] or 0
    
    categories = Category.objects.filter(user = request.user).annotate(total=Sum('expenses__amount'))

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

@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user)

    return render(request, 'home.html', {'expenses':expenses})

@login_required
def categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'categories.html', {'categories': categories})
