from django.contrib import admin
from .models import UserProfile, Loan, LoanFund, LoanConfiguration
# Register your models here.
admin.site.register(LoanConfiguration)
admin.site.register(Loan)
admin.site.register(LoanFund)
admin.site.register(UserProfile)
