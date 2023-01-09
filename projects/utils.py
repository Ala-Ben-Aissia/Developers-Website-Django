from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchProjects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    tags = Tag.objects.filter(name__icontains=search_query)      
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(tags__in=tags) # tags__in -> tags attribute in the Project model (ManyToMany realtionship)
    )
    return projects, search_query

def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)  # projects = <page {{page}} of {{paginator.num_pages}}>
        print(projects)
    left_index = int(page) - 4        # 5 > 4 : we always subtract 1 from the right_index, range(1, 5) -> 1, 2, 3 ,4
    if left_index < 1:
        left_index = 1
    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    custom_range = range(left_index, right_index)
    return projects, custom_range
