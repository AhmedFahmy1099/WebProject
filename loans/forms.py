from django import forms
from .models import LoanConfiguration, Loan


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['configuration', 'amount', 'term_months']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        return amount

    def clean_term_months(self):
        term_months = self.cleaned_data.get('term_months')
        if term_months <= 0:
            raise forms.ValidationError("Term must be greater than 0 months.")
        return term_months