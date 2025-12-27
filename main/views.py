from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm
from django.utils import timezone
from datetime import timedelta

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('categories')
    else:
        form = CategoryForm(user=request.user)
        return render(request, 'add_category.html', {'form': form})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if category.user != request.user:
        return redirect('categories')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category, user=request.user)
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
        return redirect('categories')
    
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    
    return render(request, 'category_delete.html', {'category':category})

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'add_expense.html', {'form': form})

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if expense.user != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
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

from django.shortcuts import render
from django.db.models import Sum
from .models import Expense  # Model nomini tekshiring

@login_required
def statistics(request):
    today = timezone.now().date()
    week = today - timedelta(days=7)

    bugungi_harajatlar = Expense.objects.filter(user=request.user, created_at__date=today).order_by('created_at')
    bugungi_harajatlar_summasi = bugungi_harajatlar.aggregate(Sum('amount'))['amount__sum'] or 0

    haftalik_harajatlar = Expense.objects.filter(user=request.user, created_at__date__gte=week).order_by('created_at')
    haftalik_harajatlar_summasi = haftalik_harajatlar.aggregate(Sum('amount'))['amount__sum'] or 0

    oylik_harajatlar = Expense.objects.filter(user=request.user, created_at__month=today.month, created_at__year=today.year).order_by('created_at')
    oylik_harajatlar_summasi = oylik_harajatlar.aggregate(Sum('amount'))['amount__sum'] or 0

    stats = Expense.objects.filter(user=request.user, created_at__date__gte = week).values('category__name').annotate(total=Sum('amount')).order_by('-total')

    k = 0
    f = 0
    labels = []
    data = []
    for item in stats:
        k += 1
        if k <= 5:
            labels += [item['category__name']]
            data += [float(item['total'])]
        else:
            if f == 0:
                f = 1
                labels += ["Boshqalar"]
                data += [float(item['total'])]
                continue
            data[-1] += float(item['total'])

    data1 = {
        'today_expenses': bugungi_harajatlar,
        'today_sum': bugungi_harajatlar_summasi,
        'week_expenses': haftalik_harajatlar,
        'week_sum': haftalik_harajatlar_summasi,
        'month_expenses': oylik_harajatlar,
        'month_sum': oylik_harajatlar_summasi,
        'category_labels': labels,
        'category_data': data,
    }
    return render(request, 'statistics.html', context=data1)

@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'home.html', {'expenses':expenses})

@login_required
def categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'categories.html', {'categories': categories})