from django.urls import path
from . import views


urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.profile, name='profile'),
    
    path('account/', views.userAccount, name='account'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('edit-profile/', views.updateProfile, name='update_profile'),
    
    path('create-skill/', views.createSkill, name='create_skill'),
    path('update-skill/<str:pk>/', views.updateSkill, name='update_skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete_skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.viewMessage, name='message'),
    path('send-message/<str:pk>/', views.sendMessage, name='send_message'),
    
]
