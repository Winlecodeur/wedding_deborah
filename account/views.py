from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password =  form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None : 
                auth_login(request, user)
                return redirect ('profile')
            else :
                return messages.error("erreur de nom d'utilisateur ou password")
    else :
        form = AuthenticationForm()
    return render (request, 'auth/login.html', {'form':form})