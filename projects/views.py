from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from projects.forms import ProjectForm, ReviewForm
from .models import Project, Tag
from django.contrib import messages
from . utils import searchProjects, paginateProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.


def projects(request):
    projects, search_query = searchProjects(request)
    projects, custom_range = paginateProjects(request, projects, 6)
    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        
        project.getVoteCount
        messages.success(request, 'Review added for the submitted vote')
        return redirect('project', pk=project.id)
    context = {'project':project, 'tags':tags, 'form':form}
    return render(request, 'projects/project.html', context)


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, 'Project created successfully')
            return redirect('account')
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.info(request, 'Project updated ')

            return redirect('account')
    context = {'project':project, 'form':form}    
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.info(request, 'Project deleted ')

        return redirect('account')
    context = {'object': project}
    return render(request, 'delete_template.html', context)