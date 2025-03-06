''''from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the AI Resume Screening Software!")
'''
'''
from django.shortcuts import redirect

def home(request):
    return redirect('hr_dashboard')  # Redirects to HR Dashboard


from django.shortcuts import redirect

def home(request):
    return redirect('candidates_dashboard') 
    '''
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
