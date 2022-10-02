from django.shortcuts import render
from django.contrib.auth import logout
import time


def is_not_student(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_student:
            return func(request, *args, **kwargs)
        else:
            logout(request)
            return render(request, "industrial_attachment/not_student_error_404.html",
                          context={'current_date': time.strftime("%Y"), })
    return wrapper


def is_not_supervisor(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_supervisor:
            return func(request, *args, **kwargs)
        else:
            logout(request)
            return render(request, "industrial_attachment/not_supervisor_404.html",
                          context={'current_date': time.strftime("%Y"), })
    return wrapper


def is_unauthenticated(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'industrial_attachment/not_login_404.html')
    return wrapper
