from .models import Profile, Skill, Message
from django.contrib.auth.models import User
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']  
        labels = {'first_name':'Full_Name'} 
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items(): 
            field.widget.attrs.update({'class':'input'})
            
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']
        labels = {"name":"What's your skill"}
        
    def __init__(self, *args, **kwargs):
            super(SkillForm, self).__init__(*args, **kwargs)
            for name, field in self.fields.items():
                field.widget.attrs.update({'class':'input'})


class MessagForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
        labels = {'body':'Type your message'}
    
    def __init__(self, *args, **kwargs):
        super(MessagForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
