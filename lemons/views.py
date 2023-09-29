from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Yeet
from .forms import YeetForm

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