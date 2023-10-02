from django.shortcuts import render, redirect, get_object_or_404
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

def unfollow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow.
        profile = Profile.objects.get(user_id=pk)
        #Unfollow the user
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request, (f"You successfully unfollowed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You must be logged in to access this."))
        return redirect('home')
    
def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(request, (f"You successfully followed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You must be logged in to access this."))
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        yeets = Yeet.objects.filter(user_id=pk).order_by("-created_at")


        # Post form
        if request.method == "POST":
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # Save the user
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
    form = SignUpForm()  # Initialize the form here
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully registered!"))
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
    
def yeet_like(request, pk):
    if request.user.is_authenticated:
        yeet = get_object_or_404(Yeet, id=pk)
        if yeet.likes.filter(id=request.user.id):
            yeet.likes.remove(request.user)
        else:
            yeet.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))

    else: 
        messages.success(request, ("You have to be logged in."))
        return redirect('home')
    
def yeet_share(request, pk):
        yeet = get_object_or_404(Yeet, id=pk)
        if yeet:
            return render(request, "share_yeet.html", {'yeet':yeet})
  
        else: 
            messages.success(request, ("That yeet does not exist."))
            return redirect('home')
        
def delete_yeet(request, pk):
	if request.user.is_authenticated:
		yeet = get_object_or_404(Yeet, id=pk)
		# Check if you own the yeet
		if request.user.username == yeet.user.username:
			# Delete the yeet
			yeet.delete()
			
			messages.success(request, ("The yeet has been deleted."))
			return redirect(request.META.get("HTTP_REFERER"))	
		else:
			messages.success(request, ("This yeet is not yours"))
			return redirect('home')

	else:
		messages.success(request, ("Login to continue."))
		return redirect(request.META.get("HTTP_REFERER"))
     
def edit_yeet(request, pk):
    if request.user.is_authenticated:
        yeet = get_object_or_404(Yeet, id=pk)
        # Check if you own the yeet
        if request.user.username == yeet.user.username:
            form = YeetForm(request.POST or None, instance=yeet)
            if request.method == "POST":
                if form.is_valid():
                    yeet = form.save(commit=False)
                    yeet.user = request.user
                    yeet.save()
                    messages.success(request, ("Your yeet has been updated."))
                    return redirect('home')
            else:
                return render(request, "edit_yeet.html", {'form': form, 'yeet': yeet})
        else:
            messages.success(request, ("This yeet is not yours."))
            return redirect('home')
    else:
        messages.success(request, ("You have to be logged in."))
        return redirect('home')
    
def search(request):
    if request.method == "POST":
        search = request.POST['search']
        searched = User.objects.filter(username__contains = search)

        return render(request, 'search.html', {'search':search, 'searched':searched})
    else:
        return render(request, 'search.html', {})