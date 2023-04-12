from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
class DateInput(forms.DateInput):
    input_type = 'date'
class ProductForm(forms.ModelForm):


    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_title',
            'post_category',
            'post_text'
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("post_title")

        return cleaned_data
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user