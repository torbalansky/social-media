from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile

#Unregister group
admin.site.unregister(Group)

#Combine profile with user
class ProfileInline(admin.StackedInline):
    model = Profile

#expand user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]

#unregister user
admin.site.unregister(User)

#register user and profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)

