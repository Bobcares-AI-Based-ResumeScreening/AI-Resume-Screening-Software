from django.shortcuts import render, redirect
from .forms import CandidateForm
from .models import Candidate

def candidates_dashboard(request):
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('candidates_dashboard')
    else:
        form = CandidateForm()
    return render(request, 'candidates_dashboard.html', {'form': form})
