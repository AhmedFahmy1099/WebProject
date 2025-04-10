from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    USER_ROLES = [
        ('provider', 'Loan Provider'),
        ('customer', 'Loan Customer'),
        ('personnel', 'Bank Personnel'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class LoanFund(models.Model):
    provider = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'provider'})
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Fund of {self.amount} by {self.provider}"


class LoanConfiguration(models.Model):
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'personnel'})
    min_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # in percent
    duration_months = models.PositiveIntegerField()

    def __str__(self):
        return f"Config: {self.min_amount}-{self.max_amount} @ {self.interest_rate}%"


class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    configuration = models.ForeignKey(LoanConfiguration, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term_months = models.PositiveIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_loans')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.id} - {self.amount} - {self.status}"


class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} on Loan {self.loan.id}"