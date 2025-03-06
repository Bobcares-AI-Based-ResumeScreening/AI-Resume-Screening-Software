from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.contrib.auth import login,logout
from .forms import UserRegistrationForm
from django.shortcuts import render,redirect

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True})
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def home(request):
    return render(request, 'accounts/home.html')

def logout_view(request):
    logout(request)
    return redirect('login') 