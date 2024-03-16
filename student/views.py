from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.views.generic import UpdateView
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, ProfileForm
from .models import  User
from django.urls import  reverse_lazy
from django.shortcuts import render, HttpResponseRedirect, reverse

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
                return HttpResponseRedirect(reverse('product:index'))

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
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = User()
                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.set_password(form.cleaned_data['password'])
                user.save()
                return HttpResponseRedirect(reverse('login_page'))
            except :
                  # or log the error for debugging
                return HttpResponseRedirect(reverse('register_page'))
    else:
        form = RegisterForm()
    return render(request, 'student/register_page.html', {'form': form})

class Profile_view(UpdateView):     
        form_class=ProfileForm
        model=User
        template_name='student/profile_page.html'
        extra_content={
            'users':User.objects.all()
        }
        
        def get_object(self, queryset=None):
            return self.request.user
        
        def get_success_url(self):
            return reverse_lazy('product:index')