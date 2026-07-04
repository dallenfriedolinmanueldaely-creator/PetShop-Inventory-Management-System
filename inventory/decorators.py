from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def get_user_role(user):
    if user is None or not user.is_authenticated:
        return None
    try:
        role = user.profile.role
        if role in ('owner', 'admin', 'staff'):
            return role
    except Exception:
        pass

    if user.groups.filter(name='Owner').exists():
        return 'owner'
    if user.groups.filter(name='Admin').exists():
        return 'admin'
    if user.groups.filter(name='Staff').exists():
        return 'staff'

    if user.is_superuser:
        return 'owner'
    return None

def is_owner(user):
    return get_user_role(user) == 'owner'

def is_admin_or_above(user):
    return get_user_role(user) in ('owner', 'admin')

def is_staff_or_above(user):
    return get_user_role(user) in ('owner', 'admin', 'staff')

def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Silakan login terlebih dahulu.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Silakan login terlebih dahulu.')
            return redirect('login')
        if not is_owner(request.user):
            messages.error(request, 'Akses ditolak! Fitur ini hanya untuk Owner.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Silakan login terlebih dahulu.')
            return redirect('login')
        if not is_admin_or_above(request.user):
            messages.error(request, 'Akses ditolak! Fitur ini hanya untuk Admin ke atas.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Silakan login terlebih dahulu.')
            return redirect('login')
        if not is_staff_or_above(request.user):
            messages.error(request, 'Akses ditolak! Anda tidak memiliki izin.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
