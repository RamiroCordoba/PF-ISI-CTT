from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import *

#--- Pagina principal
def home_view(request):
  return render(request,"home/index.html")

#--- Pagina para el login
def login_view(request):
  if request.method == "POST":
    usuario = request.POST['username']
    clave = request.POST['password']
    user=authenticate(request, username=usuario,password=clave)
    if user is not None:
      login(request, user)
      return redirect('dashboard') # Si esta todo bien, lleva al dashboard
    else:
      return redirect(reverse_lazy('home'))
  else:
    #___ Si ingresa por aca es porque es la primera vez.
    miForm= AuthenticationForm()
  return render(request, "home/login.html",{"form":miForm})
