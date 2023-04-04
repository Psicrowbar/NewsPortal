from django import forms
from .models import Post
from django.core.exceptions import ValidationError

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
