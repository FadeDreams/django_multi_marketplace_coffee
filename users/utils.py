from django.core.exceptions import PermissionDenied

def check_coffee_role(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_customer_role(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'coffeeDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'userDashboard'
        return redirectUrl
    elif user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
