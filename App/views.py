from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')



def member_login(request):
    return render(request, 'login.html')

