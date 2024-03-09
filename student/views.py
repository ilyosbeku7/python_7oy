from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.views.generic import UpdateView
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, ProfileForm
from .models import  User
from django.urls import  reverse_lazy, reverse

# Create your views here.


def login_page(request):
    if request.method == 'POST':
        form= LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate( request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

    form=LoginForm()
    data={
        'form':form
    }

    return render(request, 'student/login_page.html' ,context=data)

def logout_page(request):
    logout(request)

    return HttpResponseRedirect(reverse('login_page'))

def register_page(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
           try:
               user=User()
               user.username=form.cleaned_data['username']  
               user.frist_name=form.cleaned_data['frist_name']  
               user.last_name=form.cleaned_data['last_name']  
               user.set_password(form.cleaned_data['password'])
               user.save()
               return   HttpResponseRedirect(reverse('login_page'))
           except:
                return   HttpResponseRedirect(reverse('index'))
    

    form=RegisterForm()
    data={
        'form':form
    }

    return render(request, 'student/register_page.html' ,context=data)

class Profile_view(UpdateView):     
        form_class=ProfileForm
        model=User
        template_name='student/profile_page.html'
        
        def get_object(self, queryset=None):
            return self.request.user
        
        def get_success_url(self):
            return reverse_lazy('index')