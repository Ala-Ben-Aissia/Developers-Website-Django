from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q  # look-up filter
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessagForm
from .models import Profile, Skill
from .utils import paginateProfiles, searchProfiles

# Create your views here.


def profiles(request):
    profiles, search_query = searchProfiles(request)
    profiles, custom_range = paginateProfiles(request, profiles, 6)
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    skills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")
    context = {'profile':profile, 'skills':skills, 'otherskills':otherskills}
    return render(request, 'users/profile.html', context)

# account user
# login
# logout
# registration


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    projects = profile.project_set.all()
    skills = profile.skill_set.all()
    context = {'profile':profile, 'projects':projects, 'skills':skills}
    return render(request, 'users/account.html', context)


def loginUser(request):
    page = 'login'
    
    if request.method == 'POST':                     
        username = request.POST['username'].lower()
        password = request.POST['password']  # request.POST --> dict(k, v)
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username doesn't exist")    
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "successfully logged-in!")
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, "username or password is incorrect !")      
        
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'Logged-out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, 'Your account has been created !')
            
            login(request, user)
            
            return redirect('account')
        
    context={'page':page, 'form':form}
            
    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def updateProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('account')
    context = {'profile':profile, 'form':form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'skill created successfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')   
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'skill updated successfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.info(request, 'skill deleted successfully')
        return redirect('account')
    context = {'object':skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messagerequests = profile.messages.all()
    unreadCount = messagerequests.filter(is_read=False).count()
    context = {'messagerequests':messagerequests, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request, 'users/message.html', context)

def sendMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessagForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == 'POST':
        form = MessagForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'You message has been sent')
            return redirect('profile', pk=recipient.id)
    context = {'form':form, 'recipient':recipient}
    return render(request, 'message_form.html', context)