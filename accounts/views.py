from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal
from .models import Account, Transaction as Txn

@login_required
def dashboard(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'accounts/dashboard.html', {'accounts': accounts})


@login_required
def deposit(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        amount = Decimal(request.POST.get('amount'))

        account = Account.objects.get(id=account_id, owner=request.user)

        with transaction.atomic():
            account.balance += amount
            account.save()
            Txn.objects.create(
                account=account,
                transaction_type='deposit',
                amount=amount,
                description='Cash deposit'
            )

        return redirect('dashboard')

    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'accounts/deposit.html', {'accounts': accounts})