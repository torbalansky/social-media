from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('yeet_like/<int:pk>', views.yeet_like, name='yeet_like'),
    path('yeet_share/<int:pk>', views.yeet_share, name='yeet_share'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('delete_yeet/<int:pk>', views.delete_yeet, name='delete_yeet'),
    path('edit_yeet/<int:pk>', views.edit_yeet, name='edit_yeet'),
]
