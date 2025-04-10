from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Loan, LoanFund, LoanConfiguration, Payment
from django.contrib import messages
from .forms import LoanApplicationForm
from django.http import HttpResponseRedirect

def home_redirect(request):
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, role=role)
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def dashboard_view(request):
    profile = UserProfile.objects.get(user=request.user)

    context = {
        'role': profile.role,
    }

    if profile.role == 'provider':
        # Show funds, add fund option, amortization table
        context['funds'] = LoanFund.objects.filter(provider=profile)
        return render(request, 'provider/dashboard_provider.html', context)

    elif profile.role == 'customer':
        # Show current loans, apply for loan, make payment
        context['loans'] = Loan.objects.filter(customer=profile)
        return render(request, 'customer/dashboard_customer.html', context)

    elif profile.role == 'personnel':
        # Show pending loan applications, fund applications, add config
        context['loan_requests'] = Loan.objects.filter(status='pending')
        context['loan_configs'] = LoanConfiguration.objects.all()
        return render(request, 'personnel/dashboard_personnel.html', context)

    return redirect('login')


@login_required
def apply_loan(request):
    profile = request.user.userprofile

    # Ensure that the user is a customer
    if profile.role != 'customer':
        return redirect('login')  # Redirect if the user is not a customer

    # Get available loan configurations
    loan_configs = LoanConfiguration.objects.all()

    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)

        if form.is_valid():
            loan_configuration = form.cleaned_data['loan_configuration']
            loan_amount = form.cleaned_data['amount']
            term_months = form.cleaned_data['term_months']

            # Ensure loan amount is within the valid range
            if loan_amount < loan_configuration.min_amount or loan_amount > loan_configuration.max_amount:
                form.add_error('amount', f"Loan amount must be between {loan_configuration.min_amount} and {loan_configuration.max_amount}.")
            else:
                # Create the loan application and save it
                loan_application = Loan(
                    customer=profile,
                    configuration=loan_configuration,
                    amount=loan_amount,
                    term_months=term_months,
                    interest_rate=loan_configuration.interest_rate,  # Use interest rate from configuration
                    status='pending'  # Set status to pending
                )
                loan_application.save()

                return redirect('customer_dashboard')  # Redirect to the customer dashboard after applying

    else:
        form = LoanApplicationForm()

    context = {
        'form': form,
        'loan_configs': loan_configs,
    }

    return render(request, 'customer/apply_loan.html', context)

@login_required
def loan_list(request):
    profile = request.user.userprofile

    if profile.role == 'customer':
        loans = Loan.objects.filter(customer=profile)
    elif profile.role == 'personnel':
        loans = Loan.objects.all()
    else:
        return redirect('login')

    context = {
        'loans': loans
    }

    return render(request, 'customer/loan_list.html', context)


@login_required
def loan_detail(request, loan_id):
    profile = request.user.userprofile
    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return redirect('loan_list')

    if loan.customer != profile and profile.role != 'personnel':
        return redirect('login')

    context = {
        'loan': loan
    }

    return render(request, 'customer/loan_detail.html', context)

@login_required
def approve_or_reject_loan(request, loan_id):
    profile = request.user.userprofile

    if profile.role != 'personnel':
        return redirect('login')

    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return redirect('loan_list')

    action = request.POST.get('action')

    if action == 'approve':
        loan.status = 'approved'
        loan.approved_by = profile
    elif action == 'reject':
        loan.status = 'rejected'

    loan.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))