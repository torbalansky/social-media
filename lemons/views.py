from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Yeet
from .forms import YeetForm, SignUpForm, ProfilePictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        form = YeetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                yeet = form.save(commit=False)
                yeet.user = request.user
                yeet.save()
                messages.success(request, "Your yeet has been posted.")
                return redirect('home')
            
        yeets = Yeet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"yeets": yeets, "form":form})
    else:
        yeets = Yeet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"yeets": yeets})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ("You must be logged in to access this."))
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        yeets = Yeet.objects.filter(user_id=pk).order_by("-created_at")


        # Post form
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request, "profile.html", {"profile":profile, "yeets":yeets})
    else:
        messages.success(request, ("You must be logged in."))
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are logged in."))
            return redirect('home')
        else:
            messages.success(request, ("An error occured, try again."))
            return redirect('login')

    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out successfully."))
    return redirect('home')

def register_user(request):
    form = SignUpForm(request.POST)  # Initialize the form here
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You are logged in."))
            return redirect('home')
    return render(request, "register.html", {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)    
            messages.success(request, ("Your profile has been updated."))
            return redirect('home')
        
        return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request, ("You have to be logged in."))
        return redirect('home')