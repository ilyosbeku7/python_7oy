from django import forms
from .models import User
import re
from django.core.validators import FileExtensionValidator


class LoginForm(forms.Form):
    username=forms.CharField(required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control'}))


class  RegisterForm(forms.Form):
    first_name=forms.CharField(required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    confirm_password=forms.CharField(required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    photo=forms.ImageField(required=True, widget=forms.FileInput(attrs={"class":"form-control"}))
    def clean(self):
       password=self.cleaned_data.get('password')
       confirm_password=self.cleaned_data.get('confirm_password')

       if password:
           if confirm_password != password :
               raise forms.ValidationError('passwordlar bir xil emas')
           
       return self.cleaned_data
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not (first_name.isalpha() and first_name[0].isupper()):
            raise forms.ValidationError('Ism faqat harflardan va birinchi harfi katta yozilishi kerak')
        return first_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not (last_name.isalpha() and last_name[0].isupper()):
             raise forms.ValidationError('Familiya faqat harflardan va birinchi harfi katta yozilishi kerak')
        return last_name
    
class ProfileForm(forms.ModelForm):
   
    first_name=forms.CharField( widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField( widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField( widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number=forms.CharField( widget=forms.TextInput(attrs={"class":"form-control"}))
    photo=forms.ImageField( widget=forms.FileInput(attrs={"class":"form-control"}))
    bio=forms.CharField( widget=forms.TextInput(attrs={"class":"form-control"}))
    email=forms.EmailField( widget=forms.EmailInput(attrs={"class":"form-control"}))
     
    class Meta:
        model=User
        fields=('first_name', 'last_name', 'username', 'bio', 'email', 'photo','phone_number' )

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not (first_name.isalpha() and first_name[0].isupper()):
            raise forms.ValidationError('Ism faqat harflardan va birinchi harfi katta yozilishi kerak')
        return first_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not (last_name.isalpha() and last_name[0].isupper()):
             raise forms.ValidationError('Familiya faqat harflardan va birinchi harfi katta yozilishi kerak')
        return last_name    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+998\d{9}$', phone_number):
            raise forms.ValidationError("Tlefon raqam shu ko'rinishda bo'lishi lozim +998XX-XXX-XX-XX")
        return phone_number
    