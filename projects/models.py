from django.db import models
from users.models import Profile
import uuid

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True) # 1 profile owner --> many projects
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField("Tag", blank=True)
    project_image = models.ImageField(default='default.jpg', null=True, blank=True)
    demo_link = models.CharField(max_length=2000, blank=True, null=True)
    source_link = models.CharField(max_length=2000, blank=True, null=True)
    vote_total = models.IntegerField(default=0, blank=True, null=True)
    vote_ratio = models.IntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']
    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset
        # values_list('owner__id, flat=True) --> <QuerySet [id1, id2, ...]> 
        # values_list('owner__id) --> <QuerySet [tuples(id, )]>
        # values_list() --> <QuerySet [tuples(owner, id)]>

class Review(models.Model):
    VOTE_TYPE = (('up', 'up vote'),
                 ('down', 'down vote')
                 )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # project deleted --> reviews deleted
    body = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    
    def __str__(self):
        return str(self.value)
    
    class Meta:
        unique_together = [['owner', 'project']]  # one owner can do one review per project
    

class Tag(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    
    def __str__(self):
        return str(self.name)
    