# WebProject

# 💰 Loan Management System
A Django-based web platform for managing micro-loans between Customers, Bank Personnel, and Loan Providers.

# 📌 Overview
This application provides role-specific dashboards and functionalities for:

Customers to apply for loans and make payments.

Bank Personnel to review and approve/reject loan requests and create loan configurations.

Loan Providers to fund the system and track their contributions.

# 🧑‍💼 User Roles
Each user has a role defined in their UserProfile, which determines their access and dashboard:

Role	Capabilities
Customer	Apply for loans, view loans, make payments
Personnel	Approve/reject loans, manage loan configurations
Provider	Add funds to the platform, view funding history
# 🗂️ Project Structure
# 🔧 Dashboards
The system redirects logged-in users to a role-specific dashboard:

Role	Dashboard Template	View Logic
Customer	dashboard_customer.html	View their loans and apply for new ones
Personnel	dashboard_personnel.html	View and manage pending loans and configs
Provider	dashboard_provider.html	View/add funds contributed to the platform

The main view for all dashboards is:

@login_required
def dashboard_view(request):
    ...
    
# 📄 Other Views
View Function	          Description
loan_list	              Lists loans (all for personnel, own for customer)
loan_detail	            Shows a loan’s detailed information
approve_or_reject_loan	Personnel-only loan status change view

These views are protected using @login_required and role-based checks.

# 🧮 Database Models
# 📘 UserProfile
Extends Django’s User model with a role field:

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES, ...)
    
# 💸 Loan

class Loan(models.Model):
    customer = models.ForeignKey(UserProfile)
    amount = models.DecimalField(...)
    status = models.CharField(choices=[...])
    approved_by = models.ForeignKey(UserProfile, related_name="approved_loans", null=True)
    
# ⚙️ LoanConfiguration
Created by personnel to define loan rules.

# 🏦 LoanFund
Tracks funds added by providers.

🔗 URL Routing
URLs are defined using Django's urls.py. Example:

path('loan_list/', views.loan_list, name='loan_list'),
path('loan_detail/<int:loan_id>/', views.loan_detail, name='loan_detail'),
path('approve_or_reject_loan/<int:loan_id>/', views.approve_or_reject_loan, name='approve_or_reject_loan'),

These URLs are used in templates via:
<a href="{% url 'loan_list' %}">View Loans</a>

# 🎨 Templates
File	                            Description
dashboard_customer.html	          Customer view with loan list & apply btn
dashboard_personnel.html	        Personnel view with pending approvals
dashboard_provider.html	          Provider view with fund history
loan_list.html	                  General loan listing
loan_detail.html	                Detailed loan info

Styling is handled with Bootstrap via:

<link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">

# 🧠 Assumptions & Notes
- All users are authenticated and redirected to dashboards.

- Only personnel can approve or reject loan requests.

- Only customers can apply or pay loans.

- Only providers can add funds.

- Each User has one and only one UserProfile.

# ✅ Future Improvements
- Add payment processing logic.

- Add search/filtering for loans.

- Add historical transaction logs.

- REST API support for mobile apps.

# 🛠️ Tech Stack
Backend: Django (Python)

Frontend: HTML + Bootstrap

Database: PostgreSQL

Auth: Django’s built-in auth system
