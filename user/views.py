from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from user.models import UserProfile
from user.forms import (SignUpForm, EditUserForm, EditProfileForm)

def home(request):
        return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
    else:
        form = SignUpForm()

        args = {'form': form}
        return render(request, 'signup.html', args)

def view_profile(request):
    args = {'profile': UserProfile, 'user': request.user}
    return render(request, 'profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        usereditform = EditUserForm(request.POST, instance=request.user)
        profileeditform = EditProfileForm(request.POST, instance=request.user)

        if usereditform.is_valid():
            usereditform.save()
            return redirect('user:view_profile')
    else:
        usereditform = EditUserForm(instance=request.user)
        profileeditform = EditProfileForm(instance=request.user)
        args = {'usereditform': usereditform, 'profileeditform': profileeditform}
        return render(request, 'edit_profile.html',args)

def logout(request):
    return render(request, 'logout.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user:change_password')

        else:
            return redirect('user:view_profile')

    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form }
        return render(request, 'password_change_form.html', args)
