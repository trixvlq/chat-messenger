from django.shortcuts import render

# Create your views here.
def sign_up(request):
    return render(request, 'registration/sign_up.html')

def sign_in(request):
    return render(request, 'registration/sign_in.html')