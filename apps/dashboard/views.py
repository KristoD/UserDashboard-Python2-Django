from django.shortcuts import render
from .. users.models import *

def user(request):
    context = {
        "users" : User.objects.all(),
        "user_level" : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'dashboard/user.html', context)

def admin(request):
    context = {
        "users" : User.objects.all(),
        "user_level" : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'dashboard/admin.html', context)