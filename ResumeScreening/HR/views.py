from django.shortcuts import render, redirect
from .forms import HRForm
from .models import HR

def hr_dashboard(request):
    if request.method == "POST":
        form = HRForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hr_dashboard')
    else:
        form = HRForm()
    return render(request, 'hr_dashboard.html', {'form': form})
